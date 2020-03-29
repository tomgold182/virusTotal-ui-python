# -*- coding: utf-8 -*-
"""This tab is in charge of sending files for a VirusTotal scan

Due to the fact that sending files and getting the results in an ASYNCHRONOUS operation,
we will need to split our strategy into few steps:
    1) Sending the file to VT
    2) Getting a scan ID
    3) Looping to check if the scan was finished
    4) if the scan was finished, show the results.

In order to not get the UI stuck, we will need to use threads.
"""

from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import StringVar

from VTPackage import Consts

import time
import threading

class FileReportTab:

    def __init__(self,root,frame, vtClient):
        self.root = root
        self.frame = frame
        self.vtClient= vtClient
        self.mainVTURLframe = ttk.LabelFrame(frame, text=' File report')

        ttk.Label(self.mainVTURLframe, text="Progress:").grid(column=0, row=1, sticky='W')  # <== right-align
        self.mainVTURLframe.grid(column=0, row=1, padx=8, pady=4)
        self.progressBar = ttk.Progressbar(self.mainVTURLframe, orient='horizontal', length=300, mode='determinate')
        self.progressBar.grid(column=1, row=1)

        ttk.Label(self.mainVTURLframe, text="Status:").grid(column=0, row=2, sticky='W')  # <== right-align
        self.status = StringVar()
        statusEntry = ttk.Entry(self.mainVTURLframe, width=Consts.entry_width, textvariable=self.status, state='readonly')
        statusEntry.grid(column=1, row=2, sticky='W')

        chooseFileButton = ttk.Button(self.mainVTURLframe, text="Choose File",width = 40,command=self._scanFile).grid(column=1, row=0)

        for child in self.mainVTURLframe.winfo_children():
            child.grid_configure(padx=4, pady=2)

    def _scanFile(self):
        try:
            self.progressBar['value'] = 0
            hasScanFinished = False
            filePath = filedialog.askopenfilename(initialdir = "/",title = "Select file for VT",filetypes = (("EXE files","*.exe"),("all files","*.*")))

            if (filePath): # Only if the user chose a file, otherwise we will get an error
                self.status.set("Sending file...")
                scanID = self.vtClient.scan_file(filePath)
                while not hasScanFinished:
                    scanResult = self.vtClient.get_file_report(scanID)
                    print(scanResult)
                    if scanResult["response_code"] == -2: # By reading the next line, you can understand what is the meaning of the -2 response ode
                        self.status.set("Waiting for scan...")
                        self.progressBar['value'] = self.progressBar['value'] + 20
                        self.root.update_idletasks()
                        time.sleep(30)
                    else:
                        self.status.set("Finished!")
                        hasScanFinished = True
                        self.progressBar['value'] = 100

        except Exception as e:
            messagebox.showerror('Error',e)
















