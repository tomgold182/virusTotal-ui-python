import requests
from Clients.Client import Client

class VTClient(Client):
    def __init__(self, apiKey):
        super().__init__(apiKey)
        self.baseURL = 'https://www.virustotal.com/vtapi/v2/'

    def get_url_report(self,URL):
        try:
            requestURL = f'{self.baseURL}url/report?apikey={self.apiKey}&resource={URL}/'
            payload = {}
            headers = {}
            response = requests.request("GET", requestURL, headers=headers, data=payload)
            if response.status_code == 204:
                raise Exception("To much API requests")
            info = response.json()
            if info["response_code"] == 0:
                raise Exception(info["verbose_msg"])
            return info

        except Exception as e:
            print(e)
            raise Exception(e)


    def get_ip_report(self,IP):
        try:
            requestURL = f'{self.baseURL}ip-address/report?apikey={self.apiKey}&ip={IP}'
            payload = {}
            headers = {}
            response = requests.request("GET", requestURL, headers=headers, data=payload)
            if response.status_code == 403:
                return 'invalid api'
            result = response.json()
            if response.status_code == 204:
                raise Exception("To much API requests")
            info = response.json()
            if info["response_code"] == 0:
                raise Exception(info["verbose_msg"])
            return info

        except Exception as e:
            print(e)
            raise Exception(e)

    def scan_file(self, filePath):
        try:
            url = f'{self.baseURL}file/scan'

            params = {'apikey': self.apiKey}

            files = {'file': (filePath, open(filePath, 'rb'))}

            response = requests.post(url, files=files, params=params)
            info = response.json()
            if info['response_code'] == 204:
                print("to many api requests")
            if info["response_code"] == 1:
                return info["scan_id"]
            else:
                raise Exception("error")
        except Exception as e:
            raise e

    def get_file_report(self, scan_id):
        url = f'{self.baseURL}file/report'

        params = {'apikey': self.apiKey, 'resource': scan_id}
        response = requests.get(url, params=params)
        info = response.json()
        if 'positives' in info:
            if response.status_code == 204:
                raise Exception("to many api requests")
                return False
            elif response.status_code == 200:
                return info
            elif response.status_code == 403:
                raise Exception("this api key is forbiden. try again later")
                return False
            elif response.status_code == 404:
                return False
            else:
                return False
        else:
            return False