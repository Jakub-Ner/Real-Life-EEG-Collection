import keyboard


def wait_for_enter():
    while True:
        if keyboard.is_pressed("enter"):
            break
