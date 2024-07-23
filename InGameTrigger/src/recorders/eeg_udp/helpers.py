import socket


def connect_to_udp_socket(
    ip: str, port: int, connection_timeout: int = 1
) -> socket.socket:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(connection_timeout)
    udp_socket.bind((ip, port))
    return udp_socket
