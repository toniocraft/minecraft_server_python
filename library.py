from pathlib import Path
import winshell
from psutil import virtual_memory
import os
import tkinter.filedialog


def create_shortcut(name_server, path_server_directory, batch_path):
    desktop = Path(winshell.desktop())
    link_filepath = str(desktop / f"{name_server}.lnk")
    with winshell.shortcut(link_filepath) as link:
        link.path = batch_path
        link.working_directory = path_server_directory

def get_ram_info():
    total = virtual_memory().total / (1024 ** 3)
    if int(total) > 2:
        if int(total) > 4:
            if int(total) > 8:
                if int(total) > 16:
                    xmx = 10
                    xms = xmx / 2
                else:
                    xmx = 6
                    xms = xmx / 2
            else:
                xmx = 4
                xms = xmx / 2
        else:
            xmx = 2
            xms = xmx / 2
    else:
        if int(total) <= 1:
            print('Erreur, niveau de RAM insuffisant')
            raise
        else:
            print('Niveau de ram bas (Cela peut causer des lags serveur')
            xmx = 1
            xms = 1
    xmx, xms = int(xmx), int(xms)
    print(f'Xmx : {xmx}')
    print(f'Xms : {xms}')
    return xmx, xms

def locate_java_directory():
    root = tkinter.Tk()
    root.attributes("-alpha", 0)
    filename = tkinter.filedialog.askopenfilename(initialdir="/",
                                                  title="Select a File",
                                                  filetypes=(
                                                      ("Executable", "*.exe"),
                                                      ('All files', '*.*')
                                                  ))
    root.destroy()
    root.mainloop()
    return filename

def get_installed_java():
    dict_jvm = {}
    home = Path.home().drive
    # x64
    try:
        java_dir_x64 = os.path.join(home, '\\Program Files', 'Java')
        print(f"Java dir x64 : {java_dir_x64}")
        files = os.listdir(java_dir_x64)
        for java_version in files:
            try:
                temp_dir = os.path.join(java_dir_x64, f'{java_version}', 'bin', 'java.exe')
                temp_exists = os.path.exists(temp_dir)
                print(f"Exists : {temp_exists} ; Java version dir (x64) : {temp_dir}")
                if temp_exists:
                    dict_jvm[java_version] = temp_dir
            except FileNotFoundError:
                print("Java version directory (x64) not found")
    except FileNotFoundError:
        print("Java directory (x64) not found")
    # x86
    try:
        java_dir_x86 = os.path.join(home, '\\Program Files (x86)', 'Java')
        print(f"Java dir x86 : {java_dir_x86}")
        files = os.listdir(java_dir_x86)
        for java_version in files:
            try:
                temp_dir = os.path.join(java_dir_x86, f'{java_version}', 'bin', 'java.exe')
                temp_exists = os.path.exists(temp_dir)
                print(f"Exists : {temp_exists} ; Java version dir (x86) : {temp_dir}")
                if temp_exists:
                    dict_jvm[java_version] = temp_dir
            except FileNotFoundError:
                print("Java version directory (x86) not found")
    except FileNotFoundError:
        print("Java directory (x86) not found")
    finally:
        print(f'Version found (x64 & x86) : {dict_jvm}')
    return dict_jvm

def create_batch_file(path):
    path_file = f'{path}/run.bat'
    my_bat = open(path_file, 'w+')
    my_bat.close()
    return path_file

def get_installation_directory():
    print('Choisissez le répertoire d\'installation du fichier dans la fenêtre qui vient de s\'ouvrir.')
    root = tkinter.Tk()
    root.attributes("-alpha", 0)
    root.attributes("-topmost", 1)
    path = tkinter.filedialog.askdirectory()
    root.destroy()
    root.mainloop()
    return path + "/"