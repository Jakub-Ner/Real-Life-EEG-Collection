import tkinter as tk
import tkinter.ttk as ttk

from src.fragments.PlotFragments import PlotFragments
from src.fragments.ScreenCastFragment import ScreenCastFragment
from src.fragments.PlotEegFragment import PlotEegFragment

from configuration import CONFIG

root = tk.Tk()
root.title(CONFIG.TITLE)
root.attributes('-zoomed', True)
# root.state('zoomed')
root.geometry()

class Wrapper(tk.Frame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)

    self.screenCastFragment = ScreenCastFragment(self, CONFIG) 
    self.plotFragments = PlotFragments(self, CONFIG) 

    self.pack()

  def pack(self):
    self.screenCastFragment.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    self.plotFragments.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    super().pack(fill=tk.BOTH, expand=True)

    self.after(40, self.pack)


wrapper = Wrapper(root)
root.mainloop()
