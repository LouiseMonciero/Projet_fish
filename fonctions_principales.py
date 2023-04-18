import pygame_menu  # https://github.com/ppizarror/pygame-menu
import sys
import pygame
from projet_functions import *

diff = 1
nb_joueur = 1
pseudo = "pseudo"  # si pas de pseudo saisie

para_jeu = [(7, float('inf'), 20, 30), (5, 20, 15, 35), (3, 10, 10, 50)]  # (nb_pieces , nombre de tir , chance d'avoir brique_or / brique , nb_briques)


def start_the_game():
    global para_jeu
    # MON ECRAN
    screen = pygame.display.set_mode((1000, 700))  # largeur hauteur

    # MES IMAGES
    mer_img = pygame.image.load("mer.png").convert_alpha()
    sable_img = pygame.image.load("sable.png").convert_alpha()
    depart_gd = pygame.image.load("lance_pierre.png").convert_alpha()
    sardine_img = pygame.image.load("saumon.png").convert_alpha()
    globe_img = pygame.image.load("globe.png").convert_alpha()
    rouge_img = pygame.image.load("poisson_rouge.png").convert_alpha()
    # button_img = pygame.image.load("bouton.png").convert_alpha()
    piece_img_gr = pygame.image.load("piece.png").convert_alpha()
    brique_img = pygame.image.load("brique.png").convert_alpha()
    bloc_or_img = pygame.image.load("bloc_or.png").convert_alpha()
    brique_casse_img = pygame.image.load("brique_casse.png").convert_alpha()
    fumee_img = pygame.image.load("fumee.png").convert_alpha()

    mer = pygame.transform.scale(mer_img, (1000, 700))
    piece_img = pygame.transform.scale(piece_img_gr, (piece_img_gr.get_width() * 0.1, piece_img_gr.get_height() * 0.1))

    # MES SURFACES
    screen.blit(mer, (0, 0))

    # MES RECTANGLES
    bandeau_rect = pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(30, 30, 60, 60))

    sable = pygame.transform.scale(sable_img, (1000, 100))
    depart = pygame.transform.scale(depart_gd, (75, 75))


    # MES BOUTTONS
    sardine = bouton(20, 50, sardine_img, 0.2, '')
    globe = bouton(20, 100, globe_img, 0.1, '')
    rouge = bouton(20, 175, rouge_img, 0.1, '')
    # button_lancer = bouton(10, 525, button_img, 0.1, '')

    # VARIABLES
    projectile = None  # quand le poisson est en l'air
    munition = None  # quand le poisson est sur la zone de départ
    para_lancer = None  # (vitesse , angle )

    score = 0
    if diff == 0:
        n_tir = "infini"
    else :
        n_tir = para_jeu[diff][1]

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
    image_score = police.render("SCORE:", 1, (0, 0, 0))  # (0,0,0) est le code RGB.
    image_n_tir = police.render("NOMBRE DE TIR:", 1, (0, 0, 0))

    # MES PIECES
    nb_pieces = para_jeu[diff][0]
    tab_pieces = generate_piece(nb_pieces, (100, 1000, 0, 500), piece_img)

    # MES BLOCS
    M_bloc = create_mat_bloc(brique_img, bloc_or_img, para_jeu[diff][3], para_jeu[diff][2])
    print_mat(M_bloc)   #ok

    while game_on:
        screen.blit(mer, (0, 0))
        # ------------quitter le jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # -------------place les surfaces
        screen.blit(sable, (0, 600))  # coin supp gauche
        screen.blit(depart, (100, 525))

        #--------------place les textes
        screen.blit(image_score, (40, 20))
        screen.blit(police.render(str(score), 1, (0, 0, 0)), (100, 20))
        screen.blit(image_n_tir, (170, 20))
        screen.blit(police.render(str( n_tir), 1, (0, 0, 0)), (300, 20))

        # ------------place les pièces

        tab_pieces, score = draw_pieces(screen, tab_pieces, projectile, score)

        # ------------place les blocs
        M_bloc , projectile , score , n_tir = draw_mat(screen, M_bloc, projectile, brique_casse_img ,score, n_tir)  # (x1 , x2 , y1 , y2 )
        # ------------place les boutons

        if sardine.draw(screen) and projectile == None:
            x = 100
            y = 500
            print('sardine clicked')
            munition = bouton(100, 500, sardine_img, 0.3, 'sardine')
        if globe.draw(screen) and projectile == None:
            x = 100
            y = 500
            print('globe clicked')
            munition = bouton(100, 500, globe_img, 0.1, 'globe')
            # munition = fish("globe", globe_img, 100, 500, 0.1)

        if rouge.draw(screen) and projectile == None:
            x = 100
            y = 500
            print('rouge clicked')
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
                projectile = fish("sardine", sardine_img, x_position, y_position, 0.3 , para_lancer[0])
                # projectile = fish("sardine", sardine_img, 100, 500, 0.3)
            elif munition.get_name() == 'globe':
                projectile = fish("globe", globe_img, x_position, y_position, 0.1,  para_lancer[0])
            elif munition.get_name() == 'rouge':
                projectile = fish("rouge", rouge_img, x_position, y_position, 0.15,  para_lancer[0])
            vitesse = para_lancer[0]
            angle = para_lancer[1]
            para_lancer = None
            munition = None

        if munition == None and projectile != None:
            projectile.draw_fish(screen)
            if ((y < 600) or depasse_sol == False) and (y > 0):
                x, y, temps_ecoule = calcul_traj(x_position, y_position, vitesse, temps_ecoule, angle, gravite)
                projectile.attribute_pos(x, y)
            else:
                projectile = None                    # disparition du poisson !!!!!!!
                if diff != 0:
                    n_tir -= 1
            if (y <= 600) and depasse_sol == False:  # est ce que la deuxieme condition est necessaire ?
                depasse_sol = True
        pygame.display.flip()  # .update()          met à jour la fenêtre de jeu
        timer.tick(60)  # loop 60/sec


