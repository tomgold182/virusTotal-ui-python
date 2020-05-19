import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from UI import FileReportTab, IPreportTab, URLreportTab, ProportiesTab, PasswordGeneraorTab
from Clients import VTClient
from Clients import shodanClient
import configparser
config = configparser.ConfigParser()
config.read(r'C:\Users\eitan\PycharmProjects\virusTotal-ui-python\conig.ini')

vtCongig = config['VirusTotal']
vtTOKEN = vtCongig['apiKey']

shodanConfig = config['Shodan']
shodanTOKEN = shodanConfig['apiKey']

class VTApp:
    def __init__(self):
        self.clients = [VTClient.VTClient(vtTOKEN), shodanClient.shodanClient(shodanTOKEN)]
        self.root = tk.Tk()
        self.root.iconbitmap(r"C:\Users\eitan\PycharmProjects\virusTotal-ui-python\transparent.ico")
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


        self.proportiesFrame = ttk.Frame(self.tabControl)
        self.proportiesTab = ProportiesTab.ProportiesTab(self.tabControl, self.proportiesFrame)
        self.tabControl.add(self.proportiesFrame, text='Proporties')
        self.tabControl.pack(expand=1, fill="both")


        self.urlFrame = ttk.Frame(self.tabControl)
        self.urlTab = URLreportTab.URLreportTab(self.root, self.urlFrame, self.clients[0])
        self.tabControl.add(self.urlFrame,text = 'URL tab')
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible


        self.ipFrame = ttk.Frame(self.tabControl)
        self.ipTab = IPreportTab.IPreportTab(self.root, self.ipFrame, self.clients)
        self.tabControl.add(self.ipFrame, text='IP tab')
        self.tabControl.pack(expand=1, fill="both")


        self.fileFrame = ttk.Frame(self.tabControl)
        self.fileTab = FileReportTab.FileReportTab(self.tabControl, self.fileFrame, self.clients[0])
        self.tabControl.add(self.fileFrame, text='File tab')
        self.tabControl.pack(expand=1, fill="both")


        self.genFrame = ttk.Frame(self.tabControl)
        self.genTab = PasswordGeneraorTab.PasswordGeneratorTab(self.tabControl, self.genFrame, )
        self.tabControl.add(self.genFrame, text='generate passowrd')
        self.tabControl.pack(expand=1, fill="both")


    def start(self):
        self.root.mainloop()
