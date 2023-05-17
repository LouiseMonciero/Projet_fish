from random import randint, choice
from math import atan2, cos, sin, sqrt
import pygame

 # ----------------------- CLASSES ----------------------- #
class fish:
    """ensemble des munition"""

    def __init__(self, nom, img, x, y, scale, vitesse):
        self.nom = nom
        self.speed = vitesse
        if self.nom == "sardine":
            self.poids = randint(100, 200)
            self.effects = []
        elif self.nom == "globe":
            self.poids = randint(100, 600)
            self.effects = ["grossisement"]
        elif self.nom == "sole":
            self.poids = randint(100, 250)
            self.effects = ["cole", "explosion"]
        elif self.nom == "rouge":
            self.poids = randint(100, 250)
            self.effects = ["explosion"]
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.top_left = (x, y)
        self.rect[0] = self.rect[0] + self.top_left[0]
        self.rect[1] = self.rect[1] + self.top_left[1]
        self.e_cinetique = 0.5 * self.poids * (vitesse ** 2)
    

    def modify_scale_and_weight(self, scale_multiplier, weight_multiplier): # méthode permettant d'appliquer une multiplicateur à la taille et au poid d'un poisson
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*scale_multiplier), int(self.image.get_height()*scale_multiplier)))
        self.poids /= weight_multiplier
        #self.speed *= speed_multiplier

    def get_name_poisson(self): # méthode permettant de récupérer le nom d'un poisson
        return self.nom
    def draw_fish(self, screen):
        screen.blit(self.image, self.top_left)

    # si la sole cole, il ne reste que explosion comme effect
    def get_state(self):
        """permet de connaitre l'état du poisson"""
        return self.effects

    def get_weight(self):
        """permet de connaitre son poids"""
        return self.poids

    def attribute_pos(self, x, y):
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

    def get_e_cinetique(self):
        return self.e_cinetique

    def modify_e_cinetique(self, new_ec):
        self.e_cinetique = new_ec

class bouton:
    # creer des bouttons à partir des images. Comme on en aura plusieurs,
    # https://www.youtube.com/watch?v=G8MYGDf_9ho
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
        self.center_clicked = (0, 0)  # la ou l'utilisateur aura clique sur le bouton

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        action = False
        pos = pygame.mouse.get_pos()
        # print(pos)
        if self.rect.collidepoint(pos):
            # print('ok_boutton')
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # left clicked
                #print("clicked", pos)
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:  # sinon l'action est faite plusieurs fois.
                self.clicked = False
        return action

    def draw_maintain(self, screen, area):
        # area est la variable (x1,x2, y1, y2) indiquant la zone dans laquelle peut se deplacer le bouton.
        ''' zone de lancer --> vitesse, angle'''
        screen.blit(self.image, self.rect.topleft)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.clicked == False and pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.maint = True
                self.center_clicked = (pos[0] - 100, pos[1] - 500)  # le centre de l'image du poisson !!!
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        elif self.clicked == True and (
                (pygame.mouse.get_pos()[0] >= area[0] and pygame.mouse.get_pos()[0] <= area[1]) and (
                pygame.mouse.get_pos()[1] >= area[2] and pygame.mouse.get_pos()[1] <= area[3])):
            self.rect.topleft = (pos[0] - self.center_clicked[0], pos[1] - self.center_clicked[1])
            # print(pos[0] - self.center_clicked[0])
        if self.clicked == False and self.maint == True:
            vitesse = (sqrt((100 - pos[0]) ** 2 + (500 - pos[1]) ** 2)) / 5.5  # distance par rapport à (100, 500)    est ce que je fais par rapport à pos, ou tect.topleft.
            #limite la vitesse, permet de définir une Vmax
            if vitesse > 40:
                vitesse = 35
            angle = atan2(-(500 - pos[1]), (100 - pos[0]))
            # self.rect.topleft = (pos[0] - self.center_clicked[0]+100, pos[1] - self.center_clicked[1]+500)
            return vitesse, angle

    def get_x(self):
        # print("le x en question : ", self.rect.topleft[0])
        return self.rect.topleft[0]

    def get_y(self):
        return self.rect.topleft[1]

    def get_name(self):
        return self.name

class pieces:
    def __init__(self, image, x, y):
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
        # utiliser pour colliderect() in functions draw_pieces
        # self.rect renvoi un tableau (x1 , y1, largeur , hauteur )
        t = self.rect
        return t