def regle_jeu():  # fct pour la partie regle dans le menu
    screen = pygame.display.set_mode((1000, 700))
    fond_regle = pygame.image.load("fond_regle_temporaire.jpg").convert_alpha()
    bombe = pygame.image.load("bombe.png").convert_alpha()
    piece = pygame.image.load("piece.png").convert_alpha()
    retour = pygame.image.load("retour.png").convert_alpha()
    fond_regle = pygame.transform.scale(fond_regle, (1000, 700))
    bombe = pygame.transform.scale(bombe, (50, 50))
    piece = pygame.transform.scale(piece, (50, 50))
    bout_retour = bouton(20, 10, retour, 0.04, 'bouton_retour_regle')
    # création des text
    police_text = pygame.font.SysFont("arial", 30)
    police_titre = pygame.font.SysFont("arial", 35)  # prend en parametre le police d'écriture et la taille.
    text_but = police_titre.render("But du jeu :", 1, (0, 0, 0))
    text_jeu = police_titre.render("Règle jeu :", 1, (0, 0, 0))
    text_regle_but = police_text.render(" Casser toute les caisses", 1, (0, 0, 0))
    text_regle_jeu = police_text.render(" Selectionner un poisson adapter la force et l'angle du tire", 1, (0, 0, 0))
    text_regle_jeu_bis = police_text.render(" puis appuyer sur le bouton pour tirer et casser les caisses. ", 1,
                                            (0, 0, 0))
    text_objet_speciale = police_titre.render("Objet spéciale : ", 1, (0, 0, 0))
    text_objet_piece = police_text.render(": pièce : raporte des points bonus ", 1, (0, 0, 0))
    text_capacite = police_titre.render("Capacité des poissons :", 1, (0, 0, 0))
    text_capacite_bombe = police_text.render("- poisson bombe : explose à son arriver ", 1, (0, 0, 0))
    text_capacite_etc = police_text.render("- poisson...", 1, (0, 0, 0))
    timer = pygame.time.Clock()
    regle = True

    while regle:
        screen.blit(fond_regle, (0, 0))  # affichage du fond
        # affichage des texts et des images associer
        screen.blit(text_but, (75, 50))
        screen.blit(text_regle_but, (125, 100))
        screen.blit(text_jeu, (75, 175))
        screen.blit(text_regle_jeu, (125, 225))
        screen.blit(text_regle_jeu_bis, (125, 275))
        screen.blit(text_objet_speciale, (75, 350))
        screen.blit(text_objet_piece, (100, 400))
        screen.blit(piece, (35, 395))  # affichage de l'image correspondant au text
        screen.blit(text_capacite, (75, 475))
        screen.blit(text_capacite_bombe, (125, 525))
        screen.blit(bombe, (55, 520))
        screen.blit(text_capacite_etc, (125, 575))
        if bout_retour.draw(screen) == True:  # pour retourner au menu avec le bouton retour
            regle = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.flip()  # .update()          met à jour la fenêtre de jeu
        timer.tick(10)  # loop 60/sec


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