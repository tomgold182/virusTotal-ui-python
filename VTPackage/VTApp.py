import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from VTPackage import URLreportTab
from VTPackage import VTClient



class VTApp:
    def __init__(self):
        self.vtClient = VTClient.VTClient('95d362bc20946172c059611c765f7620da76f98ab4a202565b66cc4bafea9ed9')
        self.root = tk.Tk()
        self.root.title("VT App")
        self.menuBar = Menu()
        self.root.config(menu=self.menuBar)
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_separator()
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        def _quit():
            self.root.quit()  # win will exist when this function is called
            self.root.destroy()
            exit()

        self.fileMenu.add_command(label="Exit", command=_quit)  # command callback
        self.tabControl = ttk.Notebook(self.root)  # Create Tab Control
        self.urlFrame = ttk.Frame(self.tabControl)
        self.urlTab = URLreportTab.URLreportTab(self.root,self.urlFrame, self.vtClient)
        self.tabControl.add(self.urlFrame,text = 'URL tab')
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

    def start(self):
        self.root.mainloop()

