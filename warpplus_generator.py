from customtkinter import set_appearance_mode, CTk, CTkButton, CTkInputDialog
from tkinter import CENTER, DISABLED
import urllib.request
from datetime import datetime
import string
from random import choice
from json import dumps
from time import sleep
from threading import Thread
from ctypes import py_object, c_long, pythonapi

referrer = None

set_appearance_mode("system")

app = CTk()
app.geometry("500x60")
app.resizable(False, False)
app.title("WARP+ Data Generator")
# app.iconbitmap("cloud.ico")

def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if not thread.is_alive():
        return

    exc = py_object(SystemExit)
    res = pythonapi.PyThreadState_SetAsyncExc(
        c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
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
        print("Starting main function...                                                  ", end="\r")
        # Demo.setWindowTitle("Starting main function...") # type: ignore
        install_id = genString(22)
        body = {"key": "{}=".format(genString(43)),
                "install_id": install_id,
                "fcm_token": "{}:APA91b{}".format(install_id, genString(134)),
                "referrer": referrer,
                "warp_enabled": False,
                "tos": datetime.now().isoformat()[:-3] + "+02:00",
                "type": "Android",
                "locale": "es_ES"}
        data = dumps(body).encode('utf8')
        headers = {'Content-Type': 'application/json; charset=UTF-8',
                    'Host': 'api.cloudflareclient.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.12.1'
                    }
        print("Requesting...                                                              ", end="\r")
        # Demo.setWindowTitle("Requesting...")
        req         = urllib.request.Request(url, data, headers)
        response    = urllib.request.urlopen(req)
        print("Getting status code...                                                     ", end="\r")
        # Demo.setWindowTitle("Getting status code...")
        status_code = response.getcode()
        print(f"Status code: {status_code}                                                ", end="\r")
        return status_code
    except Exception as error:
            print("")
            print(error)
            
def main():
    added = 0
    while True:
        worker = run()
        if worker == 200:
            added+=1
            app.title("Success! Added " + str(added) + " GB to your account.")
            sleep(1)
        else:
            app.title("Failed to execute command.")
            sleep(1)
        for i in range(15, 0, -1):
            app.title("Next command will run in " + str(i) + "s.")
            sleep(1)

thread1 = Thread(target=main)

def button_click_event():
    global thread1, referrer
    if referrer == None or referrer == "":
            dialog = CTkInputDialog(text="Enter your WARP ID here...", title="Enter ID")
            referrer = dialog.get_input()
            if referrer != None and referrer != "":
                print("ID:", referrer)
                button.configure(text = "Running...")
                thread1.start()
                button["state"] = DISABLED


button = CTkButton(app, text="Start", command=button_click_event, width=470)
button.place(relx=0.5, rely=0.5, anchor=CENTER)

app.mainloop()
terminate_thread(thread1)
# quit(0)