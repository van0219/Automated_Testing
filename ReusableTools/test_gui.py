# -*- coding: utf-8 -*-
import tkinter as tk

print("Creating window...")
root = tk.Tk()
root.title("Test Window")
root.geometry("400x300")

label = tk.Label(root, text="If you see this, GUI works!", font=('Arial', 16))
label.pack(pady=50)

button = tk.Button(root, text="Close", command=root.destroy)
button.pack()

print("Starting mainloop...")
root.mainloop()
print("Window closed")
