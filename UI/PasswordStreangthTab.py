from tkinter import ttk
from tkinter import StringVar
from UI import Consts
from tkinter import filedialog
from tkinter import messagebox
import time


class FileReportTab:

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        self.generateFrame = ttk.LabelFrame(frame, text='File report')
        self.generateFrame.grid(column=0, row=1, padx=8, pady=4)

        ttk.Label(self.generateFrame, text="Progress:").grid(column=0, row=1, sticky='W')  # <== right-align
        self.progressBar = ttk.Progressbar(self.generateFrame, orient='horizontal', length=300, mode='determinate')
        self.progressBar.grid(column=1, row=1)

        ttk.Label(self.generateFrame, text="File path:").grid(column=0, row=2, sticky='W')  # <== right-align
        self.filePath = StringVar()
        filePathEntry = ttk.Entry(self.generateFrame, width=Consts.ENTRY_WIDTH, textvariable=self.filePath, state='readonly')
        filePathEntry.grid(column=1, row=2, sticky='W')

        ttk.Label(self.generateFrame, text="Status:").grid(column=0, row=3, sticky='W')  # <== right-align
        self.status = StringVar()
        statusEntry = ttk.Entry(self.generateFrame, width=Consts.ENTRY_WIDTH, textvariable=self.status, state='readonly')
        statusEntry.grid(column=1, row=3, sticky='W')

        ttk.Label(self.generateFrame, text="Positive Indications:").grid(column=0, row=4, sticky='W')  # <== right-align
        self.positiveIndications = StringVar()
        positiveIndicationsEntry = ttk.Entry(self.generateFrame, width=Consts.ENTRY_WIDTH, textvariable=self.positiveIndications, state='readonly')
        positiveIndicationsEntry.grid(column=1, row=4, sticky='W')

        ttk.Label(self.generateFrame, text="SHA1:").grid(column=0, row=5, sticky='W')  # <== right-align
        self.sha1 = StringVar()
        sha1Entry = ttk.Entry(self.generateFrame, width=Consts.ENTRY_WIDTH, textvariable=self.sha1, state='readonly')
        sha1Entry.grid(column=1, row=5, sticky='W')

        ttk.Label(self.generateFrame, text="SHA256:").grid(column=0, row=6, sticky='W')  # <== right-align
        self.sha256 = StringVar()
        sha256Entry = ttk.Entry(self.generateFrame, width=Consts.ENTRY_WIDTH, textvariable=self.sha256,
                                state='readonly')
        sha256Entry.grid(column=1, row=6, sticky='W')

        chooseFileButton = ttk.Button(self.generateFrame, text="Choose File", width=40, command=self.show_file_report).grid(
            column=1, row=0)

        self.scanCheckingTimeInterval = 25000  # This is the amount of time we are going to wait before asking VT again if it already processed our scan request

        for child in self.generateFrame.winfo_children():
            child.grid_configure(padx=4, pady=2)


    def move_progressbar(self, amount = 100):
        previousAmount = self.progressBar['value']
        for i in range(amount - int(previousAmount)):
            self.progressBar['value'] = previousAmount + i + 1
            time.sleep(0.05)
            self.progressBar.update()


    def _scanFile(self):
        try:
            self.progressBar['value'] = 0
            filePath = filedialog.askopenfilename(initialdir="/", title="Select file to scan",
                                                  filetypes=(('All files', "*"),
                                                             ('EXE files', "*.exe"),
                                                             ("Jar files", "*.jar")))
            self.move_progressbar(25)

            if (filePath):
                self.filePath.set(filePath)
                self.status.set('scaning file')
                self.scanID = self.vtClient.scan_file(filePath)
                self.move_progressbar(50)
                for t in range(3):
                    t = t + 1
                    self.scanResult = self.vtClient.get_file_report(self.scanID)
                    if self.scanResult != False:
                        self.move_progressbar(100)
                        self.status.set("scan finished")
                        print('scan has finished')
                        return self.scanResult
                    else:
                        self.move_progressbar(50 + 16 * t)
                        print('scan not finished')
                        time.sleep(10)
                print('scan failed')
                return False
            self.root.lift()
            messagebox.showerror(title = "no file", message = 'this is not a file. \n please choose a valid file')



        except Exception as e:
            self.root.lift()
            messagebox.showerror(title = "Error", message = "an error occurred while scanning this file. \n try again")
            raise e
            return False
            pass


    def checkStatus(self):
        try:
            print("checking")
            self.scanResult = self.vtClient.get_file_report(self.scanID)

            if self.scanResult["response_code"] == -2:
                self.status.set("scanning...")
                self.progressBar['value'] = self.progressBar['value'] + 5
            else:
                self.hasScanFinished = True
                self.sha1.set(self.scanResult["sha1"])
                self.sha256.set(self.scanResult["sha256"])

        except Exception as e:
            pass
    def show_file_report(self):
        fileReport = self._scanFile()
        if fileReport == False:
            self.status.set("scan failed")
            return
        self.positiveIndications.set(fileReport['positives'])
        self.sha1.set(fileReport['sha1'])
        self.sha256.set(fileReport['sha256'])


