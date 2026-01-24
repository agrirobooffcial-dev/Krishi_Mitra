from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import subprocess
import os
import signal

class Kirshi_MitraApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        # GridLayout: 3 columns, 2 rows (6 buttons)
        grid = GridLayout(
            cols=3,
            rows=2,
            spacing=10,
            size_hint_y=0.8
        )

        # ---- Buttons (separate instances) ----
        self.btn1 = Button(text="Weed Deetection")
        self.btn2 = Button(text="Weed Visual Slideshow")
        self.btn3 = Button(text="Button 3")
        self.btn4 = Button(text="Button 4")
        self.btn5 = Button(text="Button 5")
        self.btn6 = Button(text="Button 6")

        # ---- Bind functions (placeholders) ----
        self.btn1.bind(on_press=self.btn1_action)
        self.btn2.bind(on_press=self.btn2_action)
        self.btn3.bind(on_press=self.btn3_action)
        self.btn4.bind(on_press=self.btn4_action)
        self.btn5.bind(on_press=self.btn5_action)
        self.btn6.bind(on_press=self.btn6_action)

        # ---- Add to grid ----
        grid.add_widget(self.btn1)
        grid.add_widget(self.btn2)
        grid.add_widget(self.btn3)
        grid.add_widget(self.btn4)
        grid.add_widget(self.btn5)
        grid.add_widget(self.btn6)

        # ---- 7th Button (outside grid) ----
        self.btn7 = Button(
            text="Kill Current Process",
            size_hint_y=0.2
        )
        self.btn7.bind(on_press=self.btn7_action)

        # ---- Add layouts ----
        root.add_widget(grid)
        root.add_widget(self.btn7)

        return root

    # ---------- Button Functions ----------
    current_proc = None
    def btn1_action(self, instance):
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

    def btn4_action(self, instance):
        print("Button 4 pressed")

    def btn5_action(self, instance):
        print("Button 5 pressed")

    def btn6_action(self, instance):
        print("Button 6 pressed")

    def btn7_action(self, instance):
        if self.current_proc:
            os.killpg(self.current_proc.pid, signal.SIGKILL)
            self.current_proc = None


if __name__ == "__main__":
    Kirshi_MitraApp().run()
