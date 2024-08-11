import customtkinter
import tkinter
import urllib.request
from datetime import datetime
import string
from random import choice
import json
from time import sleep
import threading
import ctypes

referrer = None

customtkinter.set_appearance_mode("system")

app = customtkinter.CTk()
app.geometry("300x300")
app.resizable(False, False)
app.title("WARP+ Data Generator")

def terminate_thread(thread):
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def genString(stringLength):
    try:
        letters = string.ascii_letters + string.digits
        return ''.join(choice(letters) for i in range(stringLength))
    except Exception as error:
        print(error)

def digitString(stringLength):
    try:
        digit = string.digits
        return ''.join((choice(digit) for i in range(stringLength)))
    except Exception as error:
        print(error)

url = f'https://api.cloudflareclient.com/v0a{digitString(3)}/reg'

def run():
    try:
        app.title("Running...")
        install_id = genString(22)
        body = {
            "key": "{}=".format(genString(43)),
            "install_id": install_id,
            "fcm_token": "{}:APA91b{}".format(install_id, genString(134)),
            "referrer": referrer,
            "warp_enabled": False,
            "tos": datetime.now().isoformat()[:-3] + "+02:00",
            "type": "Android",
            "locale": "es_ES"
        }
        data = json.dumps(body).encode('utf8')
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'api.cloudflareclient.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.1'
        }
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        status_code = response.getcode()
        return status_code
    except Exception as error:
        print(error)

def main():
    added = 0
    while True:
        worker = run()
        if worker == 200:
            added += 1
            button.configure(text=f"Successfully added {added} GB.")
            sleep(1)
        else:
            button.configure(text="Command failed.")
            sleep(1)
        for i in range(15, 0, -1):
            progress.set((15 - i) / 15)
            progress_label.configure(text=f"{i}s.")
            sleep(1)
        progress.set(0)
        progress_label.configure(text="Running...")

thread1 = threading.Thread(target=main)

def button_click_event():
    global thread1, referrer
    referrer = entry.get()
    if referrer is not None and referrer != "":
        print("ID:", referrer)
        button.configure(text="Running...")
        thread1.start()
        button.configure(state=tkinter.DISABLED)
        entry.configure(state=tkinter.DISABLED)
        
        progress_label.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
        progress_text_label.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

label = customtkinter.CTkLabel(app, text="Enter your Device ID:", font=("Arial", 12))
label.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

entry = customtkinter.CTkEntry(
    app, 
    width=250, 
    height=40, 
    corner_radius=10, 
    font=("Arial", 12),
    border_width=2,
    border_color="gray",
    fg_color="#f5f5f5",
    text_color="black",
    placeholder_text="Enter your Device ID"
)
entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(app, text="Start", command=button_click_event, width=250, height=35,
                                 corner_radius=5, fg_color=("blue", "gray"),
                                 hover_color=("darkblue", "darkgray"), font=("Arial", 12))
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

progress_text_label = customtkinter.CTkLabel(app, text="Time left before executing next command:", font=("Arial", 12))
progress_label = customtkinter.CTkLabel(app, text="15s", font=("Arial", 12))

progress = customtkinter.CTkProgressBar(app, width=250, height=15, corner_radius=5)
progress.set(0)
progress.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

app.mainloop()
terminate_thread(thread1)
