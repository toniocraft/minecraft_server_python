import urllib.request
import os
from packaging.version import parse
import webbrowser
from subprocess import call
from minecraft_launcher_lib.forge import find_forge_version
import library


def get_version():
    version = input('Indiquer une version (x.x.x) : ')
    return version

def download_server_jar(version, path):
    forge_version = find_forge_version(version)
    print(forge_version)
    url = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/" \
          f"{forge_version}/forge-{forge_version}-installer.jar"
    size = urllib.request.urlopen(url).info()['Content-Length']
    print(url)
    print('Téléchargement... ' + "(", round(int(size) / (1024 ** 2), 2), "Mo", ")")
    name = "forge_installer.jar"
    installation_path = path + name
    print(installation_path)
    urllib.request.urlretrieve(url, installation_path)
    # return name

def get_name_server(server_path):
    files = os.listdir(server_path)
    name_server = ""
    for file in files:
        if "forge" in file:
            name_server = file
            break
    if name_server == "":
        print('Une erreur est survenue')
        raise
    return name_server

def create_server():
    server_version = get_version()
    path_installation_server = library.get_installation_directory()
    download_server_jar(server_version, path_installation_server)
    batch_installer_path = create_batch_installer_file(path_installation_server)
    create_batch_installer_content(batch_installer_path)
    run_batch_installer(batch_installer_path, path_installation_server)
    batch_path = library.create_batch_file(path_installation_server)
    name_server = get_name_server(path_installation_server)
    create_batch_content(batch_path, server_version, name_server)
    print('Serveur créé')
    shortcut = input("Voulez vous créer un raccourci sur le bureau ? (o / n) : ")
    if shortcut == "n":
        pass
    else:
        if not shortcut == "o":
            print('Choix incorrect, création du raccourci par défaut.')
        library.create_shortcut(name_server, path_installation_server, batch_path)
    start = input('Souhaitez-vous l\'exécuter ? (o / n) : ')
    if start == 'o':
        os.chdir(path_installation_server)
        os.startfile(batch_path)

def create_batch_installer_file(path):
    path_file = f'{path}/installer.bat'
    my_bat = open(path_file, 'w+')
    my_bat.close()
    return path_file

def create_batch_installer_content(batch_path):
    my_batch = open(batch_path, 'w+')
    my_batch.write('java -jar forge_installer.jar --installServer')
    my_batch.close()

def run_batch_installer(batch_installer_path, path_server):
    print('Installation du serveur...\n Merci de ne fermer aucune fenêtre.')
    os.chdir(path_server)
    call(batch_installer_path)
    try:
        os.remove("installer.bat")
        os.remove("installer.log")
        os.remove("forge_installer.jar")
    except FileNotFoundError:
        pass

def create_batch_content(batch_path, server_version, name_server):
    dict_with_java_version = library.get_installed_java()
    # java
    while True:
        selection = input('Trouvez une version de java automatique ? (o / n) : ')
        if selection == "o":
            java_path_argument = check_java_version(server_version, dict_with_java_version)
            break
        elif selection == 'n':
            java_path_argument = library.locate_java_directory()
            break
        else:
            print("Choix incorrect")
    # ram
    while True:
        selection = input('Paramètre RAM automatique ? (o / n) : ')
        if selection == 'o':
            xmx, xms = library.get_ram_info()
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

def check_java_version(version_minecraft, dict_with_java_version):
    if parse(version_minecraft) < parse("1.17"):
        # need java 1.8.0
        for key in dict_with_java_version:
            if "jre-1.8" in key:
                print('Java trouvé')
                return dict_with_java_version[key]

        print('Java n\'a pas été trouvé')
        print('1- Localiser java manuellement\n2- Télécharger java manuellement')
        selection_1 = input('Indiquer une solution (1 ou 2) : ')
        if selection_1 == "1":
            return library.locate_java_directory()
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
            return library.locate_java_directory()
        elif selection_1 == "2":
            webbrowser.open("https://www.java.com/fr/download/manual.jsp")
            print("Une fois l'installation fini, merci de redémarrer le programme")
            exit()

    else:
        print("Une erreur est survenue")
