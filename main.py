# Zapisz ten plik jako: main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import time, base64, random, math

# --- KRYPTOGRAFIA ---
# UWAGA: Jeśli budowanie APK się nie uda, usuń importy kryptografii
# Pydroid czasem ma problem ze skompilowaniem tej biblioteki na telefonie.
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

class WeraCore:
    def __init__(self, psk=b"InzynierPawel83"):
        if CRYPTO_AVAILABLE:
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'apk_build', iterations=100000)
            key = base64.urlsafe_b64encode(kdf.derive(psk))
            self.cipher = Fernet(key)
        else:
            self.cipher = None
            
    def encrypt(self, text): 
        if self.cipher: return self.cipher.encrypt(text.encode())
        return b"[BRAK SZYFROWANIA - TRYB LITE]"

class WeraInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        self.core = WeraCore()
        self.current_temp_val = 40.0
        self.time_counter = 0 
        
        self.add_widget(Label(text="[ WERA 1.8 - MOBILE APP ]", size_hint_y=None, height=40, color=(0, 1, 0.5, 1), bold=True))
        
        self.tele_box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=5)
        self.live_load = Label(text="OBCIĄŻENIE: 0%", font_size='18sp', color=(1, 0.4, 0.4, 1))
        self.live_temp = Label(text="TEMP. RDZENIA: 40.0°C", font_size='18sp', color=(1, 0.9, 0, 1))
        self.live_status = Label(text="TRYB: MANUALNY", font_size='14sp', color=(0.5, 0.5, 0.5, 1), bold=True)
        
        self.tele_box.add_widget(self.live_load)
        self.tele_box.add_widget(self.live_temp)
        self.tele_box.add_widget(self.live_status)
        self.add_widget(self.tele_box)

        self.power_bar = ProgressBar(max=100, value=80, size_hint_y=None, height=20)
        self.add_widget(self.power_bar)

        self.btn_auto = ToggleButton(text="AKTYWUJ AUTOPILOTA", size_hint_y=None, height=60, 
                                     background_color=(0, 0.5, 1, 1), font_size='16sp', bold=True)
        self.add_widget(self.btn_auto)

        scroll = ScrollView(size_hint=(1, 1))
        self.ctrl_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=40, padding=[10, 20])
        self.ctrl_layout.bind(minimum_height=self.ctrl_layout.setter('height'))

        self.sliders = {}
        params = [("Moc", 0, 100, 80, "%"), ("Chłodzenie", 0, 100, 70, "%"), ("Częstotliwość", 0, 500, 300, "Hz")]

        for p_name, p_min, p_max, p_start, p_unit in params:
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=5)
            lbl = Label(text=f"{p_name.upper()}: {p_start}{p_unit}", bold=True)
            sld = Slider(min=p_min, max=p_max, value=p_start, size_hint_y=None, height=60)
            def update_label(instance, val, l=lbl, n=p_name, u=p_unit):
                l.text = f"{n.upper()}: {int(val)}{u}"
            sld.bind(value=update_label)
            self.sliders[p_name] = sld
            box.add_widget(lbl); box.add_widget(sld)
            self.ctrl_layout.add_widget(box)

        scroll.add_widget(self.ctrl_layout)
        self.add_widget(scroll)
        
        self.log_area = Label(text="Gotowy do działania.", size_hint_y=None, height=30)
        self.add_widget(self.log_area)

        Clock.schedule_interval(self.update_telemetry, 1.0)

    def update_telemetry(self, dt):
        if self.btn_auto.state == 'down':
            self.live_status.text = ">>> AUTOPILOT <<<"
            self.live_status.color = (0, 1, 0, 1)
            self.time_counter += 0.2
            self.sliders["Moc"].value = 60 + (30 * math.sin(self.time_counter))
            self.sliders["Częstotliwość"].value = 300 + (100 * math.cos(self.time_counter * 0.3))
        else:
            self.live_status.text = "TRYB: MANUALNY"
            self.live_status.color = (0.5, 0.5, 1, 1)

        p = self.sliders["Moc"].value
        c = self.sliders["Chłodzenie"].value
        f = self.sliders["Częstotliwość"].value
        
        target = 30 + (p * 0.6) + (max(0, f-300)*0.15) - (c * 0.35)
        self.current_temp_val += (target - self.current_temp_val) * 0.1
        self.live_temp.text = f"TEMP. RDZENIA: {self.current_temp_val:.1f}°C"
        
        if self.current_temp_val > 90: self.live_temp.color = (1, 0, 0, 1)
        else: self.live_temp.color = (0, 1, 0, 1)
        
        self.power_bar.value = p
        self.live_load.text = f"OBCIĄŻENIE: {int(min(100, max(0, p + random.randint(-5, 5))))}%"

class WeraApp(App):
    def build(self): return WeraInterface()

if __name__ == "__main__":
    WeraApp().run()
