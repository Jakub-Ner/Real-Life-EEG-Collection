import tkinter as tk
import tkinter.ttk as ttk

from src.fragments.ScreenCastFragment import ScreenCastFragment
from src.fragments.PlotFragments import PlotFragments

from configuration import CONFIG, Config

root = tk.Tk()
root.title(CONFIG.TITLE)
# root.attributes('-zoomed', True)
root.geometry()

class Wrapper(tk.Frame):
  def __init__(self, master, CONFIG: Config, **kwargs):
    super().__init__(master, **kwargs)
    self.CONFIG = CONFIG

    self.full_height = self.winfo_screenheight()
    # self.screenCastFragment = ScreenCastFragment(self, self.CONFIG, height=0.7*self.full_height) 
    self.plotFragments = PlotFragments(self, self.CONFIG, height=0.2*self.full_height) 

    # self.master.bind("<Key>", self.on_resize)

    self.pack()

  def pack(self, *args, **kwargs):

    # self.screenCastFragment.pack(side=tk.TOP, fill=tk.X, expand=False)
    self.plotFragments.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    super().pack(fill=tk.BOTH, expand=True)
    to_ms = int(self.CONFIG.REFRESH_DELAY * 1_000)
    self.after(to_ms, self.pack)

  # def on_resize(self, event):
  #   print(event)
  #   if event.height == 'r':
  #     # self.screenCastFragment.config(height=event.height * 0.7)
  #     self.plotFragments.config(height=event.height * 0.2)

      


wrapper = Wrapper(root, CONFIG)
root.mainloop()
