#!usr/bin/kivy

import kivy
kivy.require('1.9.0')

from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.graphics.vertex_instructions import Line
from kivy.uix.camera import Camera
from kivy.uix.progressbar import ProgressBar
from kivy.properties import NumericProperty, AliasProperty
from kivy.core.audio import Sound, SoundLoader

import math
from math import sin, cos, pi

import time
from time import strftime

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

import winsound, sys


# miscellaneous components that were easier to implement in kv language rather than Python
# misc = '''
# #: import math math

# [SpeedometerNumber@Label]
#   text: str(ctx.i)
#   pos: ((175 + 147 * math.sin(math.pi / 6 * (ctx.i - 35))), (175 + 147 * math.cos(math.pi / 6 * (ctx.i - 35))))
#   font_size: 20
#   color: (1, 1, 1)
# '''

# allows you to switch between screens with a touch of a button rather than swiping
sidebar = '''
    SideBar
        name: 'sidebar'
        BoxLayout:
            orientation: 'vertical'
            size: (80, 480)
            pos: (720, 0)
            Button:
                text: 'Home'
                on_release: app.root.load_slide(app.root.slides[0])
            Button:
                text: 'Music'
                on_release: app.root.load_slide(app.root.slides[1])
            Button:
                text: 'Rearview'
                on_release: app.root.load_slide(app.root.slides[2])
'''

# home button 
##### DO I REALLY NEED A HOME BUTTON?? #####
##### MAYBE REPLACE WITH ANOTHER BUTTON?? #####
# K: Good to have home button if no physical button. #
homebutton = '''
    HomeButton
        name: 'homebutton'
        BoxLayout:
            pos: (720, 0)
            size: (80, 80)
            Button:
                text: 'Home'
                ## create home button image / find a cool looking home button image ##
'''

homescr = '''
HomeScreen
    name: 'homescreen'
    FloatLayout:
        size: (720, 480)
        pos: (0, 0)
        Speedometer:
            size_hint: (.6, .72)
            pos: (144, 0)
        ClockDisplay:
            size_hint: (0.6, 0.26)
            pos: (144, 360)
            font_size: 20
            halign: 'center'
        # Button:
        #   text: 'battery level'
        #   # replace with actual battery level widget
        #   size_hint: (0.18, 0.55)
        #   pos: (0, 0)
        # Button:
        #   text: 'est. range'
        #   # replace with actual estimated range widget
        #   size_hint: (0.18, 0.15)
        #   pos: (0, 272.75)
'''

musicscr = '''
MusicScreen
    name: 'musicscreen'
    id: music

    # button options
    BoxLayout:
        orientation: 'horizontal'
        pos: (0, 0)
        size: (720, 80)
        Button:
            text: 'menu'
        Button:
            text: '|<<'
        ToggleButton:
            id: play_pause
            text: 'play/pause'
            on_press: root.play_pause()
        Button:
            text: '>>|'
        Button:
            text: 'volume'

    # text display
    BoxLayout:
        orientation: 'vertical'
        pos: (0, 180)           # 100 above bottom buttons
        size: (720, 300)        # until right buttons to the top
        Label: 
            text: 'Title'
        Label: 
            text: 'Artist'
        Label: 
            text: 'Album'
        ProgressBar:
            id: progbar
            # text: 'Playback Bar'
            # height: '48dp'      
            value: music.get_pos() 
            max: music.get_len() 

'''

rearscr = '''
RearviewScreen
    name: 'rearviewscreen'
    BoxLayout:
        orientation: 'vertical'
        size: (720, 480)
        pos: (0, 40)
        Camera:
            id: cam
            play: True
            resolution: (640, 480)
    FloatLayout:
        Button:
            id: on_off
            text: 'On/Off'
            on_press: cam.play = not cam.play
            # size_hint_y: None
            # height: '48dp'
            pos: (0,0)
            size: (720, 40)

'''

# Screens and the different Widgets on them
class HomeScreen(Widget):
    pass


