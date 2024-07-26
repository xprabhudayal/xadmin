import tkinter as tk
from tkinter import font
from main import app
import webbrowser

def open_documentation():
    webbrowser.open("https://github.com/xprabhudayal/xadmin")

def invisible():
    root.withdraw()
    app()


# Create the main window
root = tk.Tk()
root.title("xadmin")

root.geometry("250x250")

heading_font = font.Font(family="Helvetica", size=24, weight="bold")

heading_label = tk.Label(root, text="xAdmin", font=heading_font)
heading_label.pack(pady=10)

# description label
description_label = tk.Label(root, text="""xAdmin is a program that remotely 
connects the terminal to the Telegram bot. """)
description_label.pack(pady=5)

#button configs
support_button = tk.Button(root, text="Support", command=open_documentation)
support_button.pack(pady=5)

normal_button = tk.Button(root, text="Normal Mode", command=app)
normal_button.pack(pady=5)

invisible_button = tk.Button(root, text="Invisible Mode", command=invisible)
invisible_button.pack(pady=5)


# Start the main event loop
root.mainloop()
