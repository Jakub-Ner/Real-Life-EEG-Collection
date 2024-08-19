import pyautogui
import tkinter as tk
from PIL import ImageTk
import tkinter.font as tkFont

from common import wait_for_enter


def update_mouse_position(event):
    x, y = pyautogui.position()
    canvas.itemconfig("coords", text=f"Mouse position: ({x}, {y})")


def log_mouse_click(event):
    print(f"Mouse clicked at: ({event.x}, {event.y})")


print(
    "Open Window You want to take ScreenShot of, then click ENTER to start the program"
)
wait_for_enter()

root = tk.Tk()
root.title("Screenshot with Mouse Coordinates")

screenshot = pyautogui.screenshot()
tk_image = ImageTk.PhotoImage(screenshot)

# Create a canvas and add the image to it
canvas = tk.Canvas(root, width=screenshot.width, height=screenshot.height)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=tk_image)
canvas.create_text(
    10,
    10,
    anchor="nw",
    text="Mouse position: (0, 0)",
    font=tkFont.Font(family="Helvetica", size=16, weight="bold"),
    fill="white",
    tags="coords",
)


root.bind("<Button-1>", log_mouse_click)
root.bind("<Motion>", update_mouse_position)
root.mainloop()
