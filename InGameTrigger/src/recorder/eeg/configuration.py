from .utils.UDPStreamer import UDPStreamer
from .utils.config_helpers import FORMAT, EEGConfigType, UDPConfigType

udp_streamer = UDPConfigType(
    IP="127.0.0.1", PORT=1000, 
    CLASS=UDPStreamer,
    OUTPUT_FORMAT=FORMAT.BINARY,
    
    )

CONFIG = EEGConfigType(
    streamer=udp_streamer,
)
