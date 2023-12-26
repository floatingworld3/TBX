import tkinter as tk
from src.text_to_fbx import TxtToFbx
import src.styles as styles
import sys

import os


if __name__ == "__main__":
    print(os.path.dirname(os.path.abspath(__file__)))

    root = tk.Tk(className='TBX V2.0')
    root.configure(bg=styles.COLOR_BASE)
    root.title("TBX V2.0")
    root.minsize(800, 600)
    if "linux" in sys.platform:
        img = tk.PhotoImage( file="assets/tbx_logo.png")
        root.tk.call('wm', 'iconphoto', root._w, img)
    else:
        # root.iconbitmap("assets/tbx_logo.ico")
        img = tk.PhotoImage( file="assets/tbx_logo.png")
        root.tk.call('wm', 'iconphoto', root._w, img)
    app = TxtToFbx(root)
    app.pack()

    root.mainloop()
