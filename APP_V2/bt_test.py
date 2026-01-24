from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
import threading

from bt_server import bluetooth_server

class TestApp(App):
    def build(self):
        self.btn = Button(text="Kivy Button", font_size=40)
        self.btn.bind(on_press=self.on_button_press)

        # Start Bluetooth thread
        threading.Thread(
            target=bluetooth_server,
            args=(self.on_bt_command,),
            daemon=True
        ).start()

        return self.btn

    def on_button_press(self, instance):
        print("🟢 Kivy button pressed")

    def on_bt_command(self, command):
        if command == "BTN1":
            # UI updates MUST happen on main thread
            Clock.schedule_once(self.fake_button_press)

    def fake_button_press(self, dt):
        print("🟢 BTN1 received → triggering Kivy logic")
        self.on_button_press(None)

if __name__ == "__main__":
    TestApp().run()
