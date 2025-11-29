import pygame
import sys
from drone import Drone # On importe la classe Drone définie dans le fichier drone.py
import os
#import math


# ---------- #Paramètres de la simulation ----------

#Couleur de fond de la carte:
fond_carte_rgb=(0, 0, 0)

#Dimensions de la carte en pixels:
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Paramètres de la grille de la carte
CELL_SIZE = 40  # taille d'une case en pixels
GRID_COLS = WINDOW_WIDTH // CELL_SIZE  # 800 / 40 = 20 colonnes
GRID_ROWS = WINDOW_HEIGHT // CELL_SIZE # 600 / 40 = 15 lignes


# Seuil de collision entre les drones (ou autres éléments):
SEUIL_COLLISION = 5  # en pixels


# ---------- Initialisation Pygame ----------
pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulation tactique")


# Horloge pour contrôler la fréquence d'update (FPS)
clock = pygame.time.Clock()
FPS = 60  # ou 30 pour moins charger le CPU



# ----------Création des images ----------


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Dossier où se trouve ce fichier main.py
IMAGE_DIR = os.path.join(BASE_DIR, "images") # Dossier des images (dans "Simulation tactique/images")


def charger_image(chemin_dossier_images, nom_image):
    image_path = os.path.join(chemin_dossier_images, nom_image) # Chemin complet vers l'image
    return pygame.image.load(image_path).convert_alpha()


image_drone_ami=charger_image(IMAGE_DIR, "drone_ami.png")
image_drone_ennemi=charger_image(IMAGE_DIR, "drone_ennemi.png")
image_drone_surveillance=charger_image(IMAGE_DIR, "drone_surveillance.png")



# ---------- Création de la matrice pour la carte: ----------

# On initialise toute la carte à 0 (zone neutre)
carte_zones = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

# Pour le test : on définit une zone à protéger (un bloc de cases en bas à droite)
for row in range(9, GRID_ROWS):      # lignes 9 à 14
    for col in range(12, GRID_COLS): # colonnes 12 à 19
        carte_zones[row][col] = 1 # 1 pour les zones à protéger



# ----------Création des drones-----------

# On crée quelques drones à des positions différentes:
drones_amis = [

    # drones bleus=intercepteurs.
    Drone(300, 220, color=(0, 0, 255)),   
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


# On renseigne qui est le drone de surveillance:
drone_surveillance=drones_amis[4]


# On met la cible en mouvement:
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
        # On ignore le drone de surveillance (vert):
        if drone is not drone_surveillance:
            dist = drone.distance_vers_drone(cible)
            if dist < meilleure_distance:
                meilleure_distance = dist
                meilleur_drone = drone
    return meilleur_drone



def draw_carte(surface, carte):
    """
    Dessine la carte en arrière-plan :
    - grille légère
    - zones à protéger en vert clair
    """
    # Couleurs
    couleur_grille = "#645619"
    couleur_zone_protegee ="#7FBD41"

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # Dessiner la grille (juste le contour)
            pygame.draw.rect(surface, couleur_grille, rect, 0) # Dernier arugment: 1 pour juste contour, 0 pour toute la case

            # Si c'est une zone à protéger, on remplit la case
            if carte[row][col] == 1:
                pygame.draw.rect(surface, couleur_zone_protegee, rect, 0) # Dernier arugment: 1 pour juste contour, 0 pour toute la case





# ---------- Boucle principale ----------

running = True
simulation_en_cours = True   # contrôle la SIMULATION (mouvements, collisions)

while running: # Tant que la fenetre est ouverte

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Si on clique sur la croix
            running = False


    # Dessin du fond (la carte):
    window.fill(fond_carte_rgb)  # gris foncé

    # Dessin de la carte (grille + zones):
    draw_carte(window, carte_zones)


    if simulation_en_cours: # Tant que la simulation est en cours

        dist = drones_amis[0].distance_vers_drone(drone_cible)
        print(dist)
        print("")

    

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
