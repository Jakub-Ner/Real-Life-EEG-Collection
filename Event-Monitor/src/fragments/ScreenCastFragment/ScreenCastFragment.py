
import tkinter as tk
import tkinter.ttk as ttk

from PIL import ImageTk
import pyautogui


class ScreenCastFragment(tk.Canvas):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)
    
  def update_ss(self):
    ss = pyautogui.screenshot().resize((self.winfo_width(), self.winfo_height()))
    self.ss = ImageTk.PhotoImage(ss) # use pyautogui
    self.create_image(0, 0, image=self.ss, anchor="nw")

  def arrange(self):
    self.update_ss()
    self.pack(fill=tk.BOTH, expand=True)
