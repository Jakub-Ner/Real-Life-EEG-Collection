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

    self.screenCastFragment = ScreenCastFragment(self, self.CONFIG) 
    self.plotFragments = PlotFragments(self, self.CONFIG) 

    self.pack()

  def pack(self, *args, **kwargs):

    self.screenCastFragment.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    self.plotFragments.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    super().pack(fill=tk.BOTH, expand=True)
    self.after(self.CONFIG.REFRESH_DELAY, self.pack)


wrapper = Wrapper(root, CONFIG)
root.mainloop()
