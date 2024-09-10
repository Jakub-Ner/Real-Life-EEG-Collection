import tkinter as tk
import tkinter.ttk as ttk

from src.fragments.ScreenCastFragment.ScreenCastFragment import ScreenCastFragment

from configuration import GENERAL_CONFIG

root = tk.Tk()
root.title(GENERAL_CONFIG.TITLE)
root.attributes('-zoomed', True)
# root.state('zoomed')
root.geometry()

class Wrapper(tk.Frame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)

    self.screenCastFragment = ScreenCastFragment(self) 
    self.screenCastFragment2 = ScreenCastFragment(self) 

    # self.pack(fill=tk.BOTH, expand=True)
    self.arange()

  def arange(self):
    self.pack(anchor="n")

    self.screenCastFragment.arrange()
    self.screenCastFragment2.arrange()

    self.after(300, self.arange)


wrapper = Wrapper(root)
root.mainloop()
