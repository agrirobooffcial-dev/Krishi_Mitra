from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label

import requests
BASE_URL = "https://appcommand-1997e-default-rtdb.firebaseio.com/" 

def read_data(path):
    url = f"{BASE_URL}{path}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to read data:", response.text)
        return None

def write_data(path, data):
    url = f"{BASE_URL}{path}.json"
    response = requests.put(url, json=data)
    if response.status_code != 200:
        print("Failed to write data:", response.text)


class MyApp(App):
    def build(self):
        self.label = Label(text="")
        Clock.schedule_interval(self.update, 1)
        return self.label

    def update(self, dt):
        self.label.text = str(read_data("CommandH"))

MyApp().run()