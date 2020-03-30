# -*- coding: utf-8 -*-
"""This is the main window of our application

In order to make our code neat and scalable, we want to create one main page and a class for any other tab.
In that way, we are achieving control over our UI elements, while making sure it is easy to add new ones.
"""
# We are importing only the relevant libraries from tkinter
import tkinter as tk
import configparser
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox

from VTPackage import URLreportTab
from VTPackage import IPReportTab
from VTPackage import FileReportTab

from VTPackage import VTClient

config = configparser.ConfigParser()
config.read('config.ini')


class VTApp:
    def __init__(self):
        # Loading the config file
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.virusTotalAPIkey = config['VirusTotal']['apiKey']

        self.vtClient = VTClient.VTClient(self.virusTotalAPIkey)
        self.root = tk.Tk()
        self.root.title("Virus Total UI")
        self.menuBar = Menu()
        self.root.config(menu=self.menuBar)
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_separator()
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        if not self.vtClient.is_API_key_valid():
            messagebox.showerror('Error', "API key is not valid! Check your config file")

        def _quit():
            self.root.quit()  # The app  will exist when this function is called
            self.root.destroy()
            exit()

        self.fileMenu.add_command(label="Exit", command=_quit)  # command callback
        self.tabControl = ttk.Notebook(self.root)  # Create Tab Control

        self.urlFrame = ttk.Frame(self.tabControl)
        self.urlTab = URLreportTab.URLreportTab(self.root, self.urlFrame, self.vtClient)
        self.tabControl.add(self.urlFrame, text='URL')

        self.ipFrame = ttk.Frame(self.tabControl)
        self.ipTab = IPReportTab.IPreportTab(self.tabControl, self.ipFrame, self.vtClient)
        self.tabControl.add(self.ipFrame, text='IP')

        self.fileFrame = ttk.Frame(self.tabControl)
        self.fileTab = FileReportTab.FileReportTab(self.tabControl, self.fileFrame, self.vtClient)
        self.tabControl.add(self.fileFrame, text='File')

        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

    def start(self):
        self.root.mainloop()
