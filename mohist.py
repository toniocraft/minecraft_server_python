import urllib.request
import tkinter.filedialog
import pathlib
import os
from packaging.version import parse
import webbrowser
from psutil import virtual_memory
import winshell
from bs4 import BeautifulSoup as Bs
import json
import requests


def create_server():
    build_version, name_server, server_version, url_download = get_version()
    path_installation_server = get_installation_directory()
    download_server_jar(url_download, path_installation_server, name_server)
    batch_path = create_batch_file(path_installation_server)
    create_batch_content(batch_path, server_version, name_server)
    print('Serveur créé')
    shortcut = input("Voulez vous créer un raccourci sur le bureau ? (o / n) : ")
    if shortcut == "n":
        pass
    else:
        if not shortcut == "o":
            print('Choix incorrect, création du raccourci par défaut.')
        create_shortcut(name_server, path_installation_server, batch_path)
    start = input('Souhaitez-vous l\'exécuter ? (o / n) : ')
    if start == 'o':
        os.chdir(path_installation_server)
        os.startfile(batch_path)


def get_version():
    print('Versions disponibles : 1.7.10 / 1.12.2 / 1.16.5 / 1.19.2')
    version = input('Indiquer une version : ')
    url = "https://mohistmc.com/api/" + version
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req).read()
    soup = json.loads(str(Bs(page, 'html.parser')))
    list_build_version = []
    for key in soup:
        if soup[key]["status"] == "SUCCESS":
            list_build_version.append(key)
    url = f"https://mohistmc.com/api/{version}/latest"
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req).read()
    soup = json.loads(str(Bs(page, 'html.parser')))
    build = soup["number"]
    name = soup["name"]
    url_download = soup["url"]
    print(f'Dernier numéro du build : {build}')
    build = max(list_build_version)
    selection = input(f'Voulez vous utiliser le dernier numéro du build pour la {version} ? (o / n) : ')
    if selection == "n":
        while True:
            print(f'Liste des versions de build disponible : {list_build_version}')
            selection_build = int(input('Indiquer un numéro de build : '))
            if selection_build in list_build_version:
                print('Build fonctionnant correctement.')
                build = selection_build
                break
            else:
                print("Erreur, impossible de trouver le build.")
    else:
        if selection != "o":
            print(f'Choix incorrect.\nDernier numéro du build par défaut')

    return build, name, version, url_download


def get_installation_directory():
    print('Choisissez le répertoire d\'installation du fichier dans la fenêtre qui vient de s\'ouvrir.')
    root = tkinter.Tk()
    root.attributes("-alpha", 0)
    root.attributes("-topmost", 1)
    path = tkinter.filedialog.askdirectory(parent=root)
    root.destroy()
    root.mainloop()
    return path + "/"


def download_server_jar(download_url, path, name):
    print(download_url)
    req = urllib.request.Request(
        url=download_url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    size = urllib.request.urlopen(req).info()["Content-Length"]
    print('Téléchargement... ' + "(", round(int(size) / (1024 ** 2), 2), "Mo", ")")
    installation_path = path + name
    print(installation_path)
    r = requests.get(download_url)
    with open(installation_path, 'wb') as outfile:
        outfile.write(r.content)


def create_batch_file(path):
    path_file = f'{path}/run.bat'
    my_bat = open(path_file, 'w+')
    my_bat.close()
    return path_file


def create_batch_content(batch_path, server_version, name_server):
    dict_with_java_version = get_installed_java()
    # java
    while True:
        selection = input('Trouvez une version de java automatique ? (o / n) : ')
        if selection == "o":
            java_path_argument = check_java_version(server_version, dict_with_java_version)
            break
        elif selection == 'n':
            java_path_argument = locate_java_directory()
            break
        else:
            print("Choix incorrect")
    # ram
    while True:
        selection = input('Paramètre RAM automatique ? (o / n) : ')
        if selection == 'o':
            xmx, xms = get_ram_info()
            break
        elif selection == 'n':
            xmx = int(input("Indiquer un nombre entier de RAM maximal (Xmx en Go) : "))
            xms = int(input('Indiquer un nombre entier de RAM maximal au démarrage (Xms en Go) : '))
            break
        else:
            print('Choix incorrect')
    selection = input("Souhaitez vous avoir une interface graphique pour serveur ? (o / n) : ")
    graphic_interface = ""
    if selection == "o":
        graphic_interface = ""
    elif selection == "n":
        graphic_interface = "nogui"
    else:
        print('Choix incorrect, interface graphique par défaut désactivé.')
    my_batch = open(batch_path, 'w+')
    my_batch.write(f'''\"{java_path_argument}\" -jar -Xmx{xmx}G -Xms{xms}G {name_server} {graphic_interface}\npause''')
    my_batch.close()


def get_installed_java():
    dict_jvm = {}
    home = pathlib.Path.home().drive
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


def check_java_version(version_minecraft, dict_with_java_version):
    if parse(version_minecraft) < parse("1.17"):
        # need java 1.8.0
        for key in dict_with_java_version:
            if "jre1.8.0" in key:
                print('Java trouvé')
                return dict_with_java_version[key]

        print('Java n\'a pas été trouvé')
        print('1- Localiser java manuellement\n2- Télécharger java manuellement')
        selection_1 = input('Indiquer une solution (1 ou 2) : ')
        if selection_1 == "1":
            return locate_java_directory()
        elif selection_1 == "2":
            webbrowser.open("https://www.java.com/fr/download/manual.jsp")
            print("Une fois l'installation finit, merci de redémarrer le programme")
            exit()

    elif parse(version_minecraft) >= parse("1.17"):
        # need java 17+
        for key in dict_with_java_version:
            if "jdk-17" in key or "jdk-18" in key or "jdk-19" in key:
                print('Java trouvé')
                return dict_with_java_version[key]
        print('Java n\'a pas été trouvé')
        print('Vous avez besoin de Java 17, 18 ou 19+')
        print('1- Localiser java manuellement\n2- Télécharger java manuellement')
        selection_1 = input('Indiquer une solution (1 ou 2) : ')
        if selection_1 == "1":
            return locate_java_directory()
        elif selection_1 == "2":
            webbrowser.open("https://www.java.com/fr/download/manual.jsp")
            print("Une fois l'installation fini, merci de redémarrer le programme")
            exit()

    else:
        print("Une erreur est survenue")


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


def create_shortcut(name_server, path_server_directory, batch_path):
    desktop = pathlib.Path(winshell.desktop())
    link_filepath = str(desktop / f"{name_server}.lnk")
    with winshell.shortcut(link_filepath) as link:
        link.path = batch_path
        link.working_directory = path_server_directory
