import pygame
import sys
from drone import Drone # On importe la classe Drone définie dans le fichier drone.py


# ---------- #Paramètres de la simulation ----------

#Dimensions de la carte:
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


#Couleur de fond de la carte:
fond_carte_rgb=(255, 255, 255)



# On crée quelques drones à des positions différentes
drones = [
    Drone(100, 100, color=(0, 255, 0)),   # drone vert
    Drone(300, 200, color=(0, 0, 255)),   # drone bleu

    Drone(380, 280, width=40, height=40, color=(0, 255, 0)),   # drone vert=surveillance
]



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

    # Dessin des drones
    for drone in drones:
        drone.draw(window)

    # Mise à jour de l'affichage
    pygame.display.flip()

# Sortie propre
pygame.quit()
sys.exit()
