from SecurityClients.BaseClient import BaseClient


import requests

class ShodanClient(BaseClient):
    def __init__(self,apiKey):
        super().__init__(apiKey)
        self.baseURI = 'https://api.shodan.io/shodan'
        self.ipURI = 'host'


    def get_ip_info(self,ipAddress):
        try:
            requestURL = f'{self.baseURI}/{self.ipURI}/{ipAddress}?key={self.apiKey}'
            response = requests.get(requestURL)

            info = response.json()

            print(info)
            return info
        except Exception as e:
            print(f'Shodan IP scan error:{str(e)}')


# H.W
# Implement error handling
# add ApiKey verification



