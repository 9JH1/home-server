import tkinter as tki
from PIL import ImageGrab, ImageTk, Image
import  os

def kill_exp():
    os.system("TaskKill /f /im explorer.exe")

class window():
    def __init__(self):
        self.tk = tki.Tk()
        self.tk.title = "NV2.exe"
        self.tk.attributes("-fullscreen",True)
        self.tk.attributes("-topmost",True)
        self.frame = tki.Frame(self.tk)
        self.frame.pack()

        # HACK: load screenshot
        label = tki.Label(self.tk);
        label.pack()
        a = ImageGrab.grab()
        img_tk = ImageTk.PhotoImage(a)
        label.config(image=img_tk)
        label.image = img_tk

        # HACK: kill explorer
        kill_exp()

def start_exp():
    os.system("start explorer.exe")

if __name__ == '__main__':
    w = window()
    w.tk.mainloop()
