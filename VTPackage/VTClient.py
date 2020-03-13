import requests


class VTClient:
    def __init__(self,apiKey):
        self.apiKey=apiKey

    def get_url_report(self,URL):
        try:
            requestURL = f'https://www.virustotal.com/vtapi/v2/url/report?apikey={self.apiKey}&resource={URL}/'
            payload = {}
            headers = {}
            response = requests.request("GET", requestURL, headers=headers, data=payload)
            if response.status_code == 204:
                raise Exception("To much API requests")
            info = response.json()
            if info["response_code"] == 0:
                raise Exception(response["verbose_msg"])
            return info
        except Exception as e:
            print(e)
            raise Exception(e)
