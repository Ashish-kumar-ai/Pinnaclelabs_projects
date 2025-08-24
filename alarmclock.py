import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import threading
import pygame
import os
import winsound
from datetime import datetime, timedelta

# Variable declaration
alarm_time = None
alarm_file = None
snooze_minutes = 5
stop_sound = False
checker_thread = None
alarm_rang = False  

pygame.mixer.init()

# Function
def set_alarm():
    global alarm_time, checker_thread, stop_sound, alarm_rang
    stop_sound = False
    alarm_rang = False  

    hr = int(hour.get())
    mn = int(minute.get())
    sec = int(second.get())
    period = am_pm.get()

    # Convert to 24-hour format
    if period == "PM" and hr != 12:
        hr += 12
    elif period == "AM" and hr == 12:
        hr = 0

    alarm_time = f"{hr:02d}:{mn:02d}:{sec:02d}"
    status_label.config(text=f"Alarm set for {alarm_time}")

    if checker_thread is None or not checker_thread.is_alive():
        threading.Thread(target=alarm_checker, daemon=True).start()


def choose_sound():
    global alarm_file
    file_path = filedialog.askopenfilename(
        title="Choose Alarm Sound",
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )
    if file_path:
        alarm_file = file_path
        sound_label.config(text=f"Sound: {os.path.basename(file_path)}")


def alarm_checker():
    global alarm_rang
    while True:
        if alarm_time and not alarm_rang:
            current_time = time.strftime("%H:%M:%S")
            if current_time >= alarm_time:
                alarm_rang = True
                ring_alarm()
        time.sleep(1)


def ring_alarm():
    global stop_sound
    stop_sound = False

    def play_sound():
        if alarm_file:
            pygame.mixer.music.load(alarm_file)
            pygame.mixer.music.play(-1)  
            while not stop_sound:
                time.sleep(0.1)
        else:
            while not stop_sound:
                winsound.Beep(1000, 700)  
                time.sleep(0.5)

    threading.Thread(target=play_sound, daemon=True).start()

    # Alarm message
    response = messagebox.askquestion("Alarm", "Wake up! Snooze?")
    if response == "yes":
        snooze_alarm()
    else:
        stop_alarm_func()


def snooze_alarm():
    global alarm_time, alarm_rang
    stop_alarm_func()  
    new_time = datetime.now() + timedelta(minutes=snooze_minutes)
    alarm_time = new_time.strftime("%H:%M:%S")
    alarm_rang = False  
    status_label.config(
        text=f"Snoozed for {snooze_minutes} mins (Next: {alarm_time})"
    )


def stop_alarm_func():
    global stop_sound
    stop_sound = True
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    status_label.config(text="Alarm stopped")


# GUI 
root = tk.Tk()
root.title("Python Alarm Clock")
root.geometry("350x340")

tk.Label(root, text="Set Alarm Time").pack(pady=10)

frame = tk.Frame(root)
frame.pack()

hour = ttk.Combobox(frame, width=3, values=[f"{i:02d}" for i in range(1, 13)])
hour.grid(row=0, column=0)
hour.set("07")

minute = ttk.Combobox(frame, width=3, values=[f"{i:02d}" for i in range(60)])
minute.grid(row=0, column=1)
minute.set("30")

second = ttk.Combobox(frame, width=3, values=[f"{i:02d}" for i in range(60)])
second.grid(row=0, column=2)
second.set("00")

am_pm = ttk.Combobox(frame, width=3, values=["AM", "PM"])
am_pm.grid(row=0, column=3)
am_pm.set("AM")

tk.Button(root, text="Set Alarm", command=set_alarm).pack(pady=5)
tk.Button(root, text="Choose Sound", command=choose_sound).pack(pady=5)
tk.Button(root, text="Stop Alarm", command=stop_alarm_func).pack(pady=5)

status_label = tk.Label(root, text="No Alarm Set", fg="blue")
status_label.pack(pady=5)

sound_label = tk.Label(root, text="Sound: Default (Beep)", fg="green")
sound_label.pack(pady=5)

root.mainloop()