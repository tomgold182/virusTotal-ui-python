from tkinter import ttk
from UI import Consts
import configparser
from pathlib import Path
from Clients.VTClient import VTClient
from Clients.shodanClient import shodanClient
config = configparser.ConfigParser()
configfile = Path(r'C:\Users\eitan\PycharmProjects\virusTotal-ui-python\conig.ini')
config.read(configfile)

class ProportiesTab:

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.vtClient = VTClient(config['VirusTotal']['apiKey'])
        self.shodanClient = shodanClient(config['Shodan']['apiKey'])

        self.proportiesFrame = ttk.LabelFrame(frame, text='Proporties')
        self.proportiesFrame.grid(column=0, row=1, padx=8, pady=4)

        ttk.Label(self.proportiesFrame, text="virus total apikey:").grid(column=0, row=2, sticky='W')  # <== right-align
        vtApiKeyEntry = ttk.Entry(self.proportiesFrame, width=Consts.ENTRY_WIDTH)
        vtApiKeyEntry.grid(column=1, row=2, sticky='W')
        vtApiKeyEntry.insert(0, config.get('VirusTotal', 'apiKey'))


        ttk.Label(self.proportiesFrame, text="shodan apikey:").grid(column=0, row=3, sticky='W')  # <== right-align
        shodanApiKeyEntry = ttk.Entry(self.proportiesFrame, width=Consts.ENTRY_WIDTH)
        shodanApiKeyEntry.grid(column=1, row=3, sticky='W')
        shodanApiKeyEntry.insert(0, config.get('Shodan', 'apiKey'))

        def Save():
            config.set('VirusTotal', 'apiKey', str(vtApiKeyEntry.get()))
            config.set('Shodan', 'apiKey', str(shodanApiKeyEntry.get()))
            config.write(configfile.open('w'))


            if self.vtClient.get_ip_report(IP = '8.8.8.8') == 'invalid api':
                print('invalid VT api key')
            try:
                self.shodanClient.get_ip_report(IP = '8.8.8.8')
            except:
                if Exception == "Invalid API key":
                    print('invalid shodan api key')




        saveButton = ttk.Button(self.proportiesFrame, text='Save', command=Save).grid(column=1, row=4)
