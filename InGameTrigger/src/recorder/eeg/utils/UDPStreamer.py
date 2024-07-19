from multiprocessing import Queue
from tkinter import messagebox

from src.utils.logger import get_logger

from .helpers import Streamer, connect_to_udp_socket
from .config_helpers import UDPConfiguration

logger = get_logger(__name__)

def decode_message(message_byte: bytearray) -> bool:
    logger.debug(f"Received {len(message_byte)} bytes")
    try:
        message = message_byte.decode("ascii")
        logger.debug(f'<start>{message}<end>')
        return True
    except UnicodeDecodeError: 
        logger.error("Error decoding message")
        return False

class UDPStreamer(Streamer, UDPConfiguration):
    def __init__(self, *args, **kwargs) -> None:
        UDPConfiguration.__init__(self, *args, **kwargs)

    def turn_off(self):
        logger.info("Turning off UDPStreamer")        

    def record(self, filename: str, jobs: Queue):
        self.file = open(f"{filename}.csv", "wb+")
        logger.debug("Saving to " + filename + ".csv")

        try:
            udp_socket = connect_to_udp_socket(
                self.IP, self.PORT, self.CONNECTION_TIMEOUT
            )
            receive_buffer_byte = bytearray(self.BUFFER_BYTE_SIZE)
            # TODO use jobs

            while True:
                number_of_bytes_received, _ = udp_socket.recvfrom_into(
                    receive_buffer_byte
                )

                if number_of_bytes_received > 0:
                    message_byte = receive_buffer_byte[:number_of_bytes_received]
                    # decode_message(message_byte)
                    self.file.write(message_byte)

        except Exception as ex:
            messagebox.showerror("Error", f"Error during UDP data acquisition:\n{ex}")
        finally:
            logger.info("UDPStreamer finally closed")
            self.file.close()
