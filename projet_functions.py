from random import randint
from math import atan2, cos, sin, sqrt
import pygame


class fish :
    """ensemble des munition"""
    def __init__(self, nom, img, x, y, scale):
        self.nom = nom
        if self.nom =='sardine':
            self.poids = randint(10,30)
            self.effects = []
        elif self.nom == "globe":
            self.poids = randint(100,600)
            self.effects = ["grossisement"]
        elif self.nom == "sole":
            self.poids = randint(100,250)
            self.effects = ["cole","explosion"]
        elif self.nom == "rouge":
            self.poids = randint(100, 250)
            self.effects = ["explosion"]
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.top_left = (x, y)
        self.rect[0] = self.rect[0] + self.top_left[0]
        self.rect[1] = self.rect[1] + self.top_left[1]
        print("Mon poisson a les coordonées (topleft): ", self.top_left )

    def draw_fish(self, screen):
        screen.blit(self.image, self.top_left)
   #si la sole cole, il ne reste que explosion comme effect


    def get_state(self):
        """permet de connaitre l'état du poisson"""
        return self.effects

    def get_weight(self):
        """permet de connaitre son poids"""
        return self.poids

    def attribute_pos (self,x,y):
        """permet d'attribuer une nouvelle position au poisson"""
        self.rect = self.image.get_rect()
        self.top_left = (x, y)
        self.rect[0] = self.rect[0] + self.top_left[0]
        self.rect[1] = self.rect[1] + self.top_left[1]

    def get_x(self):
        return self.top_left[0]
    
    def get_y(self):
        return self.top_left[1]
    
    def get_rect(self):
        "utiliser pour colliderect() in functions draw_pieces"
        t = self.rect
        return t

class bouton :
    #creer des bouttons à partir des images. Comme on en aura plusieurs,
    #https://www.youtube.com/watch?v=G8MYGDf_9ho
    """difference entre .image et .__image ???"""
    def __init__(self, x, y, img, scale, name):
        longueur = img.get_width()
        largeur = img.get_height()
        self.image = pygame.transform.scale(img, (int(longueur * scale), int(largeur * scale)))
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.maint = False
        self.center_clicked = (0,0)   # la ou l'utilisateur aura clique sur le bouton

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        action = False
        pos = pygame.mouse.get_pos()
        #print(pos)
        if self.rect.collidepoint(pos):
            #print('ok_boutton')
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False :     #left clicked
                print("clicked",pos)
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:      #sinon l'action est faite plusieurs fois.
                self.clicked = False
        return action
    
    def draw_maintain(self, screen, area):
        #area est la variable (x1,x2, y1, y2) indiquant la zone dans laquelle peut se deplacer le bouton.
        ''' zone de lancer --> vitesse, angle'''
        screen.blit(self.image, self.rect.topleft)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.clicked == False and pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.maint = True
                self.center_clicked = (pos[0]-100 , pos[1]-500)   #le centre de l'image du poisson !!!
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        elif self.clicked == True and ((pygame.mouse.get_pos()[0]>= area[0] and pygame.mouse.get_pos()[0]<=area[1]) and (pygame.mouse.get_pos()[1]>=area[2] and pygame.mouse.get_pos()[1]<=area[3])):
            self.rect.topleft = (pos[0] - self.center_clicked[0], pos[1] - self.center_clicked[1])
            print(pos[0] - self.center_clicked[0])
        if self.clicked == False and self.maint == True :
            vitesse = ( sqrt((100-pos[0])**2+(500-pos[1])**2) ) /5.5 #distance par rapport à (100, 500)    est ce que je fais par rapport à pos, ou tect.topleft.
            angle =  atan2( -(500-pos[1]) , (100-pos[0]) )
            #self.rect.topleft = (pos[0] - self.center_clicked[0]+100, pos[1] - self.center_clicked[1]+500)
            return vitesse, angle
        
    def get_x (self):
        print("le x en question : ", self.rect.topleft[0])
        return self.rect.topleft[0]
    
    def get_y (self):
        return self.rect.topleft[1]
    
    def get_name (self):
        return self.name




def calcul_traj( x_position, y_position , vitesse, temps_ecoule, angle, gravite):
    """Calcul la trajectoire d'un obj à partir de son poids (g), sa vitesse (px/s), et sa direction initiale sous forme (x,y)
    renvoie sa vitesse (px/s), sa direction.
    Frottement négligés"""
    x = x_position + (vitesse * (cos(angle)) * temps_ecoule)
    y = y_position + (vitesse * (-sin(angle)) * temps_ecoule) + (0.5 * gravite * temps_ecoule ** 2)
    temps_ecoule += 0.25
    return x,y, temps_ecoule

def reduction_img(scale,image):
    width = image.get_with
    height = image.get_height()
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image


def generate_piece (n, area, image):
        """int -> tab[ pieces ]
        nombre de piece à placer sur l'ecran dans une zone delimité (x1, x2, y1, y2) """
        t = []
        for i in range(n):
            t.append((randint(area[0],area[1]),randint(area[2],area[3])))
            t[i] = pieces(image , t[i][0], t[i][1] )   
            #screen.blit(image , (t[i]))
        return t


class pieces : 
    def __init__(self, image , x, y):
        self.img = image
        self.rect = self.img.get_rect()
        self.top_left = (x, y)
        self.rect[0] = self.rect[0] + self.top_left[0]
        self.rect[1] = self.rect[1] + self.top_left[1]

    def get_img(self):
        return self.img
    
    def get_topleft(self):
        return self.top_left
    
    def get_rect(self):
        "Renvoie le rectangle de la pièce"
        #utiliser pour colliderect() in functions draw_pieces
        # self.rect renvoi un tableau (x1 , y1, largeur , hauteur )
        t = self.rect
        return t
    

def draw_pieces ( screen , t , projectile, n_score):
    # cette fonction ne peut pas etre integrer dans la classe pices en raison de la boucle 
    """tab[ pieces ] -> tab[ pieces ] 
    blit les pieces sur l'écran, vérifie si le joueur ne ramasse pas une pièce """
    t_new = []
    for i in range (len(t)):
        screen.blit(t[i].get_img() , t[i].get_topleft())
        if projectile != None :
            print('poisson :' ,projectile.get_rect( ) , 'piece', i+1 ,':', t[i].get_rect() )
            if pygame.Rect.colliderect(t[i].get_rect(), projectile.get_rect()) :
                print("Le poisson doit recuperer la piece n°",i+1 )
                n_score += 1
            else : 
                t_new.append( t[i] )
        else : 
            t_new.append(t[i])
    return t_new , n_score

#pos = pygame.mouse.get_pos()
#.collidepoint(pos)