import pygame
import math

class Drone:
    def __init__(self, x, y, width=20, height=20, vitesse=0.1, color=(0, 255, 0)): # Par défaut: une certaine hauteur/largeur, vitesse, couleur
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
        self.vitesse = vitesse # Vitesse de déplacement du drone en mouvement(en pixels par frame) (le drone peut etre à l'arret, sa vitesse ne changera pas, mais ses vecteurs direction oui)
        self.color = color

        # Vecteurs vitesses initiaux:
        self.vx=0
        self.vy=0


    # ----------- Méthodes indispensable pour simuler le drone:--------------


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


# ----------- Autres méthodes:--------------

    def orienter_vers_position(self, cible_x, cible_y):
        """
        Oriente ce drone vers une position (cible_x, cible_y)
        en réglant vx et vy à partir de self.vitesse.
        """
        dx = cible_x - self.x
        dy = cible_y - self.y

        distance = math.hypot(dx, dy)

        if distance == 0:
            # On est déjà sur la cible
            self.vx = 0
            self.vy = 0
            return

        # vecteur directionnel de longueur 1
        nx = dx / distance
        ny = dy / distance

        # on applique la vitesse scalaire du drone
        self.vx = nx * self.vitesse
        self.vy = ny * self.vitesse



    def orienter_vers_drone(self, autre_drone):
        """
        Oriente ce drone vers un autre drone (autre_drone).
        """
        self.orienter_vers_position(autre_drone.x, autre_drone.y)



    def distance_vers_drone(self, autre_drone):
        """
        Retourne la distance entre ce drone et un autre drone.
        """
        dx = autre_drone.x - self.x
        dy = autre_drone.y - self.y
        
        distance=math.hypot(dx, dy)#racine de la somme des carrés

        return distance
