# -*- coding: utf-8 -*-
"""This tab is in charge of sending files for a VirusTotal scan

Due to the fact that sending files and getting the results in an ASYNCHRONOUS operation,
we will need to split our strategy into few steps:
    1) Sending the file to VT
    2) Getting a scan ID
    3) Looping to check if the scan was finished
    4) if the scan was finished, show the results.

In order to not get the UI stuck, we will need to use to implement a loop in which does not block the event loop.
We will use a tkinter method called 'after' which gets a time to wait param and a callback.
"""

from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import StringVar

from VTPackage import Consts


class FileReportTab:

    def __init__(self, root, frame, vtClient):
        self.root = root
        self.frame = frame
        self.vtClient = vtClient

        self.mainVTURLframe = ttk.LabelFrame(frame, text=' File report')
        self.mainVTURLframe.grid(column=0, row=1, padx=8, pady=4)

        ttk.Label(self.mainVTURLframe, text="Progress:").grid(column=0, row=1, sticky='W')  # <== right-align
        self.progressBar = ttk.Progressbar(self.mainVTURLframe, orient='horizontal', length=300, mode='determinate')
        self.progressBar.grid(column=1, row=1)

        ttk.Label(self.mainVTURLframe, text="File path:").grid(column=0, row=2, sticky='W')  # <== right-align
        self.filePath = StringVar()
        filePathEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=self.filePath, state='readonly')
        filePathEntry.grid(column=1, row=2, sticky='W')

        ttk.Label(self.mainVTURLframe, text="Status:").grid(column=0, row=3, sticky='W')  # <== right-align
        self.status = StringVar()
        statusEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=self.status, state='readonly')
        statusEntry.grid(column=1, row=3, sticky='W')

        ttk.Label(self.mainVTURLframe, text="Positive Indications:").grid(column=0, row=4, sticky='W')  # <== right-align
        self.positiveIndications = StringVar()
        positiveIndicationsEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=self.positiveIndications, state='readonly')
        positiveIndicationsEntry.grid(column=1, row=4, sticky='W')

        ttk.Label(self.mainVTURLframe, text="SHA1:").grid(column=0, row=5, sticky='W')  # <== right-align
        self.sha1 = StringVar()
        sha1Entry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=self.sha1, state='readonly')
        sha1Entry.grid(column=1, row=5, sticky='W')

        ttk.Label(self.mainVTURLframe, text="SHA256:").grid(column=0, row=6, sticky='W')  # <== right-align
        self.sha256 = StringVar()
        sha256Entry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=self.sha256, state='readonly')
        sha256Entry.grid(column=1, row=6, sticky='W')

        chooseFileButton = ttk.Button(self.mainVTURLframe, text="Choose File", width=40, command=self._scanFile).grid(column=1, row=0)

        self.scanCheckingTimeInterval = 25000  # This is the amount of time we are going to wait before asking VT again if it already processed our scan request

        for child in self.mainVTURLframe.winfo_children():
            child.grid_configure(padx=4, pady=2)

    def showResults(self, results):
        try:
            self.sha1.set(results["sha1"])
            self.sha256.set(results["sha256"])
            self.positiveIndications.set(results["positives"])
        except Exception as e:
            messagebox.showerror('Error', e)

    def checkStatus(self):
        try:
            self.scanResult = self.vtClient.get_file_report(self.scanID)
            print(self.scanResult)
            if self.scanResult["response_code"] == -2:  # By reading the next line, you can understand what is the meaning of the -2 response ode
                self.status.set("Scanning...")
                self.progressBar['value'] = self.progressBar['value'] + 5
                self.root.update_idletasks()
                self.mainVTURLframe.after(self.scanCheckingTimeInterval, self.checkStatus)

            else:
                self.hasScanFinished = True
                self.showResults(self.scanResult)
                self.status.set("Finished!")

                self.progressBar['value'] = 100
        except Exception as e:
            if "To much API requests" in str(e):
                pass

    def _scanFile(self):
        try:
            self.progressBar['value'] = 0
            filePath = filedialog.askopenfilename(initialdir="/", title="Select file for VT", filetypes=(("EXE files", "*.exe"), ("all files", "*.*")))

            if (filePath):  # Only if the user chose a file, we will want to continue the process
                self.filePath.set(filePath)
                self.status.set("Sending file...")
                self.progressBar['value'] = 10

                self.root.update_idletasks()
                self.scanID = self.vtClient.scan_file(filePath)
                self.hasScanFinished = False
                if not self.hasScanFinished:
                    self.scanResult = self.vtClient.get_file_report(self.scanID)
                    print(self.scanResult)
                    self.checkStatus()
                    # We could have been using time.sleep() or time.wait(), but then our UI would get stuck.
                    # by using after, we are initiating a callback in which does not blocks our event loop

        except Exception as e:
            messagebox.showerror('Error', e)