class ClockDisplay(Label):
    def __init__(self, **kwargs):
        super(ClockDisplay, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = time.strftime("%H:%M:%S\n%a, %b %d, %Y")


class Speedometer(Widget):
    def __init__(self, **kwargs):
        super(Speedometer, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.01)

    def update(self, *args):
        angleBetweenNumbers = 270 / 7
        centerX = 360
        centerY = 200
        numbersCenteredX = centerX - 50
        numbersCenteredY = centerY - 50
        speed = 0
        self.drawBase(centerX, centerY, numbersCenteredX, numbersCenteredY, angleBetweenNumbers)
        self.drawNeedle(centerX, centerY, speed, angleBetweenNumbers)

    # def on_touch_down(self, touch):
    #   print("x = %d, y = %d", touch.x, touch.y)

    def drawBase(self, centerX, centerY, numbersCenteredX, numbersCenteredY, angleBetweenNumbers):
        radius = 175
        with self.canvas:
            Color(1, 1, 1)
            Line(width = 5, circle = (centerX, centerY, radius))
            # when drawing Speedometer numbers, actual center of circle is at (310, 150)

            for i in range(0, 8):
                SpeedometerNumber().draw(i, numbersCenteredX, numbersCenteredY, angleBetweenNumbers)

    def drawNeedle(self, centerX, centerY, speed, angleBetweenNumbers):
        with self.canvas:
            SpeedometerNeedle().draw(centerX, centerY, speed, angleBetweenNumbers)


class SpeedometerNumber(Label):
    def __init__(self, **kwargs):
        super(SpeedometerNumber, self).__init__(**kwargs)

    def draw(self, i, centerX, centerY, angleBetweenNumbers):
        self.text = str(i * 10)
        #self.pos = (310 + 150 * math.cos(38.5714 * (i - 35))), (150 + 150 * math.sin(38.5714 * (i - 35))) ## fix this mudda fuck
        # center of circle is at (310, 150)
        newRadius = 150
        x = centerX + newRadius * math.cos(math.radians(-135 - (i * angleBetweenNumbers)))
        y = centerY + newRadius * math.sin(math.radians(-135 - (i * angleBetweenNumbers)))
        self.pos = (x, y)
        self.font_size = 20
        self.color = (1, 1, 1)


class SpeedometerNeedle(Widget):
    def __init__(self, **kwargs):
        super(SpeedometerNeedle, self).__init__(**kwargs)

    def draw(self, centerX, centerY, speed, angleBetweenNumbers):
        lengthOfNeedle = 140
        endX = centerX + lengthOfNeedle * math.cos(math.radians(-135 - (speed / 10 * angleBetweenNumbers)))
        endY = centerY + lengthOfNeedle * math.sin(math.radians(-135 - (speed / 10 * angleBetweenNumbers)))
        
        Color(1, 0, 0, 0.5, mode = 'rgba')
        Line(width = 2, points = (centerX, centerY, endX, endY))


class MusicScreen(Widget):
    def __init__(self, **kwargs):
        super(MusicScreen, self).__init__(**kwargs)
        # self.music = Music()
        self.music = SoundLoader.load('C:\\Users\\Karen\\Downloads\\music to USB\\Zelda - Song of Storms (Deon Custom Remix).mp3')
        self.position = self.music.get_pos()
        self.len = self.music.length

        # self.pb = ProgressBar(max=self.len)
        # self.pb.value = 50
        # self.update()
        # pb.value = self.position
    def get_len(self):
        return self.len

    def get_pos(self):
        return self.pos

    def play_pause(self):
        pos = 0
        if self.music.state == 'stop':
            # self.play_pause.text = 'Pause'
            self.music.seek(self.position)
            print(self.position)
            self.music.play()
        else:
            # self.text = 'Play'
            pos = self.music.get_pos()
            print(pos)
            self.music.stop()
            print(pos)
        self.position = pos

    # def update(self):
    #     while self.music.state == 'play':
    #         self.pb.value = self.music.position
    #         print self.pb.value

    
class ProgressBar(Widget):
    '''Class for creating a progress bar widget.

    See module documentation for more details.
    '''

    def __init__(self, **kwargs):
        self._value = 0.
        super(ProgressBar, self).__init__(**kwargs)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        value = max(0, min(self.max, value))
        if value != self._value:
            self._value = value
            return True

    value = AliasProperty(_get_value, _set_value)
    '''Current value used for the slider.

    :attr:`value` is an :class:`~kivy.properties.AliasProperty` that
    returns the value of the progress bar. If the value is < 0 or >
    :attr:`max`, it will be normalized to those boundaries.

    .. versionchanged:: 1.6.0
        The value is now limited to between 0 and :attr:`max`.
    '''

    def get_norm_value(self):
        d = self.max
        if d == 0:
            return 0
        return self.value / float(d)

    def set_norm_value(self, value):
        self.value = value * self.max

    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'max'))
    '''Normalized value inside the range 0-1::

        >>> pb = ProgressBar(value=50, max=100)
        >>> pb.value
        50
        >>> slider.value_normalized
        0.5

    :attr:`value_normalized` is an :class:`~kivy.properties.AliasProperty`.
    '''

    max = NumericProperty(100.)
    '''Maximum value allowed for :attr:`value`.

    :attr:`max` is a :class:`~kivy.properties.NumericProperty` and defaults to
    100.
    '''


class RearviewScreen(Widget):
    pass           
    


# Universal companents and widgets across all screens
class SideBar(Widget):
    pass


class HomeButton(Widget):
    pass


class TouchScreenApp(App):
    def build(self):
        # set the window size
        Window.size = (800, 480)

        # load miscellaneous stuff that's in kv language
        # Builder.load_string(misc)

        # setup the Carousel such that we can swipe between screens
        carousel = Carousel(direction='right')

        # add the homescreen widget to the carousel with the sidebar
        homescreen = Builder.load_string(homescr + sidebar)
        carousel.add_widget(homescreen)

        # add the musicscreen widget to the carousel with the sidebar
        musicscreen = Builder.load_string(musicscr + sidebar)
        carousel.add_widget(musicscreen)
        
        # add the rearview camera screen widget to the carousel with the sidebar
        rearviewscreen = Builder.load_string(rearscr + sidebar)
        carousel.add_widget(rearviewscreen)

        return carousel

if __name__ == '__main__':
    TouchScreenApp().run()