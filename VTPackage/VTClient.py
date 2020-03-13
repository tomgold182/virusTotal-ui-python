import requests


class VTClient:
    def __init__(self,apiKey):
        self.apiKey=apiKey

    def get_url_report(self,URL):
        try:
            requestURL = f'https://www.virustotal.com/vtapi/v2/url/report?apikey={self.apiKey}&resource={URL}/'
            payload = {}
            headers = {}
            response = requests.request("GET", requestURL, headers=headers, data=payload).json()
            if response["response_code"] == 0:
                raise Exception(response["verbose_msg"])
            return response
        except Exception as e:
            print(e)
            raise Exception(e)