class bloc:
    def __init__(self, x, y, img, type):
        self.image = img
        if type == 1:
            self.type = type  # 1 (bloc) ou 2(bloc d'or)
            self.e_cinetique = 50000
        else:
            self.type = type
            self.e_cinetique = 100000
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def get_img(self):
        return self.image

    def modify_img(self, new_img):
        self.image = new_img

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_type(self):
        return self.type

    def get_rect(self):
        # self.rect renvoi un tableau (x1 , y1, largeur , hauteur )
        t = self.rect
        return t

    def get_e_cinetique(self):
        return self.e_cinetique

    def modify_e_cinetique(self, new_ec):
        self.e_cinetique = new_ec


# ----------------------- FONCITONS DIVERSES ----------------------- #
def calcul_traj(x_position, y_position, vitesse, temps_ecoule, angle, gravite):
    """Calcul la trajectoire d'un obj à partir de sa vitesse (px/s), de son angle, du temps écoulé depuis le lancer et sa direction initiale sous forme (x,y)
    Renvoie le nouveaux temps ecoule, et la nouvelle trajectoire (x, y).
    On calcul aussi l'energie cinetique du projectile
    Frottement négligés"""
    x = x_position + (vitesse * (cos(angle)) * temps_ecoule)
    y = y_position + (vitesse * (-sin(angle)) * temps_ecoule) + (0.5 * gravite * temps_ecoule ** 2)
    temps_ecoule += 0.25
    return x, y, temps_ecoule


def reduction_img(scale, image):
    width = image.get_width
    height = image.get_height()
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image


def generate_piece(n, area, image):
    """int -> tab[ pieces ]
    nombre de piece à placer sur l'ecran dans une zone delimité (x1, x2, y1, y2) """
    t = []
    for i in range(n):
        t.append((randint(area[0], area[1]), randint(area[2], area[3])))
        t[i] = pieces(image, t[i][0], t[i][1])
        # screen.blit(image , (t[i]))
    return t


def draw_pieces(screen, t, projectile, n_score):
    # cette fonction ne peut pas etre integrer dans la classe pices en raison de la boucle
    """tab[ pieces ] -> tab[ pieces ]
    blit les pieces sur l'écran, vérifie si le joueur ne ramasse pas une pièce """
    t_new = []
    for i in range(len(t)):
        screen.blit(t[i].get_img(), t[i].get_topleft())  # blit ( image , (x ,y ))
        if projectile != None:
            # print('poisson :', projectile.get_rect(), 'piece', i + 1, ':', t[i].get_rect())
            if pygame.Rect.colliderect(t[i].get_rect(), projectile.get_rect()):
                #print("Le poisson doit recuperer la piece n°", i + 1)
                n_score += 1
            else:
                t_new.append(t[i])
        else:
            t_new.append(t[i])
    return t_new, n_score



# ----------------------- FONCTIONS DE LA MATRICE DE LA ZONE CASSABLE ----------------------- #
def print_mat(M):
    for i in range(8):
        for j in range(6):
            print(M[i][j], end=" ")
        print("")


def create_mat_initial(nb_bloc, chance_or):
    """Créer la matrice représentant la zone cassable.
    0: Pas de bloc à cet emplacement
    1: Un bloc à cet emplacement
    2: Une brique d'or à cet emplaement"""

    M = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # M= [[0]*6]   -> La modification d'un case se repercute sur toute la colonne.
    cpt_bloc = 0
    c_or = 0
    L_indice = []
    for i in range(11):
        for j in range(7):
            L_indice.append((i, j))
    while (cpt_bloc < nb_bloc):
        case = choice(L_indice)
        L_indice.remove(case)
        M[case[0]][case[1]] = 1
        if randint(0, 100) < chance_or:
            M[case[0]][case[1]] = 2
            c_or += 1
        cpt_bloc += 1
    #print(c_or)
    return M


def draw_mat(screen, M_bloc, projectile, image_bloc_casse, score, n_tir, a_joueur, nb_joueur, diff):  # (x1 , x2 , y1 , y2)
    """ M -> M : renvoie la nouvelle matrice, si le poisson à casser des blocs, la matrice renvoyé sera différente."""
    for i in range(11):
        for j in range(7):
            if M_bloc[i][j] != None:
                # print("Object")
                screen.blit(M_bloc[i][j].get_img(),
                            (M_bloc[i][j].x, M_bloc[i][j].y))  # -> None type has no attributes image.
                # screen.blit( projectile.get_img() , ( M_bloc[i][i].x , M_bloc[i][i].y )) #-> ne marche pas non plus
                # screen.blit( image, ( M_bloc[i][i].get_x() , M_bloc[i][i].get_y() ))
                if (projectile != None):
                    #print("Le poisson est detecté par draw mat, e cin : ", projectile.get_e_cinetique())
                    if pygame.Rect.colliderect(M_bloc[i][j].get_rect(), projectile.get_rect()):
                        casse = 0
                        if (projectile.get_e_cinetique() - M_bloc[i][j].get_e_cinetique()) <= 0:  # si le bloc a plus d'energie que le poisson
                            M_bloc[i][j].modify_e_cinetique(M_bloc[i][j].get_e_cinetique() - projectile.get_e_cinetique())
                            projectile = None
                            if (diff != 0):
                                n_tir -= 1
                            else :
                                n_tir += 1
                            if M_bloc[i][j].get_type() == 1:
                                M_bloc[i][j].modify_img(image_bloc_casse)
                            if (a_joueur == nb_joueur - 1):
                                a_joueur = 0
                            else:
                                a_joueur = a_joueur + 1

                        else:
                            projectile.modify_e_cinetique(projectile.get_e_cinetique() - M_bloc[i][j].get_e_cinetique())
                            casse = 1
                        #print("Le poisson  est sur un bloc")
                        if casse == 1:
                            if M_bloc[i][j].get_type() == 1:
                                #print(" le bloc cassé est normal")
                                score += 1
                            elif M_bloc[i][j].get_type() == 2:
                                #print(" le bloc cassé est d'or")
                                score += 5
                            M_bloc[i][j] = None
    return M_bloc, projectile, score, n_tir, a_joueur


