import pygame
import sys
import math
from drone import Drone # On importe la classe Drone définie dans le fichier drone.py
import os


# ---------- #Paramètres de la simulation ----------


#Dimensions de la carte:
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


SEUIL_COLLISION = 10  # en pixels


#Couleur de fond de la carte:
fond_carte_rgb=(122, 122, 122)



# ---------- Initialisation Pygame ----------
pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulation tactique - Carte + drones")


# Horloge pour contrôler la fréquence d'update (FPS)
clock = pygame.time.Clock()
FPS = 60  # ou 30 pour moins charger le CPU


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Dossier où se trouve ce fichier main.py
IMAGE_DIR = os.path.join(BASE_DIR, "images") # Dossier des images (dans "Simulation tactique/images")

image_drone_ami_path = os.path.join(IMAGE_DIR, "drone_ami.png") # Chemin complet vers l'image
image_drone_ami = pygame.image.load(image_drone_ami_path).convert_alpha()

image_drone_ennemi_path = os.path.join(IMAGE_DIR, "drone_ennemi.png")
image_drone_ennemi = pygame.image.load(image_drone_ennemi_path).convert_alpha()

image_drone_surveillance_path = os.path.join(IMAGE_DIR, "drone_surveillance.png")
image_drone_surveillance = pygame.image.load(image_drone_surveillance_path).convert_alpha()


# ----------Création des drones-----------

# On crée quelques drones à des positions différentes:
drones_amis = [

    # drones bleus=intercepteurs.
    Drone(300, 200, color=(0, 0, 255)),   
    Drone(0, 280, image=image_drone_ami),  
    Drone(500, 100, image=image_drone_ami),   
    Drone(100, 500, image=image_drone_ami),   

    # drone vert=surveillance
    Drone(380, 280, vitesse=0, image=image_drone_surveillance),   
]

drones_ennemis = [
    Drone(0, 0, width=25, height=25, color=(255, 0, 0), vitesse=2, image=image_drone_ennemi),   # drone rouge
    Drone(600, 400, width=25, height=25, color=(255, 0, 0), image=image_drone_ennemi),   # drone rouge
]


# ---------- Paramétrage des drones: ----------

# On définit la cible pour notre simulation:
drone_cible=drones_ennemis[0]

# On définit qui est le drone de surveillance:
drone_surveillance=drones_amis[4]

# Et on la met en mouvement:
drone_cible.orienter_vers_drone(drone_surveillance)



# ---------- Fonction pour déterminer quel drone est le plus près de la cible: ----------
def trouver_allie_le_plus_proche(cible, drones_amis, drone_surveillance):
    """
    Retourne le drone allié (parmi drones_amis, sauf le drone_surveillance)
    qui est le plus proche de 'cible'.
    """
    meilleur_drone = None
    meilleure_distance = float("inf")

    for drone in drones_amis:
        # On ignore le drone de surveillance (vert)
        if drone is drone_surveillance:
            continue

        dist = drone.distance_vers_drone(cible)
        if dist < meilleure_distance:
            meilleure_distance = dist
            meilleur_drone = drone

    return meilleur_drone




# ---------- Boucle principale ----------

running = True
simulation_en_cours = True   # contrôle la SIMULATION (mouvements, collisions)

while running:

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Si on clique sur la croix
            running = False


    # Dessin du fond (la carte)
    window.fill(fond_carte_rgb)  # gris foncé

    if simulation_en_cours:

        # dist = drones_amis[0].distance_vers_drone(drone_cible)
        # print(dist)
        # print("")

    

        # Lancer la poursuite du drone cible:
        # On choisit le drone allié le plus proche de la cible
        drone_intercepteur = trouver_allie_le_plus_proche(drone_cible, drones_amis, drone_surveillance)

        # Lancer la poursuite du drone cible uniquement pour l'intercepteur
        for drone in drones_amis:
            if drone is drone_intercepteur:
                # Ce drone fonce vers la cible
                drone.orienter_vers_drone(drone_cible)
            else:
                # Les autres restent immobiles (pour l'instant)
                drone.vx = 0
                drone.vy = 0


        # Mise à jour des positions
        for drone in drones_amis + drones_ennemis:
            drone.update_position()


        # Test de collision ennemi / drone de surveillance
        distance_ennemi_surveillance = drone_cible.distance_vers_drone(drone_surveillance)
        if distance_ennemi_surveillance < SEUIL_COLLISION:
            print("⚠ Ennemi a atteint le drone vert -> fin de la simulation")
            simulation_en_cours = False



        # Test de collision allié / ennemi
        for drone in drones_amis:
            # On ignore le drone de surveillance
            if drone is not drone_surveillance:
                distance_allie_ennemi = drone.distance_vers_drone(drone_cible)
                if distance_allie_ennemi < SEUIL_COLLISION:
                    print("✅ Un drone allié a atteint l'ennemi -> fin de la simulation")
                    simulation_en_cours = False
                    break  # on sort de la boucle sur les alliés


    
    # Dessin des drones (on le fait meme si la simulation est arrêtée)
    for drone in drones_amis + drones_ennemis:
        drone.draw(window)


    
    pygame.display.flip() # Mise à jour de l'affichage    
    clock.tick(FPS) # Limite la boucle à FPS images par seconde

# On ferme la fenetre: sortie propre
pygame.quit()
sys.exit()
