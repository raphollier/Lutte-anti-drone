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

    # Drones ennemis:
    Drone(0, 0, color=(255, 0, 0)),   # drone rouge

    # Drones amis:
    Drone(600, 400, color=(0, 0, 255)),   # drone bleu
    Drone(300, 200, color=(0, 0, 255)),   # drone bleu
    Drone(500, 100, color=(0, 0, 255)),   # drone bleu
    Drone(100, 500, color=(0, 0, 255)),   # drone bleu

    Drone(380, 280, width=40, height=40, color=(34, 120, 15)),   # drone vert=surveillance
]


# On définit les drones qui bougent (temporaire, pour tester la mobilité des drones, mais ensuite on bougera selon les ennemis):
drone_mouvant = drones[0]  # On choisit un drone à faire bouger (par exemple le 4eme drone ami (index 3) )

# On lui donne une vitesse (en pixels par frame)
drone_mouvant.vx = 0.05
drone_mouvant.vy = 0.05


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
        drone.update_position()
        drone.draw(window)

    # Mise à jour de l'affichage
    pygame.display.flip()

# Sortie propre
pygame.quit()
sys.exit()
