import tkinter as tk
from tkinter import scrolledtext
import threading
import datetime
import requests
import time
import webbrowser
import os
import speech_recognition as sr
import pyttsx3
import shutil
import sqlite3
import pvporcupine
import pyaudio
import struct

from modules.brain import teach_brain, search_memory, delete_memory, load_memory, jarvis_answer, init_brain
from modules.brain import init_brain
from modules.reminder_store import init_db, add_reminder, get_reminders
from modules.local_weather import get_local_weather
from modules.local_calendar import open_local_calendar
from modules.connection_check import check_online_status

chat_history = []
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

root = tk.Tk()
root.title("Jarvis AI Dashboard")
root.geometry("720x500")
root.configure(bg="black")

status_label = tk.Label(root, text="🌐 Status: Checking...", font=("Helvetica", 12), bg="black", fg="yellow")
status_label.pack(pady=5)

time_label = tk.Label(root, text="🕒 Time: --:--:--", font=("Helvetica", 12), bg="black", fg="cyan")
time_label.pack(pady=5)

listening_led = tk.Label(root, text="🔴 Not Listening", font=("Helvetica", 12), bg="black", fg="red")
listening_led.pack(pady=5)

log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=90, font=("Courier", 10), bg="#111", fg="white")
log_area.pack(pady=10)
log_area.configure(state='disabled')

listening_mode = False

import webbrowser

