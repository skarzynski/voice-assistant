import os
import sys
import tkinter as tk
from tkinter import PhotoImage
from tkinter import filedialog, simpledialog, messagebox
import controller
import voice_engine as ve

import config
from langs import languages

changes = False


def gui():
    def restart_app():
        app = sys.executable
        os.execl(app, app, *sys.argv)

    def create_modal():
        window.wm_attributes("-disabled", True)
        global modal_window
        modal_window = tk.Toplevel(window)
        modal_window.minsize(400, 400)
        modal_window.resizable(False, False)
        modal_window.transient(window)
        modal_window.protocol("WM_DELETE_WINDOW", close_modal)

    def close_modal():
        global changes
        exit_confirm = True if not changes else messagebox.askokcancel(config.lang["exit"], config.lang["exit_confirm"])
        if exit_confirm:
            window.wm_attributes("-disabled", False)
            modal_window.destroy()
            changes = False

    def open_help():
        create_modal()
        help_label = tk.Label(modal_window, text=config.lang["about_text"])
        help_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def open_commands():
        create_modal()
        commands = tk.Label(modal_window, text=config.lang["all_commands"])
        commands.pack(pady=10)

    def open_settings():
        create_modal()
        global changes
        changes = False
        apps_temp = config.apps.copy()
        username_var = tk.StringVar()
        username_label = tk.Label(modal_window, text=config.lang["username"])
        username_value = tk.Entry(modal_window, textvariable=username_var, width=30)
        username_label.grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        username_value.grid(row=0, column=1, pady=10, padx=10)
        username_var.set(config.username)

        lang_var = tk.StringVar()
        lang_label = tk.Label(modal_window, text=f"{config.lang['language']}:")
        lang_value = tk.OptionMenu(modal_window, lang_var, *(languages.keys()))
        lang_label.grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        lang_value.grid(row=1, column=1, pady=10, padx=10)
        lang_var.set(config.lang["full_lang"])

        apps_list = tk.Listbox(modal_window)
        for app in config.apps:
            apps_list.insert(tk.END, app.capitalize())
        apps_list.grid(row=2, columnspan=2)
        apps_list.config(width=65, height=15)

        apps_buttons = tk.Frame(modal_window)
        apps_buttons.grid(row=3, columnspan=2, pady=10, padx=10)

        add_button = tk.Button(apps_buttons, text=config.lang["add"], command=lambda: add_app(apps_list, apps_temp))
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = tk.Button(apps_buttons, text=config.lang["edit"], command=lambda: edit_app(apps_list, apps_temp))
        edit_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(apps_buttons, text=config.lang["remove"],
                                  command=lambda: delete_app(apps_list, apps_temp))
        remove_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(modal_window, text=config.lang["save_config"],
                                command=lambda: save_config_to_file(apps_temp, username_var.get(), lang_var.get()))
        save_button.grid(row=4, columnspan=2, pady=10)

    def add_app(apps_list, apps_temp):
        global changes
        name = simpledialog.askstring(config.lang["name"], config.lang["enter_app_name"])
        if name is not None:
            name = name.lower()
            path = filedialog.askopenfilename()
            if path != "":
                if name not in apps_temp:
                    apps_temp[name] = path
                    apps_list.insert(tk.END, name.capitalize())
                    changes = True
                    status_text.set(config.lang["app_added"])
                else:
                    status_text.set(config.lang["error"])
                    messagebox.showerror(config.lang["error"], f"{name.capitalize()} {config.lang['already_on_list']}")
            else:
                status_text.set(config.lang["error"])
                messagebox.showerror(config.lang["error"], config.lang["err_choose_exe"])
        else:
            status_text.set(config.lang["error"])
            messagebox.showerror(config.lang["error"], config.lang["err_enter_app_name"])

    def edit_app(apps_list, apps_temp):
        global changes
        name = apps_list.get(apps_list.curselection()).lower()
        path = filedialog.askopenfilename()
        if path != "":
            apps_temp[name] = path
            changes = True
            status_text.set(config.lang["app_edited"])
        else:
            status_text.set(config.lang["error"])
            messagebox.showerror(config.lang["error"], config.lang["err_choose_exe"])

    def delete_app(apps_list, apps_temp):
        global changes
        name = apps_list.get(apps_list.curselection()).lower()
        delete_confirmed = messagebox.askyesno(config.lang["delete"],
                                               f"{config.lang['del_confirm1']} {name.capitalize()} {config.lang['del_confirm2']}")
        if delete_confirmed:
            del apps_temp[name]
            apps_list.delete(apps_list.curselection())
            changes = True
            status_text.set(config.lang["app_removed"])

    def save_config_to_file(new_apps_list, new_username, new_lang):
        save_confirmed = messagebox.askyesno(config.lang["save_config"], config.lang["save_confirm"])
        if save_confirmed:
            config.apps = new_apps_list.copy()
            if new_username != "":
                config.username = new_username
            config.lang = languages[new_lang]
            config.save_conf()
            restart_app()

    def listen():
        audio = ve.take_command()
        command = ve.recognize(audio)
        controller.process_command(command.lower())
        previous_command_text.set(f"{config.lang['previous_command']}: {command}")
        pass

    window = tk.Tk()
    window.title(config.lang["title"])

    dropdown_menu = tk.Menu(window)

    file_menu = tk.Menu(dropdown_menu, tearoff=0)
    file_menu.add_command(label=config.lang["settings"], command=open_settings)
    file_menu.add_separator()
    file_menu.add_command(label=config.lang["restart"], command=restart_app)
    file_menu.add_command(label=config.lang["exit"], command=window.quit)

    dropdown_menu.add_cascade(label=config.lang["file"], menu=file_menu)

    help_menu = tk.Menu(dropdown_menu, tearoff=0)
    help_menu.add_command(label=config.lang["commands"], command=open_commands)
    help_menu.add_command(label=config.lang["about"], command=open_help)

    dropdown_menu.add_cascade(label=config.lang["help"], menu=help_menu)

    toolbar = tk.Frame(window)
    toolbar.pack(fill=tk.X, anchor=tk.N)

    content_frame = tk.Frame(window)
    content_frame.pack(expand=True, fill=tk.BOTH)

    app_response_text = tk.StringVar()
    app_response = tk.Label(content_frame, textvariable=app_response_text)
    app_response_text.set(config.lang["push_button"])
    app_response.grid(row=0, padx=10, pady=5)
    app_response.configure(font=("Arial", 15))

    previous_command_text = tk.StringVar()
    previous_command = tk.Label(content_frame, textvariable=previous_command_text)
    previous_command_text.set(f"{config.lang['previous_command']}: ")
    previous_command.grid(row=1, padx=10, pady=5)
    previous_command.configure(font=("Arial", 10), fg="#696969")

    try_commands_text = tk.StringVar()
    try_commands = tk.Label(content_frame, textvariable=try_commands_text)
    try_commands_text.set(config.lang["try_commands"])
    try_commands.grid(row=2, padx=10, pady=5)
    try_commands.configure(font=("Arial", 10), fg="#696969")

    listen_button_image = PhotoImage(file=r"images/microphone.png")
    listen_button = tk.Button(content_frame, image=listen_button_image, relief=tk.FLAT, command=listen)
    listen_button.grid(row=3, padx=10, pady=5)

    status_bar = tk.Frame(window)
    status_bar.pack(fill=tk.X, anchor=tk.S)

    status_text = tk.StringVar()
    status = tk.Label(status_bar, bd=1, textvariable=status_text, relief=tk.SUNKEN)
    status.pack(fill=tk.X)

    window.config(menu=dropdown_menu)
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    gui()
