from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import subprocess
import os
import signal
import requests



BASE_URL = "Cant share this URL. Top Secret!" 

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

# print(read_data("CommandH"))

# if read_data("CommandH") is not None:
#     write_data("CommandH", "None")

# print(read_data("CommandH"))

write_data("CommandH", "None")

class Kirshi_MitraApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        grid = GridLayout(
            cols=3,
            rows=2,
            spacing=10,
            size_hint_y=0.8
        )

        Clock.schedule_interval(self.get_command, 1)
    
        self.btn1 = Button(text="Weed Deetection")
        self.btn2 = Button(text="Weed Visual Slideshow")
        self.btn3 = Button(text="Weed Report")
        self.btn4 = Button(text="Disease Detection")
        self.btn5 = Button(text="Disease Slideshow")
        self.btn6 = Button(text="FPV Driving")

        self.btn1.bind(on_press=self.btn1_action)
        self.btn2.bind(on_press=self.btn2_action)
        self.btn3.bind(on_press=self.btn3_action)
        self.btn4.bind(on_press=self.btn4_action)
        self.btn5.bind(on_press=self.btn5_action)
        self.btn6.bind(on_press=self.btn6_action)

        grid.add_widget(self.btn1)
        grid.add_widget(self.btn2)
        grid.add_widget(self.btn3)
        grid.add_widget(self.btn4)
        grid.add_widget(self.btn5)
        grid.add_widget(self.btn6)

        self.btn7 = Button(
            text="Kill Current Process",
            size_hint_y=0.2
        )
        self.btn7.bind(on_press=self.btn7_action)

        root.add_widget(grid)
        root.add_widget(self.btn7)


        return root

    current_proc = None
    command = None
    def btn1_action(self, instance):
        print("BTN1 pressed")
        self.current_proc = subprocess.Popen([
            "xterm",
            "-hold",
            "-e",
            "//home//cypher//testvenv2//bin//python3 final3.py"
        ], 
            preexec_fn=os.setsid 
        )

    def btn2_action(self, instance):
        self.current_proc = subprocess.Popen([
            "xterm",
            "-hold",
            "-e",
            "//home//cypher//testvenv2//bin//python3 slideshow_weed.py"
        ], 
            preexec_fn=os.setsid 
        )


    def btn3_action(self, instance):
        print("Button 3 pressed")

    def btn5_action(self, instance):
        self.current_proc = subprocess.Popen([
            "xterm",
            "-hold",
            "-e",
            "//home//cypher//testvenv2//bin//python3 slideshow.py"
        ], 
            preexec_fn=os.setsid 
        )


    def btn6_action(self, instance):
        self.current_proc = subprocess.Popen([
            "xterm",
            "-hold",
            "-e",
            "//home//cypher//testvenv2//bin//python3 fpv_driving.py"
        ], 
            preexec_fn=os.setsid 
        )


    def btn4_action(self, instance):
        print("Button 6 pressed")

    def btn7_action(self, instance):
        if self.current_proc:
            os.killpg(self.current_proc.pid, signal.SIGKILL)
            self.current_proc = None

    def get_command(self,dt):
        self.command = read_data("CommandH")
        print(self.command)
        if self.command == "\"BTN1\"":
            self.btn1_action(self.btn1)
            write_data("CommandH","None")
        if self.command == "\"BTN2\"":
            self.btn2_action(self.btn2)
            write_data("CommandH","None")
        if self.command == "\"BTN3\"":
            self.btn3_action(self.btn3)
            write_data("CommandH","None")
        if self.command == "\"BTN4\"":
            self.btn4_action(self.btn4)
            write_data("CommandH","None")
        if self.command == "\"BTN5\"":
            self.btn5_action(self.btn5)
            write_data("CommandH","None")
        if self.command == "\"BTN6\"":
            self.btn6_action(self.btn6)
            write_data("CommandH","None")
        if self.command == "\"BTN7\"":
            self.btn7_action(self.btn7)
            write_data("CommandH","None")



if __name__ == "__main__":
    Kirshi_MitraApp().run()
