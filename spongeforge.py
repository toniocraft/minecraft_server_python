import urllib.request
import os
from subprocess import call
from bs4 import BeautifulSoup as Bs
from minecraft_launcher_lib.forge import find_forge_version
import webbrowser
import library


def get_version():
    url = "https://repo.spongepowered.org/service/rest/repository/browse/maven-releases/org/spongepowered/spongeforge/"
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req).read()
    soup = Bs(page, 'html.parser')
    list_version = []
    for a in soup.find_all('a', href=True):
        if a['href'] != '../' and not 'https://' in a['href']:
            list_version.append(a['href'])

    while True:
        choice = input('Choisir une version :\n1- 1.12.2\n2- 1.16.5\n')
        if choice == '1':
            print('Version disponible pour la 1.12.2')
            for i in list_version:
                if '1.12.2' in i:
                    print(i)
            build = input('Indiquer une version spécifique parmi celle du dessus : ')
            if not build[-1] == '/':
                build += '/'
            print(build)
            if build in list_version:
                print('Version found')
                return build
            else:
                print('Version not found')
        elif choice == '2':
            print('Version disponible pour la 1.16.5')
            for i in list_version:
                if '1.16.5' in i:
                    print(i)
            build = input('Indiquer une version spécifique parmi celle du dessus : ')
            if not build[-1] == '/':
                build += '/'
            print(build)
            if build in list_version:
                print('Version found')
                return build
            else:
                print('Version not found')
        else:
            print('Version not found')

def download_server_jar(version, path):

    version = list(version)
    del version[-1]
    version = ''.join(version)
    if '1.16.5' in version:
        name = 'spongeforge-' + version + '-universal.jar'
    else:
        name = 'spongeforge-'+version+'.jar'
    link = 'https://repo.spongepowered.org/repository/maven-releases/org/spongepowered/spongeforge/' + version + "/" + name
    print('Téléchargement... ')
    if not os.path.exists(path + 'mods/'):
        os.mkdir(path + 'mods/')
    installation_path = path + 'mods/' + name
    print("Path : " + installation_path)
    print("Link : " + link)
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0')
    opener.retrieve(link, installation_path)

def create_server():
    server_version = get_version()
    path_installation_server = library.get_installation_directory()
    download_server_jar(server_version, path_installation_server)
    print('Mise en place Forge...')
    forge_install(server_version, path_installation_server)
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

def forge_install(sponge_version, path):
    if '1.12.2' in sponge_version:
        forge_version = find_forge_version('1.12.2')
    elif '1.16.5' in sponge_version:
        forge_version = find_forge_version('1.16.5')
    else:
        raise "Error"
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

def create_batch_content(batch_path, server_version, name_server):
    dict_with_java_version = library.get_installed_java()
    # java
    while True:
        selection = input('Trouvez une version de java automatique ? (o / n) : ')
        if selection == "o":
            java_path_argument = check_java_version(dict_with_java_version)
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

def check_java_version(dict_with_java_version):
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
