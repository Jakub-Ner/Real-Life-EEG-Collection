from dataclasses import dataclass
from multiprocessing import Process, Queue
import socket


@dataclass
class StreamerConfig:
    CLASS: type  # class to be instantiated


class Recorder(Process):
    def __init__(self, jobs: Queue) -> None:
        super().__init__()
        self.jobs = jobs


class Streamer:
    def record(self, filename: str, jobs: Queue): ...
    def turn_off(self): ...


def connect_to_udp_socket(
    ip: str, port: int, connection_timeout: int = 1
) -> socket.socket:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(connection_timeout)
    udp_socket.bind((ip, port))
    return udp_socket
