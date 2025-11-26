import pygame

class Drone:
    def __init__(self, x, y, width=20, height=20, color=(0, 255, 0)):
        """
        Représente un drone sur la carte.

        x, y : position (en pixels) du coin supérieur gauche
        width, height : taille du rectangle
        color : couleur du drone (RGB)
        """

        #On définit ici tous les attributs que possèdent un objet "Drone":
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
        self.name="nom_test"

        # Vitesse du drone (en pixels par frame)
        self.vx = 0
        self.vy = 0


    def draw(self, surface):
        """
        Dessine le drone sous forme de rectangle sur la surface donnée.
        surface : par exemple la fenêtre Pygame (window)
        """
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)


    def update_position(self):
        """
        Met à jour la position du drone en fonction de sa vitesse.
        """
        self.x += self.vx
        self.y += self.vy