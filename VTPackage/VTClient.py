import requests


class VTClient:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.baseURI = 'https://www.virustotal.com/vtapi/v2/'  # We could have been just concating the url to each request, but we want our code to be neat & re-usable

    def is_API_key_valid(self):
        try:
            requestURL = f'{self.baseURI}url/report?apikey={self.apiKey}&resource=www.google.com'
            payload = {}
            headers = {}
            response = requests.request("GET", requestURL, headers=headers, data=payload)
            if response.status_code == 403:
                return False
            else:
                return True
        except Exception as e:
            errMessage = f'Error while trying to check the API key:{e}'  # Instead of writing to error string twice, we are writing it once and using it twice.
            print(errMessage)
            raise Exception(errMessage)

    def get_url_report(self, URL):
        try:
            requestURL = f'{self.baseURI}url/report?apikey={self.apiKey}&resource={URL}/'
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
            errMessage = f'Error while trying to get an URL report:{e}'  # Instead of writing to error string twice, we are writing it once and using it twice.
            print(errMessage)
            raise Exception(errMessage)

    def get_ip_report(self, ipAddress):
        try:
            requestURL = f'{self.baseURI}ip-address/report?apikey={self.apiKey}&ip={ipAddress}'
            payload = {}
            headers = {}
            response = requests.request("GET", requestURL, headers=headers, data=payload)
            if response.status_code == 204:
                raise Exception("To much API requests")
            info = response.json()
            if info["response_code"] == 0 or info["response_code"] == -1:
                raise Exception(info["verbose_msg"])
            return info

        except Exception as e:
            errMessage = f'Error while trying to get an IP report:{e}'
            print(errMessage)
            raise Exception(errMessage)

    def scan_file(self, filePath):
        try:
            requestUrl = f'{self.baseURI}file/scan'
            params = {'apikey': self.apiKey}
            files = {
                'file': (filePath, open(filePath, 'rb'))
            }
            response = requests.post(requestUrl, files=files, params=params)
            info = response.json()
            if info["response_code"] == 1:
                return info['scan_id']

        except Exception as e:
            errMessage = f'Error while trying to scan file:{e}'
            print(errMessage)
            raise Exception(errMessage)

    def get_file_report(self, scan_ID):
        try:
            requestUrl = f'{self.baseURI}file/report'
            params = {'apikey': self.apiKey, 'resource': scan_ID}
            resopnse = requests.get(requestUrl, params=params)
            if resopnse.status_code == 204:
                raise Exception("To much API requests. Please wait a minute and try again")
            if resopnse.status_code == 200:
                return resopnse.json()
            else:
                print(resopnse.json())
        except Exception as e:
            errMessage = f'Error while trying to get scan report:{e}'
            print(errMessage)
            raise Exception(errMessage)
