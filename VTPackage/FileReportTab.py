from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk



class FileReportTab:

    def __init__(self,root,frame,vtClient):
        self.root = root
        self.frame = frame
        self.vtClient= vtClient
        self.mainVTURLframe = ttk.LabelFrame(frame, text=' File report tab!')

        self.mainVTURLframe.grid(column=0, row=0, padx=8, pady=4)
        self.progress = ttk.Progressbar(self.mainVTURLframe, orient='horizontal', length=100, mode='determinate')
        self.ddd = ttk.Progressbar()
        self.progress.grid(column=0, row=1)

        chooseFileButton = ttk.Button(self.mainVTURLframe, text="Choose File",command=self._openFileChooser).grid(column=0, row=0)

        for child in self.mainVTURLframe.winfo_children():
            child.grid_configure(padx=4, pady=2)

    def _openFileChooser(self):
        try:
            print('in')
            filePath = filedialog.askopenfilename(initialdir = "/",title = "Select file for VT",filetypes = (("EXE files","*.exe"),("all files","*.*")))
            print(filePath)
            result = self.vtClient.scan_file(filePath)

            self.progress['value'] = 20
            self.root.update_idletasks()


        except Exception as e:
            messagebox.showerror('Error',e)
















