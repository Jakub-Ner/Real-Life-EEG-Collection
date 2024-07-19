from .utils.UDPStreamer import UDPStreamer
from .utils.config_helpers import EEGConfiguration, UDPConfiguration

udp_streamer = UDPConfiguration(IP="127.0.0.1", PORT=1000, CLASS=UDPStreamer)

CONFIG = EEGConfiguration(
    streamer=udp_streamer,
)