def search_google(query):
    """Opens a Google search for the given query."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)


def update_led(state):
    if state:
        listening_led.config(text="🟢 Listening", fg="lime")
    else:
        listening_led.config(text="🔴 Not Listening", fg="red")

def log(text, sender="Jarvis"):
    log_area.configure(state='normal')
    log_area.insert(tk.END, f"{sender}: {text}\n")
    log_area.configure(state='disabled')
    log_area.see(tk.END)
    print(f"{sender}: {text}")
    if sender == "Jarvis":
        engine.say(text)
        engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        log("🎤", "System")
        r.dynamic_energy_threshold = True
        r.energy_threshold = 400
        r.adjust_for_ambient_noise(source, duration=1)

        log("🎤 Listening...", "System")
        try:
            audio = r.listen(source, phrase_time_limit=5)
            query = r.recognize_google(audio)
            log(query, "You")
        except sr.UnknownValueError:
            log("Sorry, I didn't catch that.", "Jarvis")
            return ""
        except sr.RequestError:
            log("Speech service error.", "Jarvis")
            return ""
    return query.lower()

def run_nircmd(args):
    nircmd_path = shutil.which("nircmd.exe") or os.path.join(os.getcwd(), "nircmd.exe")
    if os.path.exists(nircmd_path):
        os.system(f'"{nircmd_path}" {args}')
    else:
        log("NirCmd not found.")

def update_time():
    while True:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        time_label.config(text=f"🕒 Time: {now}")
        time.sleep(1)

def check_connection():
    while True:
        if check_online_status():
            status_label.config(text="🌐 Status: Online", fg="green")
        else:
            status_label.config(text="🌐 Status: Offline", fg="red")
        time.sleep(5)

def handle_command(query):
    if not query:
        return

    if "exit" in query or "shutdown" in query:
        log("Goodbye!", "Jarvis")
        root.quit()

    elif "time" in query:
        now = datetime.datetime.now().strftime("%H:%M")
        log(f"The time is {now}", "Jarvis")

    elif "open notepad" in query:
        os.system("notepad")
        
        
        
    elif "open whatsapp" in query:
        desktop_path = os.path.expanduser(r"~\AppData\Local\WhatsApp\WhatsApp.exe")
        if os.path.exists(desktop_path):
            try:
                os.startfile(desktop_path)
                log("Opening WhatsApp Desktop...", "Jarvis")
            except Exception as e:
                log(f"Couldn't open WhatsApp Desktop: {e}. Opening WhatsApp Web instead...", "Jarvis")
                webbrowser.open("https://web.whatsapp.com")
        else:
            log("WhatsApp Desktop not found. Opening WhatsApp Web...", "Jarvis")
            webbrowser.open("https://web.whatsapp.com")

        
    elif "open youtube" in query:
        webbrowser.open("https://youtube.com")

    elif "volume up" in query:
        run_nircmd("changesysvolume 5000")

    elif "volume down" in query:
        run_nircmd("changesysvolume -5000")

    elif "weather" in query:
        log("Which city?", "Jarvis")
        city = take_command()
        if city:
            log(get_local_weather(city), "Jarvis")

    elif "add note" in query or "reminder" in query:
        log("What should I remember?", "Jarvis")
        note = take_command()
        if note:
            add_reminder(note)
            log("Note added.", "Jarvis")

    elif "show notes" in query or "reminders" in query:
        notes = get_reminders()
        if notes:
            for n, t in notes:
                log(f"{n} (added on {t})", "Jarvis")
        else:
            log("You have no reminders.", "Jarvis")

    elif "open calendar" in query:
        open_local_calendar()

    elif "learn this" in query:
        log("What should I learn?", "Jarvis")
        key = take_command()
        log("What should I reply to it?", "Jarvis")
        value = take_command()
        if key and value:
            log(teach_brain(key, value), "Jarvis")
            

    elif "show memory" in query:
        memory = search_memory("")
        for k, v in memory.items():
            log(f"{k} → {v}", "Jarvis")

    elif "delete memory" in query:
        log(delete_memory(), "Jarvis")

    elif "learn this" in query:
        log("What should I learn?", "Jarvis")
        key = take_command()
        log("What should I reply to it?", "Jarvis")
        value = take_command()
        if key and value:
            log(teach_brain(key, value), "Jarvis")

    elif "show memory" in query:
        log(load_memory(), "Jarvis")

    elif "delete memory" in query:
        log(delete_memory(), "Jarvis")
        
# ✅ Google search for "who/what/when/where/why/how"
    elif query.startswith(("who", "what", "when", "where", "why", "how")):
        search_google(query)
        return f"Here’s what I found about {query} on Google."

    # ✅ Generic search / open
    elif "search" in query or "open" in query:
        search_google(query)
        return f"Searching {query} on Google."
    elif "restart" in query:
        os.system("shutdown /r /t 1")
        return "Restarting your system."
    elif "lock" in query:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking your system."
    elif "weather" in query:
        speak("Which city?")
        city = listen()
        if city:
            weather_info = get_local_weather(city)
            log(weather_info, "Jarvis")
        else:
             log("I didn’t catch the city name.", "Jarvis")
    
    else:
        if check_online_status():
            reply = jarvis_answer(query)   # ✅ unified brain
        else:
            reply = search_memory(query) or "I'm still learning to answer that offline."
        log(reply, "Jarvis")

def assistant_loop():
    global listening_mode
    init_db()
    init_brain()  # <-- NEW: setup SQLite brain

    log(load_memory(), "Jarvis")


    porcupine = pvporcupine.create(
        access_key="9giKgCksXGjV90de2WK54GJ+ZOXWtI5glNyq0NCV5Egdt6Dh1tSMJg==",  # Replace with your actual key
        keyword_paths=["jarvis_windows.ppn"]
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    log("Say 'Hey Jarvis' to activate...", "System")

    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        if porcupine.process(pcm) >= 0:
            log("Yes?", "Jarvis")
            listening_mode = True
            update_led(True)
            while listening_mode:
                query = take_command()
                if "go to sleep" in query or "stop listening" in query:
                    log("Okay, going silent.", "Jarvis")
                    listening_mode = False
                    update_led(False)
                    break
                handle_command(query)

def toggle_listening():
    global listening_mode
    if not listening_mode:
        listening_mode = True
        update_led(True)
        threading.Thread(target=manual_listen_loop, daemon=True).start()
    else:
        log("Manual listening stopped.", "Jarvis")
        listening_mode = False
        update_led(False)

def manual_listen_loop():
    global listening_mode
    while listening_mode:
        query = take_command()
        if "go to sleep" in query or "stop listening" in query:
            log("Okay, going silent.", "Jarvis")
            listening_mode = False
            update_led(False)
            break
        handle_command(query)

# Toggle button for manual listening
toggle_btn = tk.Button(root, text="🎙️ Toggle Listening", command=toggle_listening, bg="gray", fg="white", font=("Helvetica", 12))
toggle_btn.pack(pady=10)

# Start threads
threading.Thread(target=update_time, daemon=True).start()
threading.Thread(target=check_connection, daemon=True).start()
threading.Thread(target=assistant_loop, daemon=True).start()

root.mainloop()
