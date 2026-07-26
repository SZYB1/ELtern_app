# eltern_app_android.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
import json, os

Window.clearcolor = (0.09, 0.09, 0.10, 1)
DATA_FILE = "timeguard_data.json"

class CleanParentAndroidApp(App):
    def build(self):
        self.title = "TimeGuard - Eltern (Android)"
        self.root_layout = BoxLayout(orientation='vertical')
        self.show_login_screen()
        return self.root_layout

    def show_login_screen(self):
        self.root_layout.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Label(text="KONTROLLE (MOBILE)", font_size='24sp', bold=True, color=(1, 1, 1, 1), size_hint_y=0.2))
        layout.add_widget(Label(text="Code eingeben:", font_size='15sp', color=(0.6, 0.6, 0.65, 1), size_hint_y=0.15))
        self.code_input = TextInput(text="", hint_text="z.B. A4F-9K2", multiline=False, font_size='18sp', background_color=(0.18, 0.18, 0.20, 1), foreground_color=(1, 1, 1, 1), size_hint_y=0.15)
        layout.add_widget(self.code_input)
        connect_btn = Button(text="VERBINDEN", font_size='16sp', bold=True, background_normal='', background_color=(0.0, 0.48, 1.0, 1), color=(1, 1, 1, 1), size_hint_y=0.18)
        connect_btn.bind(on_press=lambda x: self.show_control_panel())
        layout.add_widget(connect_btn)
        self.root_layout.add_widget(layout)

    def show_control_panel(self):
        self.root_layout.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=12, size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        main_layout.add_widget(Label(text="APPLE-STYLE ÜBERSICHT", font_size='20sp', bold=True, color=(1, 1, 1, 1), size_hint_y=None, height=40))
        self.status_label = Label(text="Nutzung: 0h 0m", font_size='15sp', color=(0.7, 0.7, 0.75, 1), size_hint_y=None, height=30)
        main_layout.add_widget(self.status_label)
        self.alert_label = Label(text="Keine Anfragen", font_size='14sp', color=(0.3, 0.6, 1.0, 1), size_hint_y=None, height=30)
        main_layout.add_widget(self.alert_label)
        
        box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        box.add_widget(Label(text="Limit (Min):", font_size='14sp', color=(0.8, 0.8, 0.85, 1)))
        self.limit_input = TextInput(text="120", multiline=False, input_filter='int', font_size='16sp', background_color=(0.18, 0.18, 0.20, 1), foreground_color=(1, 1, 1, 1))
        box.add_widget(self.limit_input)
        main_layout.add_widget(box)

        btn = Button(text="LIMIT SPEICHERN", font_size='14sp', bold=True, background_normal='', background_color=(0.0, 0.48, 1.0, 1), color=(1, 1, 1, 1), size_hint_y=None, height=45)
        btn.bind(on_press=self.save_data)
        main_layout.add_widget(btn)

        self.extra_btn = Button(text="+ 30 Min Extra-Zeit", font_size='14sp', bold=True, background_normal='', background_color=(0.2, 0.78, 0.35, 1), color=(1, 1, 1, 1), size_hint_y=None, height=45)
        self.extra_btn.bind(on_press=self.grant_extra_time)
        main_layout.add_widget(self.extra_btn)

        self.lock_btn = Button(text="🔒 GERÄT SPERREN", font_size='14sp', bold=True, background_normal='', background_color=(1, 0.23, 0.18, 1), color=(1, 1, 1, 1), size_hint_y=None, height=45)
        self.lock_btn.bind(on_press=self.toggle_lock)
        main_layout.add_widget(self.lock_btn)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(main_layout)
        self.root_layout.add_widget(scroll)
        Clock.schedule_interval(lambda dt: self.load_data(), 2)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    used, maximum = data.get("total_seconds", 0), data.get("max_daily_seconds", 7200)
                    self.status_label.text = f"Nutzung: {used//3600}h {(used%3600)//60}m / Limit: {maximum//3600}h {(maximum%3600)//60}m"
                    self.lock_btn.text = "🔓 GERÄT ENTSPERREN" if data.get("is_locked", False) else "🔒 GERÄT SPERREN"
                    self.alert_label.text = "⚠️ Kind bittet um Mehr Zeit!" if data.get("request_extra_time", False) else "Keine neuen Anfragen"
            except: pass

    def save_data(self, instance):
        try:
            new_max = int(self.limit_input.text) * 60
            data = {"total_seconds": 0, "max_daily_seconds": 7200, "request_extra_time": False, "is_locked": False}
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f: data = json.load(f)
            data["max_daily_seconds"] = new_max
            with open(DATA_FILE, "w") as f: json.dump(data, f)
        except: pass

    def grant_extra_time(self, instance):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f: data = json.load(f)
                data["max_daily_seconds"] += 1800
                data["request_extra_time"] = False
                with open(DATA_FILE, "w") as f: json.dump(data, f)
        except: pass

    def toggle_lock(self, instance):
        try:
            data = {"total_seconds": 0, "max_daily_seconds": 7200, "request_extra_time": False, "is_locked": False}
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f: data = json.load(f)
            data["is_locked"] = not data.get("is_locked", False)
            with open(DATA_FILE, "w") as f: json.dump(data, f)
        except: pass

if __name__ == '__main__': CleanParentAndroidApp().run()
