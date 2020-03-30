# -*- coding: utf-8 -*-
"""This tab is in charge of sending sending IP addresses for investigation

Some times,
we will want the analyze certain IP address to understand if it is associated with malicious files or URLs.
VirusTotal gives us some useful information like where in the world this IP address hosted,
and the amount of malicious files that was downloaded from it.
"""

from tkinter import ttk
from tkinter import StringVar

from VTPackage import Consts


class IPreportTab:

    def __init__(self, root, frame, vtClient):
        self.root = root
        self.frame = frame
        self.mainVTURLframe = ttk.LabelFrame(frame, text=' IP report tab!')

        # using the tkinter grid layout manager
        self.mainVTURLframe.grid(column=0, row=0, padx=8, pady=4)
        ttk.Label(self.mainVTURLframe, text="IP:").grid(column=0, row=0, sticky='W')  # Sticky sayes where to stick the label to : N,S,E,W
        ipEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH)
        ipEntry.grid(column=1, row=0, sticky='E')

        ttk.Label(self.mainVTURLframe, text="Country:").grid(column=0, row=1, sticky='W')  # <== right-align
        Country = StringVar()
        CountryEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=Country, state='readonly')
        CountryEntry.grid(column=1, row=1, sticky='W')

        ttk.Label(self.mainVTURLframe, text="Owner:").grid(column=0, row=2, sticky='W')  # <== right-align
        Owner = StringVar()
        OwnerEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=Owner, state='readonly')
        OwnerEntry.grid(column=1, row=2, sticky='W')

        ttk.Label(self.mainVTURLframe, text="Number of detected URLS:").grid(column=0, row=3, sticky='W')  # <== right-align
        numberOfDetectedUrls = StringVar()
        numberOfDetectedUrlsEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=numberOfDetectedUrls, state='readonly')
        numberOfDetectedUrlsEntry.grid(column=1, row=3, sticky='W')

        ttk.Label(self.mainVTURLframe, text="Number of detected malicious files:").grid(column=0, row=4, sticky='W')  # <== right-align
        numberOfDownloadedMaliciousFiles = StringVar()
        numberOfDownloadedMaliciousFilesEntry = ttk.Entry(self.mainVTURLframe, width=Consts.ENTRY_WIDTH, textvariable=numberOfDownloadedMaliciousFiles, state='readonly')
        numberOfDownloadedMaliciousFilesEntry.grid(column=1, row=4, sticky='W')

        self.notificationFrame = ttk.LabelFrame(self.frame, text=' Notifications', width=Consts.ENTRY_WIDTH)
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
                if not ipEntry.get():
                    errMessage = 'Please enter an IP address'
                    print(errMessage)
                    Error.set(errMessage)
                    return

                ipToCheck = ipEntry.get()
                response = vtClient.get_ip_report(ipToCheck)
                print(response)
                Country.set(response["country"])
                Owner.set(response["as_owner"])
                numberOfDetectedUrls.set(len(response["detected_urls"]))  # len helps us count the amount of items inside the list
                numberOfDownloadedMaliciousFiles.set(len(response["detected_downloaded_samples"]))

            except Exception as e:
                print(e)
                Error.set(e)

        checkURLinVTButton = ttk.Button(self.mainVTURLframe, text='Check in VT!', command=_getReport).grid(column=2, row=0)

        # Instead of setting padding for each UI element, we can just iterate through the children of the main UI object.
        for child in self.mainVTURLframe.winfo_children():
            child.grid_configure(padx=4, pady=2)
        for child in self.notificationFrame.winfo_children():
            child.grid_configure(padx=4, pady=2)
