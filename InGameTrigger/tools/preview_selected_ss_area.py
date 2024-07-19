import pyautogui
import fire

from common import wait_for_enter


def main(top: tuple[int, int], bottom: tuple[int, int]):
    print(
        "Open Window You want to take ScreenShot of, then click ENTER to start the program"
    )
    wait_for_enter()

    width = bottom[0] - top[0]
    height = bottom[1] - top[1]
    pyautogui.screenshot(region=(top[0], top[1], width, height)).show()


fire.Fire(main)
