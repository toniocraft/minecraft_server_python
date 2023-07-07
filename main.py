import spongeforge
import mohist
import papermc
import vanilla
import forge
import fabricmc
# crucible/thermos pour mods et plugins ??
list_type_server = "1. Mods & Plugins" \
                   "2. Mods" \
                   "3. Plugins" \
                   "4. Vanilla"

print('---Création de serveur Minecraft---')
while True:
    print('Choisissez le type de serveur que vous souhaitez créer :')
    print("1-Mods & Plugins\n2-Mods\n3-Plugins\n4-Vanilla\n5-Exit")
    selection = input('Entrez un nombre (1, 2, 3, 4 ou 5) : ')
    if selection == '1':
        # Mods & Plugins
        while True:
            print('1- Mohist\n2- SpongeForge\n3- Retour')
            selection = input("Quel type de serveur modded voulez vous ? (1, 2 ou 3) : ")
            if selection == "1":
                mohist.create_server()
            elif selection == "2":
                spongeforge.create_server()
            elif selection == "3":
                break
            else:
                print('Choix incorrect')
    elif selection == '2':
        # Mods
        while True:
            print('1- Forge\n2- FabricMC\n3- Retour')
            selection = input("Quel type de serveur modded voulez vous ? (1, 2 ou 3) : ")
            if selection == "1":
                forge.create_server()
            elif selection == "2":
                fabricmc.create_server()
            elif selection == "3":
                break
            else:
                print('Choix incorrect')
    elif selection == '3':
        # Plugins
        while True:
            print('1- PaperMC\n2- Glowstone\n3- Spigot/Bukkit\n4- Retour')
            selection = input("Quel type de serveur avec plugin voulez vous ? (1, 2 ou 3) : ")
            if selection == "1":
                papermc.create_server()
            elif selection == "2":
                print("Soon")
            elif selection == "3":
                print("Soon")
            elif selection == "4":
                break
            else:
                print('Choix incorrect')
        # https://glowstone.net/#downloads
        # https://getbukkit.org/download/
        pass
    elif selection == '4':
        # Vanilla
        vanilla.create_server()
    elif selection == '5':
        exit()
    else:
        print('Choix incorrect')
