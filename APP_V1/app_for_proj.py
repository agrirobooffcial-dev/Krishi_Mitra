#!/usr/bin/env python3
import subprocess
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout



class GridButtons(GridLayout):    
    def weed_detection(self, dt):
        self.process = subprocess.Popen([
            "lxterminal",
            "-e",
            "//home//cypher//testvenv2//bin//python3 final3.py"
        ])
    def weed_visual(self, dt):
        pass

    def weed_slideshow(self, dt):
        pass

    def get_leaves(self, dt):
        pass

    def ddetect(self, dt):
        pass

    def disease_slideshow(self, dt):
        pass

class KvAppProj(App):
    pass


if __name__ == '__main__':
    KvAppProj().run()