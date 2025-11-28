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

    # drones bleus=intercepteurs
    Drone(50, 50, color=(0, 0, 0)),   
    Drone(300, 200, color=(0, 0, 255)),  
    Drone(500, 100, color=(0, 0, 255)),   
    Drone(100, 500, color=(0, 0, 255)),   

    # drone vert=surveillance
    Drone(380, 280, width=40, height=40, vitesse=0, color=(34, 120, 15)),   
]

drones_ennemis = [
    Drone(0, 300, color=(255, 0, 0), vitesse=0.08),   # drone rouge
    Drone(600, 400, color=(255, 0, 0)),   # drone rouge
]

# On définit la cible pour notre simulation:
drone_cible=drones_ennemis[0]

# Et on la met en mouvement:
drone_cible.orienter_vers_drone(drones_amis[4])


# ---------- Initialisation Pygame ----------
pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulation tactique - Carte + drones")



# ---------- Boucle principale ----------

running = True

while running:

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Dessin du fond (la carte)
    window.fill(fond_carte_rgb)  # gris foncé



    dist = drones_amis[0].distance_vers_drone(drone_cible)
    print(dist)
    print("")

   

    # Lancer la poursuite du drone cibble:
    for drone in drones_amis:
        drone.orienter_vers_drone(drone_cible)


    # Dessin des drones
    for drone in drones_amis + drones_ennemis:
        drone.update_position()
        drone.draw(window)

    # Mise à jour de l'affichage
    pygame.display.flip()

# Sortie propre
pygame.quit()
sys.exit()
