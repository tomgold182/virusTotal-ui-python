from tkinter import ttk
from tkinter import StringVar

ENTRY_WIDTH = 40

class IPreportTab:
    def __init__(self, root, frame, clients):
        self.vtClient = clients[0]
        self.shodanClient = clients[1]
        self.root = root
        self.frame = frame
        self.mainVTIPFrame = ttk.Labelframe(frame, text = 'IP report tab')


        self.mainVTIPFrame.grid(column = 0, row = 0, padx = 8, pady = 4)
        ttk.Label(self.mainVTIPFrame, text = "IP:").grid(column = 0, row = 0, sticky = "W")
        ipEntry = ttk.Entry(self.mainVTIPFrame)
        ipEntry.grid(column = 1, row = 0, sticky = "E")


        ttk.Label(self.mainVTIPFrame, text = "Country:").grid(column = 0, row = 1, sticky = "W")
        Country = StringVar()
        ttk.Entry(self.mainVTIPFrame, textvariable = Country, state = 'readonly').grid(column = 1, row = 1, sticky = "E")


        ttk.Label(self.mainVTIPFrame, text = "Owner:").grid(column = 0, row = 2, sticky = "W")
        Owner = StringVar()
        ttk.Entry(self.mainVTIPFrame, textvariable = Owner, state = 'readonly').grid(column = 1, row = 2, sticky = "E")


        ttk.Label(self.mainVTIPFrame, text = "Number of detected URLS:").grid(column = 0, row = 3, sticky = "W")
        NumberOfDetectedURLS = StringVar()
        ttk.Entry(self.mainVTIPFrame, textvariable = NumberOfDetectedURLS, state = 'readonly').grid(column = 1, row = 3, sticky = "E")


        ttk.Label(self.mainVTIPFrame, text = "Number of detected malicious files:").grid(column = 0, row = 4, sticky = "W")
        NumberOfDetectedMaliciousFiles = StringVar()
        ttk.Entry(self.mainVTIPFrame, textvariable = NumberOfDetectedMaliciousFiles, state = 'readonly').grid(column = 1, row = 4, sticky = "E")


        ttk.Label(self.mainVTIPFrame, text = "open ports").grid(column = 0, row = 5, sticky = "W")
        ports = StringVar()
        ttk.Entry(self.mainVTIPFrame, textvariable = ports, state = 'readonly').grid(column = 1, row = 5, sticky = "E")


        notificationFrame = ttk.LabelFrame(self.frame, text=' Notifications', width=40)
        # using the tkinter grid layout manager
        notificationFrame.grid(column=0, row=1, padx=8, pady=10, sticky='W')


        ttk.Label(notificationFrame, text="Errors:").grid(column=0, row=0, sticky='W')  # <== increment row for each
        Error = StringVar()
        ErrorEntry = ttk.Entry(notificationFrame, width=ENTRY_WIDTH, textvariable=Error, state='readonly')
        ErrorEntry.grid(column=1, row=0, sticky='W')

        def CleanErrorMessage():
            Error.set('')


        def print_ip_report():
            try:
                CleanErrorMessage()  # Starting with cleaning the error message bar
                if not ipEntry.get():
                    print('Please enter a IP')
                    Error.set("Please enter a IP!")
                    return

                ipToCheck = ipEntry.get()
                VTresponse = self.vtClient.get_ip_report(ipToCheck)
                SHODANresponse = self.shodanClient.get_ip_report(ipToCheck)
                print(VTresponse)
                Country.set(VTresponse["country"])
                Owner.set(VTresponse["as_owner"])
                NumberOfDetectedURLS.set(len(VTresponse["detected_urls"]))
                NumberOfDetectedMaliciousFiles.set(len(VTresponse["detected_downloaded_samples"]))
                ports.set(SHODANresponse["ports"])


            except Exception as e:
                raise e
                Error.set(e)
        ttk.Button(self.mainVTIPFrame, text = "Check in VT", command = print_ip_report).grid(column = 2, row = 0, sticky = "E")