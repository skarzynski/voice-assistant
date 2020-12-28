from tkinter import filedialog
from tkinter import PhotoImage
import tkinter as tk
import tkinter.ttk as ttk
import os
import pickle


def gui():
    global help_window

    def close_help():
        window.wm_attributes("-disabled", False)
        global help_window
        help_window.destroy()

    def open_help():
        window.wm_attributes("-disabled", True)
        global help_window
        help_window = tk.Toplevel(window)
        help_window.minsize(400, 400)
        help_window.transient(window)
        help_window.protocol("WM_DELETE_WINDOW", close_help)

        help_label = tk.Label(help_window, text="App made for script languages laboratory")
        help_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #     option = Option(place, dateDay, dateMonth, numberOfDays, countDeaths, sortDeaths)
    #     if option not in options:
    #         previousOptions.insert(tk.END, option)
    #         options.append(option)

    window = tk.Tk()
    window.title("Voice Assistant")

    dropdown_menu = tk.Menu(window)

    file_menu = tk.Menu(dropdown_menu, tearoff=0)
    file_menu.add_command(label="Settings", command=None)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.quit)

    dropdown_menu.add_cascade(label="File", menu=file_menu)

    help_menu = tk.Menu(dropdown_menu, tearoff=0)
    help_menu.add_command(label="Commands", command=None)
    help_menu.add_command(label="About", command=open_help)

    dropdown_menu.add_cascade(label="Help", menu=help_menu)

    toolbar = tk.Frame(window)
    toolbar.pack(fill=tk.X, anchor=tk.N)

    content_frame = tk.Frame(window)
    content_frame.pack(expand=True, fill=tk.BOTH)

    app_response_text = tk.StringVar()
    app_response = tk.Label(content_frame, textvariable=app_response_text)
    app_response_text.set("Push button and say something")
    app_response.grid(row=0, padx=10, pady=5)
    app_response.configure(font=("Arial", 15))

    previous_command_text = tk.StringVar()
    previous_command = tk.Label(content_frame, textvariable=previous_command_text)
    previous_command_text.set(f"Previous command: what time is it")
    previous_command.grid(row=1, padx=10, pady=5)
    previous_command.configure(font=("Arial", 10), fg="#696969")

    try_commands_text = tk.StringVar()
    try_commands = tk.Label(content_frame, textvariable=try_commands_text)
    try_commands_text.set("Try: \"Hello\"\nTry: \"What time is it?\"\nTry: \"Open notepad\"")
    try_commands.grid(row=2, padx=10, pady=5)
    try_commands.configure(font=("Arial", 10), fg="#696969")

    listen_button_image = PhotoImage(file=r"images/microphone.png")
    listen_button = tk.Button(content_frame, image=listen_button_image, relief=tk.FLAT, command=None)
    listen_button.grid(row=3, padx=10, pady=5)

    status_bar = tk.Frame(window)
    status_bar.pack(fill=tk.X, anchor=tk.S)

    status_text = tk.StringVar()
    status = tk.Label(status_bar, bd=1, textvariable=status_text, relief=tk.SUNKEN)
    status_text.set("Status bar")
    status.pack(fill=tk.X)

    window.config(menu=dropdown_menu)
    # window.minsize(970, 555)
    # window.maxsize(1400, 530)
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    gui()
