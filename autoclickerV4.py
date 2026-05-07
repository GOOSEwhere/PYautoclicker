import pyautogui
import tkinter as tk
from PIL import Image, ImageTk
import keyboard
import threading
from tkinter import messagebox
import sys
import os

window = tk.Tk()
window.title('AutoClicker')
window.geometry('300x400')

#viktige variabler for autoclickeren
autoClickerOn=False
delay = 1000 #ms
autoclickerHotkey = "f9"
påKnappPå = True

hotkey_lock = threading.Lock()


#bilde


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

image_path = resource_path('images/astolfo.png')


icon_image = Image.open(image_path)
icon_photo = ImageTk.PhotoImage(icon_image)
window.iconphoto(False,icon_photo)
#bilde


#funksjon for å skru på autoclickeren
def autoClickerTurnOn():
    global autoClickerOn
    global påKnappPå

    if påKnappPå == False:
        return
    
    påKnappPå = False
    autoClickerOn = True
    print(autoClickerOn)
    autoClicker()


def turbomodus():
    messagebox.showinfo("ADVARSEL", "TURBOMODUS KAN FÅ TING TIL Å KRÆSJE")
    pyautogui.PAUSE = 0
    pyautogui.MINIMUM_DURATION = 0
def turbomodusAV():
    messagebox.showinfo("Turbomodus AV", "Turbomodus har blitt skrudd av")
    pyautogui.PAUSE = 0.1
    pyautogui.MINIMUM_DURATION = 0.1


#funksjonen som utfører klikkene.
def autoClicker():
    global autoClickerOn
    if autoClickerOn:
        pyautogui.click()
        window.after(delay, autoClicker)


#funksjon for å skru avv autoclickeren.
def autoClickerTurnOff():
    global autoClickerOn
    global påKnappPå

    autoClickerOn = False
    påKnappPå = True
    print(autoClickerOn)


def oppdaterClickDelay():
    try:
        ny_verdi = int(inputClickDelay.get())
        global delay
        delay = ny_verdi

        messagebox.showinfo("Click Delay oppdatert", f"Ny Delay oppdatert til: {delay}ms")
    except ValueError:
        messagebox.showinfo("Feil", "Verdien til delay må være et tall uten komma")



#funksjon for å skru av eller på autoclickeren relativt om den er av eller på fra før.
def toggleAutoClicker():
    if autoClickerOn:
        autoClickerTurnOff()
    else:
        autoClickerTurnOn()




# Function for å høre etter om knapp blir trykket 
def setup_hotkeys():
    global autoclickerHotkey

    with hotkey_lock:
        keyboard.add_hotkey(autoclickerHotkey, toggleAutoClicker)  #satt hotkey for å skru av og på
    keyboard.wait('f23')  # sier at den skal vente for et til trykk. Satt til f23 siden den ikke må skrus av, og svært få keyboard har f23


# starte lytteren i en egen "thread" så den ikke kjører over annen kode
hotkey_thread = threading.Thread(target=setup_hotkeys, daemon=True)
hotkey_thread.start()

def hotkeyOppdaterer(ny_hotkey):
    global autoclickerHotkey

    with hotkey_lock:
        keyboard.remove_hotkey(autoclickerHotkey)
        autoclickerHotkey = ny_hotkey
        keyboard.add_hotkey(autoclickerHotkey, toggleAutoClicker)
        print("hotkey er oppdatert")


def oppdaterHotkey():
    try:
        ny_verdi = str(inputNewHotkey.get())
        
        hotkeyOppdaterer(ny_verdi)

        messagebox.showinfo("Hotkey Oppdatert", f"Ny hotkey oppdatert til: {autoclickerHotkey}")
    except ValueError:
        messagebox.showinfo("Feil", "Det du skrev ble ikke forstått.")


def infoBoks():
    messagebox.showinfo("INFO","Default klikk delay er 1000ms eller 1 sekund. Default Hotkey for av og på er f9. Hvis din nye hotkey ikke fungerer prøv noe annent.                                                                       --Autoclickeren er laget av Max Jonas")


#Knapper for å skru på autoclickeren manuelt
påknapp = tk.Button(
    window,
    text="Clicker På",
    command = autoClickerTurnOn)

avknapp = tk.Button(
    window,
    text = "Clicker Av",
    command= autoClickerTurnOff)

påknapp.grid(
    row=0,
    column=0,
    padx=10,   # Add horizontal padding
    pady=40,   # Add vertical padding
    ipadx=20,  # Internal padding on the x-axis
    ipady=10   # Internal padding on the y-axis
)

avknapp.grid(
    row=0,
    column=1,
    padx=10,   # Add horizontal padding
    pady=40,   # Add vertical padding
    ipadx=20,  # Internal padding on the x-axis
    ipady=10   # Internal padding on the y-axis
)


inputClickDelay = tk.Entry(window)
inputClickDelay.grid(row=2,column=0, padx=10,pady=10)

endreKnapp = tk.Button(window, text="Endre Klikk Delay", command=oppdaterClickDelay)
endreKnapp.grid(row=3, column=0, padx=10,pady=10)


inputNewHotkey = tk.Entry(window)
inputNewHotkey.grid(row=2, column=1, padx=10,pady=10)

endreHotkeyKnapp = tk.Button(window,text="Endre Hotkey", command=oppdaterHotkey)
endreHotkeyKnapp.grid(row=3, column=1,padx=10,pady=10)


turbomodusKnapp = tk.Button(window,text="turbomodus", command=turbomodus)
turbomodusKnapp.grid(row=4,column=0,pady=20)

turbomodusAvKnapp = tk.Button(window,text="Turbomodus AV", command=turbomodusAV)
turbomodusAvKnapp.grid(row=4,column=1,pady=20)

infoKnapp = tk.Button(window, text="Info", command=infoBoks)
infoKnapp.grid(row=5,column=1,pady=50)

window.mainloop()
