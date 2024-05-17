import pyo
import numpy as np
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from pyo import *
from kivy.core. window import Window
from kivy.lang import Builder
from kivymd. app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd. uix. dialog import MDDialog
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager, Screen
import sounddevice as sd

KV = '''
WindowManager:
    MainWindow:
    Screen_2:
    Screen_3:
    
<MainWindow>:
    name: "main"
    FloatLayout:
        orientation: 'vertical'
        MDRaisedButton:
            text: "Обработать аудиофайл"
            pos_hint: {'center_x':.5, 'center_y':.6}
            on_release:
                app.root.current = "second"
                root.manager.transition.direction = "left"
        MDRaisedButton:
            text: "Записать и обработать голос"
            pos_hint: {'center_x':.5, 'center_y':.5}
            on_release:
                app.root.current = "third"
                root.manager.transition.direction = "left"
                app.initial2()  
<Screen_2>:
    name: "second"
    BoxLayout:
        orientation: 'vertical'
        pos_hint:{'center_x':.5, 'center_y':1.4}
        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            MDRaisedButton:
                text: "<<--"
                on_release:
                    app.root.current = "main"
                    root.manager.transition. direction = "right"
            MDRoundFlatIconButton:
                id: b1
                text: "Выбрать аудиофайл"
                icon: "folder"
                on_release: app.file_manager_open2()
            MDRaisedButton:
                id: b2
                text: "Слушать"
                on_release: app.start_stop_playing_file(),root.change_title_b2()
            MDRoundFlatIconButton:
                id: b3
                text: "Выбрать папку для записи"
                icon: "folder"
                on_release: app.file_manager_open()
            MDRaisedButton:
                id:b4
                text: "Запись"
                on_release: app.start_stop_record(), root.change_title_b4()
            MDRaisedButton:
                id: b5
                text: "Запись c начала"
                on_release: app.start_stop_playing_and_record(), root.change_title_b5()
    BoxLayoutSliders:
        orientation: 'horizontal'
        padding: 30
        spacing: 10
        size_hint: 1.0, 0.9
        Slider:
            id: s_harmonizer
            orientation: 'vertical'
            value_track: True
            value_track_color: 1, 0, 0, 1
            min: -24
            max: 24
            step: 1
            value: 0
            on_touch_move: app.slider1(s_harmonizer.value)
        Slider:
            id: s_delay
            orientation: 'vertical'
            value_track: True
            value_track_color: 1, 0, 0, 1
            min: 0
            max: 40
            step: 1
            value: 0
            on_touch_move: app.slider2(s_delay.value)
        Slider:
            id: s_echo
            orientation: 'vertical'
            value_track: True
            value_track_color: 1, 0, 0, 1
            min: 0
            max: 40
            step: 1
            value: 0
            on_touch_move: app.slider3(s_echo.value)
        Slider:
            id: s_voices
            orientation: 'vertical'
            value_track: True
            value_track_color: 1, 0, 0, 1
            min: 0
            max: 8
            step: 1
            value: 0
            on_touch_move: app.slider4(s_voices.value)
        Slider:
            id: s_freqshift
            orientation: 'vertical'
            value_track: True
            value_track_color: 1, 0, 0, 1
            min: -20
            max: 20
            step: 1
            value: 0
            on_touch_move: app.slider5(s_freqshift.value) 
<Screen_3>:
    name: "third"
    BoxLayout:
        orientation: 'vertical'
        spacing:10
        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            size_hint: 1.0, 0.1
            MDRaisedButton:
                text: "<<--"
                on_release: 
                    app.root.current = "main"
                    root.manager.transition. direction = "right"
            MDRaisedButton:
                id: b23
                icon: "folder"
                text: "Слышать себя"
                on_release: app.modus_x_2(), root.change_title_b23()
            MDRaisedButton:
                id: b33
                icon: "folder"
                text: "Запись"
                on_release: app.start_stop_record(), root.change_title_b33()
            MDRaisedButton:
                id: b34
                icon: "folder"
                text: "Сбросить эффекты"
                on_release: app.set_default(), root.set_default()
            MDRaisedButton:
                id: b35
                icon: "folder"
                text: "Включить визуализацию"
                on_release: root.start_progress(), root.change_title_b35()
            MDRoundFlatIconButton:
                text: "Выбрать папку или файл"
                icon: "folder"
                on_release: app.file_manager_open() 
        BoxLayout:
            padding: 10
            size_hint: 1.0, 0.05
            MDProgressBar:
                id: progress
                orientation: "horizontal"       
        BoxLayoutSliders:
            orientation: 'horizontal'
            padding: 30
            spacing: 10
            size_hint: 1.0, 0.7
            Slider:
                id: s_harmonizer
                orientation: 'vertical'
                value_track: True
                value_track_color: 1, 0, 0, 1
                min: -24
                max: 24
                step: 1
                value: 0
                on_touch_move: app.slider1(s_harmonizer.value)
            Slider:
                id: s_delay
                orientation: 'vertical'
                value_track: True
                value_track_color: 1, 0, 0, 1
                min: 0
                max: 40
                step: 1
                value: 0
                on_touch_move: app.slider2(s_delay.value)
            Slider:
                id: s_echo
                orientation: 'vertical'
                value_track: True
                value_track_color: 1, 0, 0, 1
                min: 0
                max: 40
                step: 1
                value: 0
                on_touch_move: app.slider3(s_echo.value)
            Slider:
                id: s_voices
                orientation: 'vertical'
                value_track: True
                value_track_color: 1, 0, 0, 1
                min: 0
                max: 8
                step: 1
                value: 0
                on_touch_move: app.slider4(s_voices.value)
            Slider:
                id: s_freqshift
                orientation: 'vertical'
                value_track: True
                value_track_color: 1, 0, 0, 1
                min: -20
                max: 20
                step: 1
                value: 0
                on_touch_move: app.slider5(s_freqshift.value) 
        BoxLayoutLabels:
            padding: 30
            orientation: 'horizontal'
            spacing: 10
            size_hint: 1.0, 0.1
            Label:
                text: "Гармонизатор"          
'''
def stop(pyoObject):
    clean = Clean_objects(0, pyoObject)
    clean.start()
