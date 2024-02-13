import requests
from task_3.ManagersPrototype import ManagersPrototype
from task_3.http.DTObject import DTObject


class HttpServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.api_token = self.registration_on_server()
        self.manager = ManagersPrototype.get_manager()

    def registration_on_server(self):
        return requests.get(f"{self.host}:{self.port}/register").json()

    def load_data(self):
        try:
            data = requests.get(f"{self.host}:{self.port}/load?API_TOKEN={self.api_token}").json()
        except:
            data = None
        return data

    def save_to_server(self, tasks, history):
        dto = DTObject(tasks, history)
        requests.request("POST", f"{self.host}:{self.port}/save?API_TOKEN={self.api_token}", json=dto.data)
