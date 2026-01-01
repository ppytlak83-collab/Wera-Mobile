[app]
# (1) Tytuł aplikacji na pulpicie
title = Wera 1.8
package.name = wera
package.domain = org.pawel

# (2) Kod źródłowy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (3) Wersja
version = 1.8.0

# (4) Wymagania (hydraulika) - TO JEST KLUCZOWE
requirements = python3,kivy==2.2.0,cryptography,plyer

# (5) Uprawnienia (żeby ekran nie gasł)
android.permissions = INTERNET,WAKE_LOCK

# (6) Ustawienia ekranu
orientation = portrait
fullscreen = 0

# (7) Konfiguracja Androida
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
