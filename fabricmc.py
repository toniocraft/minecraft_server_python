import urllib.request
import os
from packaging.version import parse
import webbrowser
from bs4 import BeautifulSoup as Bs
import json
import library


def create_server():
    server_version, installer_version, loader_version = get_version()
    path_installation_server = library.get_installation_directory()
    name_server = download_server_jar(server_version, loader_version, installer_version, path_installation_server)
    batch_path = library.create_batch_file(path_installation_server)
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

def get_version():
    req = urllib.request.Request(
        url="https://meta.fabricmc.net/v2/versions/",
        headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req).read()
    soup = json.loads(str(Bs(page, 'html.parser')))

    installer_version = []
    for key in soup["installer"]:
        for version in key:
            if version == "version":
                installer_version.append(key[version])
    print(f"Latest Fabric installer : {installer_version[0]}")

    minecraft_version = []
    for key in soup["game"]:
        for version in key:
            if version == "version":
                minecraft_version.append(key[version])
    print(f"Latest Minecraft Fabric Version : {minecraft_version[0]}")

    loader_version = []
    for key in soup["loader"]:
        for version in key:
            if version == "version":
                loader_version.append(key[version])
    print(f"Latest Fabric Loader Version : {loader_version[0]}")

    while True:
        version = input('Indiquer une version de minecraft (x.x.x)'
                        ' ou (liste) pour afficher la liste des versions disponibles : ')
        if version == "liste":
            print(minecraft_version)
        else:
            if version in minecraft_version:
                print('Version correct.')
                while True:
                    selection = input('Voulez vous utilisez les dernières versions '
                                      'des installers et loaders ? (o / n) : ')
                    if selection == 'o':
                        return version, installer_version[0], loader_version[0]
                    elif selection == 'n':
                        while True:
                            loader = input('Spécifier la version du loader '
                                           '(ou \"liste\" pour afficher les versions disponibles) : ')
                            if loader == "liste":
                                print(loader_version)
                            elif loader in loader_version:
                                print('Version correct.')
                                while True:
                                    installer = input('Spécifier la version de l\'installer '
                                                      '(ou \"liste\" pour afficher les versions disponibles) : ')
                                    if installer == 'liste':
                                        print(installer_version)
                                    elif installer in installer_version:
                                        print('Choix correct.')
                                        return version, installer, loader
                                    else:
                                        print('Choix incorrect.')
                            else:
                                print('Version incorrect.')
                    else:
                        print('Choix incorrect.')
            else:
                print('Version inconnu.')

def download_server_jar(minecraft_version, loader_version, installer_version, path):
    url = "https://meta.fabricmc.net/v2/versions/" \
          f"loader/{minecraft_version}/{loader_version}/{installer_version}/server/jar"
    print(url)
    print('Téléchargement... ')
    name = f"fabric-server-mc.{minecraft_version}-loader.{loader_version}-launcher.{installer_version}.jar"
    installation_path = path + name
    print(installation_path)
    urllib.request.urlretrieve(url, installation_path)
    return name

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

