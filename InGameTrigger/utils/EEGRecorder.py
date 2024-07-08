import os
import threading

from utils.constants import DATA_PATH
from utils.listen_udp import listen_udp
from utils.common import get_now

FRUSTRATION = 'frustration'
NEUTRAL = 'neutral'

class EEGRecorder:
    def __init__(self, name, state_duration) -> None:
        self.name = name
        self.event_count = 0
        self.state_duration = state_duration

        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)

    def parse_name(self, state: str, key: str):
        return f'{self.name}_{state}_{key}_{self.event_count}'

    def background_record(self, key: str):
        """Initiates background recording of EEG data in two separate threads.

        This method captures EEG data in two distinct phases:
        1. **Neutral State:** Records data for a specified duration with the filename
           indicating a "neutral" emotional state.
        2. **Frustration State:** After the neutral state recording completes, this
           records data for another specified duration, with the filename indicating
           a "frustration" state.

        `recording_before` lasts 0.1s less than timer clock to ensure it finished before `recording_after` starts.
        """
        current_name = self.parse_name(NEUTRAL, key)
        recording_before_thread = threading.Thread(target=listen_udp, args=(f'{DATA_PATH}/{current_name}', self.state_duration - 0.1))
        recording_before_thread.daemon = True

        current_name = self.parse_name(FRUSTRATION, key)
        recording_after_thread = threading.Thread(target=listen_udp, args=(f'{DATA_PATH}/{current_name}', self.state_duration - 0.1))
        recording_after_thread.daemon = True

        delayed_recording = threading.Timer(self.state_duration, recording_after_thread.start)
        delayed_recording.daemon = True

        recording_before_thread.start()
        delayed_recording.start()

        self.event_count += 1