class MainWindow (Screen):
    pass
# второй экран приложения
class Screen_2 (Screen):
    def change_title_b2(self):
        if self.ids["b2"].text == 'Слушать':
            self.ids["b2"].text = 'Остановить'
        else:
            self.ids["b2"].text = 'Слушать'
    def change_title_b4(self):
        if self.ids["b4"].text == 'Запись':
            self.ids["b4"].text = 'Остановить'
        else:
            self.ids["b4"].text = 'Запись'
    def change_title_b5(self):
        if self.ids["b5"].text == 'Запись с начала':
            self.ids["b5"].text = 'Остановить'
        else:
            self.ids["b5"].text = 'Запись с начала'
# третий экран приложения
class Screen_3 (Screen):
    def change_title_b23(self):
        if self.ids["b23"].text == 'Слышать себя':
            self.ids["b23"].text = 'Остановить'
        else:
            self.ids["b23"].text = 'Слышать себя'
    def change_title_b33(self):
        if self.ids["b33"].text == 'Запись':
            self.ids["b33"].text = 'Остановить'
        else:
            self.ids["b33"].text = 'Запись'

    def change_title_b35(self):
        if self.ids["b35"].text == 'Включить визуализацию':
            self.ids["b35"].text = 'Остановить'
        else:
            self.ids["b35"].text = 'Включить визуализацию'
    def set_default(self):
        self.ids['s_harmonizer'].value = 0
        self.ids['s_delay'].value = 0
        self.ids['s_voices'].value = 0
        self.ids['s_echo'].value = 0
        self.ids['s_freqshift'].value = 0
    def start_progress(self):
        while self.ids["b35"].text == 'Остановить':
            with sd.InputStream(callback=self.print_volume):
                sd.sleep(100)
    def print_volume(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        self.ids["progres"].value = int(volume_norm)
class BoxLayoutSliders(BoxLayout):
   pass
class BoxLayoutLabels(BoxLayout):
   pass

# менеджер экранов
class WindowManager (ScreenManager):
    pass

class MainApp (MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,  # function called when the user reaches directory tree root
            select_path=self.select_path,  # function called when selecting a file/directory
        )
        self.file_manager2 = MDFileManager(
            exit_manager=self.exit_manager2,  # function called when the user reaches directory tree root
            select_path=self.select_path2,  # function called when selecting a file/directory
        )
        self.s = pyo.Server(duplex=1)
        self.s.boot()
        self.s.start()
        self.path_playing_file = ''
        self.path_recording_file = ''
        self.record = 0
        self.a = 0
        self.hr = 0
        self.d = 0
        self.rev = 0
        self.chor = 0
        self.sh = 0
        self.dialog= None
        self.rec = 0
        self.flag_b3 = 0
        self.flag_record=0
        self.flag_playing=0

    def build (self):
        return Builder.load_string(KV)
    def initial2(self):
        self.a = Input()
        self.hr = Harmonizer(self.a)
        self.hr.setTranspo(0)
        self.d = Delay(self.hr, feedback=0)
        self.d.setFeedback(0)
        self.rev = Freeverb(self.d, size=0, bal=0.5)
        self.chor = Chorus(self.rev, depth=[1.5, 1.6], feedback=0.5, bal=0.5)
        self.sh = FreqShift(self.chor)
        self.sh.setShift(0)
    def modus_x_2(self):
        if self.flag_b3==0:
            self.sh.play().out()
            self.flag_b3=1
        else:
            self.sh.play()
            self.flag_b3 = 0
    def start_stop_playing_file(self):
        if self.path_playing_file == '':
            self.show_alert_dialog()
            return
        if self.flag_playing==0:
            self.a = pyo.SfPlayer(path=self.path_playing_file, speed=[1, 1])
            self.hr = Harmonizer(self.a)
            self.hr.setTranspo(0)
            self.d = Delay(self.hr, feedback=0)
            self.d.setFeedback(0)
            self.rev = Freeverb(self.d, size=0, bal=0.5)
            self.chor = Chorus(self.rev, depth=[1.5, 1.6], feedback=0.5, bal=0.5)
            self.sh = FreqShift(self.chor).out()
            self.sh.setShift(0)
            self.flag_playing=1
        else:
            stop(self.a)
            self.flag_playing=0
    def start_stop_record(self):
        if self.path_recording_file == '':
            self.show_alert_dialog()
            return
        if self.flag_record==0:
            folders = self.path_recording_file.split('/')
            if '.' not in folders[len(folders)-1]:
                self.path_recording_file=self.path_recording_file+'/record.wav'
            self.rec = Record(self.sh, filename=self.path_recording_file, fileformat=0, sampletype=1)
            self.flag_record=1
        else:
            clean = Clean_objects(0, self.rec)
            clean.start()
            self.flag_record = 0

    def start_stop_playing_and_record(self):
        if self.path_playing_file == '' or self.path_recording_file=='':
            self.show_alert_dialog()
            return
        self.start_stop_playing_file()
        self.start_stop_record()
    def set_default(self):
        self.hr.setTranspo(0)
        self.d.setFeedback(0)
        self.rev.setSize(0)
        self.chor.setFeedback(0)
        self.sh.setShift(0)

    def playing_file(self):
        if self.path_playing_file == '':
            self.show_alert_dialog()
            return
        self.a = pyo.SfPlayer(path=self.path_playing_file, speed=[1, 1])
        self.hr = Harmonizer(self.a)
        self.hr.setTranspo(0)
        self.d = Delay(self.hr, feedback=0)
        self.d.setFeedback(0)
        self.rev = Freeverb(self.d, size=0, bal=0.5)
        self.chor = Chorus(self.rev, depth=[1.5, 1.6], feedback=0.5, bal=0.5)
        self.sh = FreqShift(self.chor).out()
        self.sh.setShift(0)
    def slider1(self, value):
        self.hr.setTranspo(value)
    def slider2(self, value):
        self.d.setFeedback(value/40)

    def slider3(self, value):
        self.rev.setSize(value/40)

    def slider4(self, value):
        self.chor.setFeedback(value/20 + 0.5)

    def slider5(self, value):
        self.sh.setShift(value*10)
    def file_manager_open (self):
        self.file_manager.show ("/") # вывода менеджерана экран
        self.manager_open = True
    def file_manager_open2 (self):
        self.file_manager2.show ("/") # вывода менеджерана экран
        self.manager_open = True
    def show_alert_dialog(self):
        self.dialog = MDDialog(text = "Сначала выберите файл", buttons = [MDFlatButton(text = "ОК", on_release=lambda _: self.dialog.dismiss())])
        self.dialog.open()
    def select_path (self, path):
        '''Будет вызвана, когда вы нажмете на имя файла или кнопка выбора каталога.
        :type path: str;
        :param path: путь к выбранному каталогу или файлу;'''
        print("Выбран файл", path)
        self.exit_manager()
        toast(path)
        self.path_recording_file=path

    def select_path2(self, path):
        '''Будет вызвана, когда вы нажмете на имя файла или кнопка выбора каталога.
        :type path: str;
        :param path: путь к выбранному каталогу или файлу;'''
        print("Выбран файл", path)
        self.exit_manager2()
        toast(path)
        self.path_playing_file = path
    def exit_manager (self, *args):
        '''Вызывается, когда пользователь достигает
                  корня дерева каталогов.'''
        self.manager_open = False
        self.file_manager.close ()
    def exit_manager2 (self, *args):
        self.manager_open = False
        self.file_manager2.close ()
    def events (self, instance, keyboard, keycode, text, modifiers):
        '''Вызывается при нажатии кнопок на мобильном устройстве.'''
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back ()
        return True
MainApp().run()
