from Clients.Client import Client
import shodan

class shodanClient(Client):
    def __init__(self, apiKey):
        super().__init__(apiKey)
        self.api = shodan.Shodan(apiKey)


    def get_ip_report(self, IP):
        # Search Shodan
        response = self.api.host(IP)
        print(response)
        return response