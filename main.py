import pygame        #https://www.pygame.org/
import pygame_menu   #https://github.com/ppizarror/pygame-menu
import sys
from projet_functions import *

from fonctions_principales import *
print("\nHello from the creators of the game, thanks to play with us !\n")
pygame.init()

music = pygame.mixer.music.load('sounds/mixkit-diving-sea-ambience-1205.wav')
pygame.mixer.music.play(-1)

#MON ECRAN
screen = pygame.display.set_mode((1000, 700))   # largeur hauteur
menu = pygame_menu.Menu('AngryFish', 1000, 700, theme=pygame_menu.themes.THEME_BLUE)

#MENU
menu.add.button('Jouer', start_the_game) # quand on appuie sur Jouer, la boucle de jeu est lancé
menu.add.selector('Difficulté : ', [('Normal',1),('Difficile', 2), ('Facile', 0)], onchange= set_difficulty)
menu.add.selector('Joueurs : ', [('1',1),('2',2),('3',3),('4',4),('5',5)], onchange=set_nb_joueurs)
menu.add.button('Règles', regle_jeu) # quand on clique sur le bouton "regle" la fct regle_jeu qui affiche une page avec le but du jeu, les regle du jeu, les objets spéciaux et les capacités des different poissons est lancé
menu.add.button('Quitter', pygame_menu.events.EXIT)
# alternative way to manage the main loop explained here : https://pygame-menu.readthedocs.io/en/4.3.9/_source/create_menu.html#display-a-menu
menu.mainloop(screen)