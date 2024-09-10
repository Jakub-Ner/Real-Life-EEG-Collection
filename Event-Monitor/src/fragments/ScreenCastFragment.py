
import tkinter as tk
from PIL import ImageTk
import pyautogui

from src.utils.config_helpers import Config



class ScreenCastFragment(tk.Canvas):
  def __init__(self, master, CONFIG: Config, **kwargs):
    super().__init__(master, **kwargs)
    self.CONFIG = CONFIG
    
  def update_ss(self):
    ss = pyautogui.screenshot().resize((self.winfo_width(), self.winfo_height()))
    self.ss = ImageTk.PhotoImage(ss) 
    self.create_image(0, 0, image=self.ss, anchor="nw")

  def pack(self, *args, **kwargs):
    self.update_ss()
    super().pack(*args, **kwargs)

