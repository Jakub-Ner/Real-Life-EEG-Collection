from __future__ import annotations
from multiprocessing import Process, Queue
import os
from queue import Empty
from tkinter import messagebox
import logging

from src.utils.logger import get_logger
from .helpers import connect_to_udp_socket
from .config_helpers import FORMAT, EegUdpConfig

logger = get_logger(__name__, logging.INFO)


class EegUdpRecorder(Process):
    def __init__(self, config: EegUdpConfig, jobs: Queue):
        super().__init__()
        self.config = config
        self.jobs = jobs

    def turn_off(self):
        logger.info("Turning off UDPStreamer")

    def parse_message(self, message: bytearray, marker: str) -> str | bytearray:
        marker_column = self.config.COL_SEPARATOR + marker

        if self.config.OUTPUT_FORMAT == FORMAT.ASCII:
            try:
                msg: str = message.decode("ascii")
                return msg.replace("\n", f"{marker_column}\n")
            except UnicodeDecodeError:
                logger.error("Error decoding message")
                return ""
        else:
            return message + marker_column.encode("ascii")

    def run(self):
        os.makedirs(self.config.DATA_PATH, exist_ok=True)
        self.record(os.path.join(self.config.DATA_PATH, self.config.FILENAME))

    def record(self, path: str):
        file_mode = "w+" if self.config.OUTPUT_FORMAT == FORMAT.ASCII else "wb+"
        self.file = open(path, file_mode)
        logger.debug("Saving to " + path)

        try:
            udp_socket = connect_to_udp_socket(
                self.config.IP, self.config.PORT, self.config.CONNECTION_TIMEOUT
            )
            receive_buffer_byte = bytearray(self.config.BUFFER_BYTE_SIZE)

            while True:
                number_of_bytes_received, _ = udp_socket.recvfrom_into(
                    receive_buffer_byte
                )

                if number_of_bytes_received > 0:
                    message_byte = receive_buffer_byte[:number_of_bytes_received]

                    try:
                        marker = self.jobs.get(block=False)
                    except Empty:
                        marker = "0"

                    if msg := self.parse_message(message_byte, marker):
                        logger.debug(f"<msg>{msg}</msg>")
                        self.file.write(msg)
                        self.file.flush()


        except Exception as ex:
            messagebox.showerror("Error", f"Error during UDP data acquisition:\n{ex}")
        finally:
            logger.info("UDPStreamer finally closed")
            self.file.close()