def create_mat_bloc(img_bloc, img_bloc_or, M):

    M_bloc = [[None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None]]
    for i in range(11):
        for j in range(7):
            x = 600 + i * 50
            y = 200 + j * 50
            if M[i][j] == 1:
                M_bloc[i][j] = bloc(x, y, img_bloc, 1)  # energie cinetique basse.
                # print( M_bloc[i][j].get_x())
            elif M[i][j] == 2:
                M_bloc[i][j] = bloc(x, y, img_bloc_or, 2)  # energie cinetique haute.
            else:
                M[i][j] = None
    return M_bloc


def test():
    b = bloc(10, 20, "image", 2)
    print(b.get_x())

# test()
# pos = pygame.mouse.get_pos()
# .collidepoint(pos)

def matrice_nb_bloc(mat):
    nb_bloc = 0
    for i in range(8):
        for j in range(7):
            if mat[i][j] != None:
                nb_bloc += 1
    return nb_bloc

def print_score(screen, nb_joueur, score, police):
    if (nb_joueur == 1):  # si il n'y a que un joueur n'affiche pas score joueur 1 : mais juste le score
        screen.blit(police.render(str(score[0]), 1, (0, 0, 0)), (260, 20))
    else:
        screen.blit(police.render("joueur 1 :", 1, (0, 0, 0)), (260, 20))
        screen.blit(police.render(str(score[0]), 1, (0, 0, 0)), (325, 20))
    if (nb_joueur >= 2):
        screen.blit(police.render("joueur 2 :", 1, (0, 0, 0)), (390, 20))
        screen.blit(police.render(str(score[1]), 1, (0, 0, 0)), (455, 20))
    if (nb_joueur >= 3):
        screen.blit(police.render("joueur 3 :", 1, (0, 0, 0)), (520, 20))
        screen.blit(police.render(str(score[2]), 1, (0, 0, 0)), (585, 20))
    if (nb_joueur >= 4):
        screen.blit(police.render("joueur 4 :", 1, (0, 0, 0)), (650, 20))
        screen.blit(police.render(str(score[3]), 1, (0, 0, 0)), (715, 20))
    if (nb_joueur >= 5):
        screen.blit(police.render("joueur 5 :", 1, (0, 0, 0)), (770, 20))
        screen.blit(police.render(str(score[4]), 1, (0, 0, 0)), (835, 20))

def print_gameover(screen, nb_joueur, score):
    go_img = pygame.image.load("images/game_over.png").convert_alpha()
    go = pygame.transform.scale(go_img, (1000, 700))
    screen.blit(go, (0, 0))

    winner_is = -1  # personne ne gagne si tous les scores sont à zero
    max_score = 0
    current_player = 0
    while (current_player < nb_joueur):
        if (score[current_player] > max_score):
            winner_is = current_player
            max_score = score[current_player]
        current_player += 1

    go_police = pygame.font.SysFont("bold", 60)
    if (winner_is == -1):
        screen.blit(go_police.render("Vous avez perdu !", 1, (255, 255, 255)), (200, 40))
    else:
        if (nb_joueur != 1):
            screen.blit(go_police.render(f"Le joueur {winner_is + 1} a gagné !", 1, (255, 255, 255)), (200, 40))
        else:
            screen.blit(go_police.render("Vous avez gagné !", 1, (255, 255, 255)), (200, 40))

    screen.blit(go_police.render(f"Appuyer sur une touche pour continuer", 1, (255, 255, 255)), (100, 100))
    pygame.display.flip()

    timer = pygame.time.Clock()
    waiting = True
    while waiting:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
