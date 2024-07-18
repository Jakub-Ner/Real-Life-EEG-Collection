import socket
import os
import time
import warnings
from tkinter import messagebox

warnings.filterwarnings("ignore")

IP = "127.0.0.1"
PORT = 1000
TIMEOUT = 1 # in seconds

def listen_udp(full_path, duration: int, dialogue_box=True):
    file = open(f"{full_path}.csv", "wb+")

    try:
        end_point = (IP, PORT)

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.settimeout(TIMEOUT)
        udp_socket.bind(end_point)
        receive_buffer_byte = bytearray(1024)

        now = time.time()
        while time.time() - now < duration: 
            number_of_bytes_received, _ = udp_socket.recvfrom_into(receive_buffer_byte)

            if number_of_bytes_received > 0:
                message_byte = receive_buffer_byte[:number_of_bytes_received]
                # add marker column 
                file.write(message_byte)

    except Exception as ex:
        if dialogue_box:
            messagebox.showerror("Error", f"Error during UDP data acquisition: {ex}")
        else:
            raise Exception(f"Error during UDP data acquisition: {ex}")
    finally:
        file.close()


if __name__ == "__main__":
    listen_udp("test", 5)