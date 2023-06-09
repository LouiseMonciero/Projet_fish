import pygame_menu  # https://github.com/ppizarror/pygame-menu
import sys
import pygame
from projet_functions import *

diff = 1
nb_joueur = 1
pseudo = "pseudo"  # si pas de pseudo saisie

para_jeu = [(7, float('inf'), 20, 30), (5, 20, 15, 35), (3, 10, 10, 50)]  # (nb_pieces , nombre de tir , chance d'avoir brique_or / brique , nb_briques)


def start_the_game():
    """Fonction du jeu entier, elle charge toutes les images et comprends la boucle du jeu"""
    global para_jeu

    # MON ECRAN
    screen = pygame.display.set_mode((1000, 700))  # largeur hauteur

    # MES IMAGES
    mer_img = pygame.image.load("images/mer.png").convert_alpha()
    sable_img = pygame.image.load("images/sable.png").convert_alpha()
    depart_gd = pygame.image.load("images/lance_pierre.png").convert_alpha()

    sardine_img = pygame.image.load("images/saumon.png").convert_alpha()
    globe_img = pygame.image.load("images/globe.png").convert_alpha()
    rouge_img = pygame.image.load("images/poisson_rouge.png").convert_alpha()

    # button_img = pygame.image.load("images/bouton.png").convert_alpha()
    piece_img_gr = pygame.image.load("images/piece.png").convert_alpha()
    brique_img = pygame.image.load("images/brique.png").convert_alpha()
    bloc_or_img = pygame.image.load("images/bloc_or.png").convert_alpha()
    brique_casse_img = pygame.image.load("images/brique_casse.png").convert_alpha()
    fumee_img = pygame.image.load("images/fumee.png").convert_alpha()

    mer = pygame.transform.scale(mer_img, (1000, 614))
    piece_img = pygame.transform.scale(piece_img_gr, (piece_img_gr.get_width() * 0.1, piece_img_gr.get_height() * 0.1))

    # MES SURFACES
    screen.blit(mer, (0, 0))

    # MES RECTANGLES
    bandeau_rect = pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(30, 30, 60, 60))

    sable = pygame.transform.scale(sable_img, (1000, 100))
    depart = pygame.transform.scale(depart_gd, (75, 75))


    # MES BOUTTONS
    sardine = bouton(20, 50, sardine_img, 0.1, '')
    globe = bouton(20, 110, globe_img, 0.05, '')
    rouge = bouton(20, 175, rouge_img, 0.1, '')
    # button_lancer = bouton(10, 525, button_img, 0.1, '')

    # VARIABLES
    projectile = None  # quand le poisson est en l'air
    munition = None  # quand le poisson est sur la zone de départ
    para_lancer = None  # (vitesse , angle )

    score = [0] * nb_joueur

    n_tir = [0] * nb_joueur
    for i in range (len(n_tir)):
        if diff == 0:
            n_tir[i] = 0
        else :
            n_tir[i] = para_jeu[diff][1]

    nb_grossissement = None  # permet de donner un nombre maximal de grossissement à globe en vérifiant si cette valeur est strictement supérieure à 0

    timer = pygame.time.Clock()
    game_on = True

    # variables trajectoire
    x_position = None
    y_position = None
    vitesse = None
    angle = None
    temps_ecoule = 0
    gravite = 0.7
    e_cinetique = 0

    # MES TEXTES
    police = pygame.font.SysFont("bold", 20)  # prend en parametre le police d'écriture et la taille.
    image_score = police.render("SCORE :", 1, (0, 0, 0))  # (0,0,0) est le code RGB.
    image_n_tir = police.render("NOMBRE DE TIR :", 1, (0, 0, 0))

    # MES PIECES
    nb_pieces = para_jeu[diff][0]
    tab_pieces = [0]*nb_joueur # créé un tableau de la taille du nb_joueur pour avoir pour chaque joueur les pièces correspondante
    M_piece = generate_piece(nb_pieces, (100, 1000, 0, 500), piece_img)
    for i in range (len(tab_pieces)):
        tab_pieces[i] = M_piece # initialise pour chaque joueur les meme pièces au debut

    # MES BLOCS
    M = create_mat_initial(para_jeu[diff][3], para_jeu[diff][2]) # nb_bloc, chance_or
    Mat_bloc_j = [0]*nb_joueur # créé un tableau de la taille du nb_joueur pour avoir pour chaque joueur la matrice des blocs
    for i in range (len(Mat_bloc_j)):
        Mat_bloc_j[i] = create_mat_bloc(brique_img, bloc_or_img, M) # initialise pour chaque joueur la meme matrice de bloc au début


    # MES JOUEURS
    Mes_joueurs = [0] * nb_joueur  # initialisation d'un tableau contenant les indices des joueurs
    for i in range(len(Mes_joueurs)):
        Mes_joueurs[i] = i
    a_joueur = 0 #initialisation de l'indice du joueur a qui est le tour

    police_joueur = pygame.font.SysFont("bold", 40)
    image_joueur = police_joueur.render("Au tour du joueur ", 1, (0, 0, 0))

    # SOUNDS
    punch_sound = pygame.mixer.Sound('sounds/PUNCH.wav')
    punch_sound.set_volume(0.1)
    applause_sound = pygame.mixer.Sound('sounds/applause10.wav')
    missed_sound = pygame.mixer.Sound('sounds/missed.wav')
    missed_sound.set_volume(0.1)

    old_score = [0] * nb_joueur

    while game_on:
        screen.blit(mer, (0, 0))
        # ------------quitter le jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # vérification si la touche "e" a été appuyée
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and projectile is not None and projectile.get_name_poisson() == "globe" and nb_grossissement > 0: # vérifie si le projectile en cours d'utilisation est "globe" et si la touche "e" est appuyée
                nb_grossissement -= 1 # enlève un grossissement à "globe", est réinitialisé à une valeur donnée à chaque fois que "globe" est sélectionné
                projectile.modify_scale_and_weight(2,0.25) # augmente la taille de "globe" par 2 et son poid par 4


        # -------------place les surfaces
        screen.blit(sable, (0, 600))  # coin supp gauche
        screen.blit(depart, (100, 525))

        #--------------place les textes
        screen.blit(image_n_tir, (40, 20))
        screen.blit(police.render(str(n_tir[a_joueur]), 1, (0, 0, 0)), (160, 20))

        if (nb_joueur != 1) : #si plus de 1 joueur affiche a quel joueur est le tour
            screen.blit(image_joueur, (40, 635))
            screen.blit(police_joueur.render(str(a_joueur + 1), 1, (0, 0, 0)), (290, 635))

        screen.blit(image_score, (200, 20))

        if (((diff != 0 and n_tir[a_joueur] > 0) or diff == 0) and (len(tab_pieces[a_joueur]) + matrice_nb_bloc(Mat_bloc_j[a_joueur])) > 0):
            print_score(screen, nb_joueur, score, police)
        else:
            print_gameover(screen, nb_joueur, score)
            game_on = False

        # ------------place les pièces

        tab_pieces[a_joueur], score[a_joueur] = draw_pieces(screen, tab_pieces[a_joueur], projectile, score[a_joueur], applause_sound)

        # ------------place les blocs
        Mat_bloc_j[a_joueur], projectile , score[a_joueur] , n_tir[a_joueur], a_joueur, old_score[a_joueur] = draw_mat(screen, Mat_bloc_j[a_joueur], projectile, brique_casse_img ,score[a_joueur], n_tir[a_joueur], a_joueur, nb_joueur, diff, punch_sound, old_score[a_joueur])  # (x1 , x2 , y1 , y2 )



        # ------------place les boutons

        if sardine.draw(screen) and projectile == None:
            x = 100
            y = 500
            #print('sardine clicked')
            munition = bouton(100, 500, sardine_img, 0.1, 'sardine')

        if globe.draw(screen) and projectile == None:
            x = 100
            y = 500
            #print('globe clicked')
            munition = bouton(100, 500, globe_img, 0.05, 'globe')
            # munition = fish("globe", globe_img, 100, 500, 0.1)
            nb_grossissement = 1  # permet de donner un nombre maximal de grossissement à globe en vérifiant si cette valeur est strictement supérieure à 0

        if rouge.draw(screen) and projectile == None:
            x = 100
            y = 500
            #print('rouge clicked')
            munition = bouton(100, 500, rouge_img, 0.15, 'rouge')
            # munition = fish("rouge", rouge_img, 100, 500, 0.15)

        # -------------variables de lancer/tir
        if munition != None:
            para_lancer = munition.draw_maintain(screen, (0, 250, 375, 700))  #para_lancer (vitesse , angle)

        if munition != None and para_lancer != None:
            temps_ecoule = 0
            x_position = munition.get_x()
            y_position = munition.get_y()
            if (y_position > 600):
                depasse_sol = False
            else:
                depasse_sol = None
            if munition.get_name() == 'sardine':
                projectile = fish("sardine", sardine_img, x_position, y_position, 0.1 , para_lancer[0])
                # projectile = fish("sardine", sardine_img, 100, 500, 0.3)
            elif munition.get_name() == 'globe':
                projectile = fish("globe", globe_img, x_position, y_position, 0.05,  para_lancer[0])
            elif munition.get_name() == 'rouge':
                projectile = fish("rouge", rouge_img, x_position, y_position, 0.15,  para_lancer[0])
            vitesse = para_lancer[0]
            angle = para_lancer[1]
            para_lancer = None
            munition = None

        if munition == None and projectile != None:
            projectile.draw_fish(screen)
            if ((y < 600) or depasse_sol == False) and (y > 0) and (x>-200) and (x<1200):
                x, y, temps_ecoule = calcul_traj(x_position, y_position, vitesse, temps_ecoule, angle, gravite)
                #print("x =", x)
                projectile.attribute_pos(x, y)
            else:
                projectile = None                    # disparition du poisson !!!!!!!
                if old_score[a_joueur] == score[a_joueur]:               # le poisson n'a rien touché
                    missed_sound.play()
                else:
                    old_score[a_joueur] = score[a_joueur]
                if diff != 0: #si le poisson est sorti de l'ecran le nombre de tire diminue et ca passe au joueur suivant sauf si en facile ou le coup n'est pas comptabilisé
                    n_tir[a_joueur] -= 1
                    if (a_joueur == nb_joueur - 1):
                        a_joueur = 0
                    else:
                        a_joueur = a_joueur + 1

            if (y <= 600) and depasse_sol == False:  # est ce que la deuxieme condition est necessaire ?
                depasse_sol = True

        pygame.display.flip()  # .update()          met à jour la fenêtre de jeu
        timer.tick(60)  # loop 60/sec




