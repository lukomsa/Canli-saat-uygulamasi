import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import threading
import time
import winsound
import os
from datetime import datetime, timedelta

class AlarmClock:
    def __init__(self, master):
        self.master = master
        master.title("Gelişmiş Alarm Saati")

        self.default_alarm_sound = "alarm.wav"  # Varsayılan alarm sesi
        if not os.path.exists(self.default_alarm_sound):
            # Varsayılan alarm sesi yoksa, bir bip sesi oluştur
            winsound.Beep(500, 750)
        self.alarm_sound = self.default_alarm_sound
        self.alarm_thread = None
        self.alarm_active = False
        self.snooze_time = 5  # Erteleme süresi (dakika)

        self.time_display = tk.Label(master, text="", font=('Helvetica', 48), fg='red')
        self.time_display.pack()

        # Alarm zamanı girişi
        tk.Label(master, text="Alarm Zamanını Ayarla (HH:MM)").pack()
        self.alarm_time_var = tk.StringVar(master)
        self.alarm_entry = tk.Entry(master, textvariable=self.alarm_time_var, width=5)
        self.alarm_entry.pack()

        # Alarm butonları
        self.set_alarm_button = tk.Button(master, text="Alarmı Ayarla", command=self.set_alarm)
        self.set_alarm_button.pack()

        self.snooze_button = tk.Button(master, text="Ertele", command=self.snooze, state=tk.DISABLED)
        self.snooze_button.pack()

        self.stop_alarm_button = tk.Button(master, text="Alarmı Durdur", command=self.stop_alarm, state=tk.DISABLED)
        self.stop_alarm_button.pack()

        self.choose_sound_button = tk.Button(master, text="Alarm Sesi Seç", command=self.choose_sound)
        self.choose_sound_button.pack()

        self.test_sound_button = tk.Button(master, text="Sesi Test Et", command=self.test_sound)
        self.test_sound_button.pack()

        # Zamanı güncelle
        self.update_time()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_display.config(text=current_time)
        self.master.after(1000, self.update_time)

    def set_alarm(self):
        alarm_time_str = self.alarm_time_var.get()
        try:
            alarm_time = datetime.strptime(alarm_time_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen HH:MM formatında bir zaman girin.")
            return
        self.alarm_time = alarm_time
        self.alarm_active = True
        self.snooze_button['state'] = tk.NORMAL
        self.stop_alarm_button['state'] = tk.NORMAL
        self.set_alarm_button['state'] = tk.DISABLED
        self.alarm_thread = threading.Thread(target=self.activate_alarm)
        self.alarm_thread.start()

    def activate_alarm(self):
        while self.alarm_active:
            now = datetime.now()
            if now.hour == self.alarm_time.hour and now.minute == self.alarm_time.minute:
                self.ring_alarm()
                break
            time.sleep(20)

    def ring_alarm(self):
        self.alarm_active = False
        self.snooze_button['state'] = tk.DISABLED
        self.stop_alarm_button['state'] = tk.DISABLED
        winsound.PlaySound(self.alarm_sound, winsound.SND_FILENAME)

    def snooze(self):
        # Erteleme işlemini başlat
        self.stop_alarm()
        snooze_time = datetime.now() + timedelta(minutes=self.snooze_time)
        self.alarm_time = snooze_time
        self.set_alarm()

    def stop_alarm(self):
        # Alarmı durdur
        self.alarm_active = False
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.join()
        self.set_alarm_button['state'] = tk.NORMAL
        self.snooze_button['state'] = tk.DISABLED
        self.stop_alarm_button['state'] = tk.DISABLED

    def choose_sound(self):
        # Alarm ses dosyasını seç
        file_path = filedialog.askopenfilename()
        if file_path:
            self.alarm_sound = file_path
        else:
            self.alarm_sound = self.default_alarm_sound

    def test_sound(self):
        # Alarm sesini test et
        winsound.PlaySound(self.alarm_sound, winsound.SND_FILENAME)

root = tk.Tk()
my_alarm = AlarmClock(root)
root.mainloop()
