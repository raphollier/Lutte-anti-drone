import pygame
import sys
import math
from drone import Drone # On importe la classe Drone définie dans le fichier drone.py


# ---------- #Paramètres de la simulation ----------


#Dimensions de la carte:
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


#Couleur de fond de la carte:
fond_carte_rgb=(255, 255, 255)


# On crée quelques drones à des positions différentes:

drones_amis = [
    Drone(50, 50, color=(0, 0, 255)),   # drone bleu=intercepteur
    Drone(300, 200, color=(0, 0, 255)),  
    Drone(500, 100, color=(0, 0, 255)),   
    Drone(100, 500, color=(0, 0, 255)),   

    Drone(380, 280, width=40, height=40, vitesse=0, color=(34, 120, 15)),   # drone vert=surveillance
]

drones_ennemis = [
    Drone(300, 400, color=(255, 0, 0)),   # drone rouge
    Drone(600, 400, color=(255, 0, 0)),   # drone rouge
]

# On définit la cible pour notre simulation:
drone_cible=drones_ennemis[0]


# ---------- Initialisation Pygame ----------
pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulation tactique - Carte + drones")



# ---------- Boucle principale ----------


def orienter_drone_vers_cible(drone_source, drone_cible, vitesse):
    """
    Calcule un vecteur de direction de drone_source vers drone_cible
    et met à jour vx, vy pour que drone_source se dirige vers drone_cible.

    """
    # Différence de position
    dx = drone_cible.x - drone_source.x
    dy = drone_cible.y - drone_source.y

    # Distance entre les deux drones
    distance = math.hypot(dx, dy)  # équivalent à sqrt(dx*dx + dy*dy)

    if distance == 0:
        # Les deux drones sont au même endroit → pas de mouvement
        drone_source.vx = 0
        drone_source.vy = 0
    else:
        # On normalise le vecteur (dx, dy) pour en faire un vecteur de longueur 1
        nx = dx / distance
        ny = dy / distance

        # On multiplie par la vitesse voulue
        drone_source.vx = nx * vitesse
        drone_source.vy = ny * vitesse



running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Dessin du fond (la carte)
    window.fill(fond_carte_rgb)  # gris foncé
   

    # Lancer la poursuite du drone cibble:
    for drone in drones_amis:
        orienter_drone_vers_cible(drone, drone_cible, drone.vitesse)


    # Dessin des drones
    for drone in drones_amis + drones_ennemis:
        drone.update_position()
        drone.draw(window)

    # Mise à jour de l'affichage
    pygame.display.flip()

# Sortie propre
pygame.quit()
sys.exit()
