import random
from ahk import AHK
from pynput import keyboard
import time
import fire

from utils.common import get_now, parse_filename, parse_range, EEGEvent
from utils.EEGRecorder import EEGRecorder

class RandomClick(EEGEvent):
    def __init__(self, state_duration, random_range, key: str) -> None:
        super().__init__(state_duration)
        self.random_range = random_range
        self.ahk = AHK()
        self.time_to_wait = 0
        self.key = key

        self.init_key_listener()

    def init_key_listener(self): 
        key_listener = keyboard.Listener(on_press=self.on_press)
        key_listener.daemon = True
        key_listener.start()

    def set_timer(self):
        self.time_to_wait = random.choice(self.random_range) - self.state_duration

    def on_press(self, key):
        if self.key == str(key).strip("'"):
            print(f'You pressed {self.key}')
            self.set_timer()
        return key

    def wait(self):
        self.set_timer()

        while self.time_to_wait > 0:
            time.sleep(1)
            self.time_to_wait -= 1
        
    def trigger(self, key: str):
        time.sleep(self.state_duration)

        self.ahk.key_down(key)
        time.sleep(0.1)
        self.ahk.key_up(key)

        time.sleep(self.state_duration)


@parse_filename
@parse_range
def main(key: str, random_range: tuple, filename: str, state_duration: int=2):
    print(f'Initiating random klick {get_now()} with {locals()}')
    event = RandomClick(state_duration, random_range, key)
    recorder = EEGRecorder(filename, state_duration)

    while True:
        event.wait()
        recorder.background_record(key)
        event.trigger(key)


if __name__ == '__main__':
    fire.Fire(main)

