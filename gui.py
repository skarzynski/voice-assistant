from tkinter import filedialog
from tkinter import PhotoImage
import tkinter as tk
import tkinter.ttk as ttk
import os
import pickle
from config import lang, apps
from langs import languages


def gui():

    def create_modal():
        window.wm_attributes("-disabled", True)
        global modal_window
        modal_window = tk.Toplevel(window)
        modal_window.minsize(400, 400)
        modal_window.transient(window)
        modal_window.protocol("WM_DELETE_WINDOW", close_modal)

    def close_modal():
        window.wm_attributes("-disabled", False)
        modal_window.destroy()

    def open_help():
        create_modal()
        help_label = tk.Label(modal_window, text=lang["about_text"])
        help_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def open_commands():
        create_modal()
        commands = tk.Label(modal_window, text=lang["all_commands"])
        commands.pack(pady=10)

    def open_settings():
        create_modal()

        # TODO: Add username change setting

        lang_var = tk.StringVar()
        lang_label = tk.Label(modal_window, text=f"{lang['language']}:")
        lang_value = tk.OptionMenu(modal_window, lang_var, *(languages.keys()))
        lang_label.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        lang_value.grid(row=0, column=1, pady=10, padx=10)
        lang_var.set(lang["full_lang"])

        apps_list = tk.Listbox(modal_window)
        for app in apps:
            apps_list.insert(tk.END, app.capitalize())
        apps_list.grid(row=1, columnspan=2)
        apps_list.config(width=65, height=15)

        apps_buttons = tk.Frame(modal_window)
        apps_buttons.grid(row=2, columnspan=2, pady=10, padx=10)

        # TODO: Add app function
        add_button = tk.Button(apps_buttons, text="Add", command=None)
        add_button.pack(side=tk.LEFT, padx=5)

        # TODO: Edit app function
        edit_button = tk.Button(apps_buttons, text="Edit", command=None)
        edit_button.pack(side=tk.LEFT, padx=5)

        # TODO: Remove app function
        remove_button = tk.Button(apps_buttons, text="Remove", command=None)
        remove_button.pack(side=tk.LEFT, padx=5)

        # TODO: Save settings function
        save_button = tk.Button(modal_window, text="Save", command=None)
        save_button.grid(row=3, columnspan=2, pady=10)

    window = tk.Tk()
    window.title(lang["title"])

    dropdown_menu = tk.Menu(window)

    file_menu = tk.Menu(dropdown_menu, tearoff=0)
    file_menu.add_command(label=lang["settings"], command=open_settings)
    file_menu.add_separator()
    file_menu.add_command(label=lang["exit"], command=window.quit)

    dropdown_menu.add_cascade(label=lang["file"], menu=file_menu)

    help_menu = tk.Menu(dropdown_menu, tearoff=0)
    help_menu.add_command(label=lang["commands"], command=open_commands)
    help_menu.add_command(label=lang["about"], command=open_help)

    dropdown_menu.add_cascade(label=lang["help"], menu=help_menu)

    toolbar = tk.Frame(window)
    toolbar.pack(fill=tk.X, anchor=tk.N)

    content_frame = tk.Frame(window)
    content_frame.pack(expand=True, fill=tk.BOTH)

    app_response_text = tk.StringVar()
    app_response = tk.Label(content_frame, textvariable=app_response_text)
    app_response_text.set(lang["push_button"])
    app_response.grid(row=0, padx=10, pady=5)
    app_response.configure(font=("Arial", 15))

    previous_command_text = tk.StringVar()
    previous_command = tk.Label(content_frame, textvariable=previous_command_text)
    previous_command_text.set(f"{lang['previous_command']}: what time is it")
    previous_command.grid(row=1, padx=10, pady=5)
    previous_command.configure(font=("Arial", 10), fg="#696969")

    try_commands_text = tk.StringVar()
    try_commands = tk.Label(content_frame, textvariable=try_commands_text)
    try_commands_text.set(lang["try_commands"])
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
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    gui()