# ----------------------- RULES ----------------------- #
def regle_jeu():
    """Fonction de la partie regle appelée depuis le menu"""
    screen = pygame.display.set_mode((1000, 700))
    fond_regle = pygame.image.load("images/mer_regle.png").convert_alpha()
    globe = pygame.image.load("images/globe.png").convert_alpha()
    piece = pygame.image.load("images/piece.png").convert_alpha()
    retour = pygame.image.load("images/retour.png").convert_alpha()
    poisson = pygame.image.load("images/saumon.png").convert_alpha()
    brique = pygame.image.load("images/brique.png").convert_alpha()
    bloc_or = pygame.image.load("images/bloc_or.png").convert_alpha()
    fond_regle = pygame.transform.scale(fond_regle, (1000, 700))
    globe = pygame.transform.scale(globe, (50, 50))
    piece = pygame.transform.scale(piece, (35, 35))
    poisson = pygame.transform.scale(poisson, (50, 50))
    brique = pygame.transform.scale(brique, (35, 35))
    bloc_or = pygame.transform.scale(bloc_or, (35, 35))

    bout_retour = bouton(20, 10, retour, 0.04, 'image/bouton_retour_regle')
    # création des text
    police_text = pygame.font.SysFont("arial", 30)
    police_titre = pygame.font.SysFont("arial", 35)  # prend en parametre le police d'écriture et la taille.
    text_but = police_titre.render("But du jeu :", 1, (0, 0, 0))
    text_jeu = police_titre.render("Règle jeu :", 1, (0, 0, 0))
    text_regle_but = police_text.render(" Collecter le plus de point", 1, (0, 0, 0))
    text_regle_jeu = police_text.render(" Selectionner un poisson adapter la force et l'angle du tire avec la souris", 1, (0, 0, 0))
    text_regle_jeu_bis = police_text.render(" puis relacher pour lancer le poisson et casser les caisses. ", 1,(0, 0, 0))
    text_objet_speciale = police_titre.render("Objet : ", 1, (0, 0, 0))
    text_objet_brique = police_text.render(": brique : rapporte des points quand elle sont détruites ", 1, (0, 0, 0))
    text_objet_brique_or = police_text.render(": brique d'or : rapporte plus de point que les briques mais sont plus solide ", 1, (0, 0, 0))
    text_objet_piece = police_text.render(": pièce : rapporte des points bonus ", 1, (0, 0, 0))
    text_capacite = police_titre.render("Capacité des poissons :", 1, (0, 0, 0))
    text_capacite_bombe = police_text.render("- poisson globe : grossie en appuyant sur E ", 1, (0, 0, 0))
    text_capacite_poisson = police_text.render("- poisson : pas de capcité spéciale", 1, (0, 0, 0))
    timer = pygame.time.Clock()
    regle = True

    while regle:
        screen.blit(fond_regle, (0, 0))  # affichage du fond
        # affichage des texts et des images associer
        screen.blit(text_but, (75, 50))
        screen.blit(text_regle_but, (250, 55))
        screen.blit(text_jeu, (75, 100))
        screen.blit(text_regle_jeu, (125, 145))
        screen.blit(text_regle_jeu_bis, (125, 185))
        screen.blit(text_objet_speciale, (75, 250))
        screen.blit(text_objet_brique, (125, 295))
        screen.blit(brique, (55, 295))
        screen.blit(text_objet_brique_or, (125, 340))
        screen.blit(bloc_or, (55, 345))
        screen.blit(text_objet_piece, (125, 395))
        screen.blit(piece, (55, 390))  # affichage de l'image correspondant au text
        screen.blit(text_capacite, (75, 475))
        screen.blit(text_capacite_poisson, (125, 525))
        screen.blit(poisson, (55, 520))
        screen.blit(text_capacite_bombe, (125, 575))
        screen.blit(globe, (55, 570))

        if bout_retour.draw(screen) == True:  # pour retourner au menu avec le bouton retour
            regle = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.flip()  # .update()          met à jour la fenêtre de jeu
        timer.tick(60)  # loop 60/sec

# ----------------------- OTHER ----------------------- #
def set_difficulty(value, difficulty):
    """la variable diff sauvegarde la difficulté
    0: Facile
    1: Normal
    2: Difficile"""
    global diff
    diff = difficulty
    pass


def save_pseudo(pseudo_sav):  # sauvegarde le pseudo dans la variable pseudo
    global pseudo
    pseudo = pseudo_sav
    print(pseudo)


def set_nb_joueurs(value, joueurs):
    global nb_joueur
    nb_joueur = joueurs
    pass
