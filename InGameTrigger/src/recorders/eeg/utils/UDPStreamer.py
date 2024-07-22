from multiprocessing import Queue
from queue import Empty
from tkinter import messagebox
import logging

from src.utils.logger import get_logger

from .helpers import Streamer, connect_to_udp_socket
from .config_helpers import FORMAT, UDPConfigType

logger = get_logger(__name__, logging.INFO)


class UDPStreamer(Streamer, UDPConfigType):
    def __init__(self, *args, **kwargs) -> None:
        UDPConfigType.__init__(self, *args, **kwargs)

    def turn_off(self):
        logger.info("Turning off UDPStreamer")

    def parse_message(self, message: bytearray, marker: str) -> str | bytearray:
        marker_column = self.COL_SEPARATOR + marker

        if self.OUTPUT_FORMAT == FORMAT.ASCII:
            try:
                msg: str = message.decode("ascii")
                return msg.replace("\n", f"{marker_column}\n")
            except UnicodeDecodeError:
                logger.error("Error decoding message")
                return ""
        else:
            return message + marker_column.encode("ascii")

    def record(self, filename: str, jobs: Queue):
        file_mode = "w+" if self.OUTPUT_FORMAT == FORMAT.ASCII else "wb+"
        self.file = open(f"{filename}.csv", file_mode)
        logger.debug("Saving to " + filename + ".csv")

        try:
            udp_socket = connect_to_udp_socket(
                self.IP, self.PORT, self.CONNECTION_TIMEOUT
            )
            receive_buffer_byte = bytearray(self.BUFFER_BYTE_SIZE)

            while True:
                number_of_bytes_received, _ = udp_socket.recvfrom_into(
                    receive_buffer_byte
                )

                if number_of_bytes_received > 0:
                    message_byte = receive_buffer_byte[:number_of_bytes_received]

                    try:
                        marker = jobs.get(block=False)
                    except Empty:
                        marker = "0"

                    if msg := self.parse_message(message_byte, marker):
                        logger.debug(f"<msg>{msg}</msg>")
                        self.file.write(msg)

        except Exception as ex:
            messagebox.showerror("Error", f"Error during UDP data acquisition:\n{ex}")
        finally:
            logger.info("UDPStreamer finally closed")
            self.file.close()
