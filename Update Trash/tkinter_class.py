from tkinter import *


class MainApp:
    def __init__(self):
        self.main_frame = Frame(self.dp)
        self.dp = Tk()
        self.dp_all(self)
        self.main_frame.pack()
        self.dp.mainloop()

if __name__ == "__main__":
    __