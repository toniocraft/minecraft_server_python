import vanilla
import forge
import fabricmc
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
        # https://mohistmc.com/api
        # https://repo.spongepowered.org/#browse/browse:maven-releases:org%2Fspongepowered%2Fspongeforge
        pass
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
        # https://glowstone.net/#downloads
        # https://getbukkit.org/download/
        # https://papermc.io/downloads -> https://api.papermc.io/v2/projects/paper donne une liste de version donc...
        # ...récupérer la version la plus basse et la plus haute
        pass
    elif selection == '4':
        # Vanilla
        vanilla.create_server()
    elif selection == '5':
        exit()
    else:
        print('Choix incorrect')
