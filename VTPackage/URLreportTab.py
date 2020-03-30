# -*- coding: utf-8 -*-
"""This tab is in charge of sending sending URLs for investigation

VirusTotal gives us the ability to send a suspicious URL to for analysis.
It then returns the results as can be seen inside the code.
"""

from tkinter import ttk
from tkinter import StringVar
from VTPackage import Consts


class URLreportTab:
    def __init__(self, root, frame, vtClient):
        self.root = root
        self.frame = frame
        self.mainVTURLframe = ttk.LabelFrame(frame, text=' URL report tab!')

        # using the tkinter grid layout manager
        self.mainVTURLframe.grid(column=0, row=0, padx=8, pady=4)
        ttk.Label(self.mainVTURLframe, text="URL:").grid(column=0, row=0, sticky='W')  # What does sticky does?      Sticky sayes where to stick the label to : N,S,E,W
        urlEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH)
        urlEntry.grid(column=1, row=0, sticky='E')

        ttk.Label(self.mainVTURLframe, text="Positive Indications:").grid(column=0, row=1, sticky='W')  # <== right-align
        Positive = StringVar()
        PositiveEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=Positive, state='readonly')
        PositiveEntry.grid(column=1, row=1, sticky='W')

        ttk.Label(self.mainVTURLframe, text="Detections:").grid(column=0, row=2, sticky='W')  # <== right-align
        detections = StringVar()
        detectionsEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=detections, state='readonly')
        detectionsEntry.grid(column=1, row=2, sticky='W')

        self.notificationFrame = ttk.LabelFrame(self.frame, text=' Notifications', width=40)
        # using the tkinter grid layout manager
        self.notificationFrame.grid(column=0, row=1, padx=8, pady=10, sticky='W')

        ttk.Label(self.notificationFrame, text="Errors:").grid(column=0, row=0, sticky='W')  # <== increment row for each
        Error = StringVar()
        ErrorEntry = ttk.Entry(self.notificationFrame, width=Consts.ENTRY_WIDTH, textvariable=Error, state='readonly')

        ErrorEntry.grid(column=1, row=0, sticky='W')

        def _cleanErrorMessage():  # We could have been doing this without a function, but it is more neat that way
            Error.set("")

        def _getReport():
            # the _ notation before a function means that this function is internal to the class only. As python cannot really prevent you from using it outside the class (as C# for example) the notation is being used to warn other developers not to call this function outside the class
            try:
                _cleanErrorMessage()  # Starting with cleaning the error message bar
                if not urlEntry.get():
                    print('Please enter a URL')
                    Error.set("Please enter a URL!")
                    return

                urlToCheck = urlEntry.get()
                response = vtClient.get_url_report(urlToCheck)
                print(response)
                Positive.set(response["positives"])
                scans = response["scans"]

                findings = set()
                for key, value in scans.items():
                    if value["detected"]:
                        findings.add(value["result"])
                detections.set(",".join([str(finding) for finding in findings]))

            except Exception as e:
                print(e)
                Error.set(e)

        checkURLinVTButton = ttk.Button(self.mainVTURLframe, text='Check in VT!', command=_getReport).grid(column=2, row=0)

        # Instead of setting padding for each UI element, we can just iterate through the children of the main UI object.
        for child in self.mainVTURLframe.winfo_children():
            child.grid_configure(padx=4, pady=2)
        for child in self.notificationFrame.winfo_children():
            child.grid_configure(padx=4, pady=2)
