import pyautogui
from fire import Fire

from common import wait_for_enter

print('Open Window You want to take ScreenShot of, then click ENTER to start the program')
wait_for_enter()

screenshot = pyautogui.screenshot()


def main(top: tuple[int, int], bottom: tuple[int, int]):
    cropped = screenshot.crop((top[0], top[1], bottom[0], bottom[1]))
    cropped.show()

Fire(main)