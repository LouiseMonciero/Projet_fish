import pygame        #https://www.pygame.org/
import pygame_menu   #https://github.com/ppizarror/pygame-menu
import sys
from projet_functions import *
from fonctions_principales import *

print("\nHello from the creators of the game, go directly to the pygame console to play please\n")
pygame.init()

#MON ECRAN
screen = pygame.display.set_mode((1000, 700))   # largeur hauteur

menu = pygame_menu.Menu('AngryFish', 1000, 700, theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Joueur : ', default='pseudo')
menu.add.selector('Difficulté : ', [('Normal',2),('Difficile', 3), ('Facile', 1)], onchange= set_difficulty)
menu.add.button('Jouer', start_the_game) # l'ancien main a ete mit dans la fonction start_the_game pour que le jeu se lance que quand on clique sur le bouton "Jouer"
menu.add.button('Règle', regle_jeu) # quand on clique sur le bouton "regle" ca lance la fct regle_jeu qui affiche une page avec le but du jeu, les regle du jeu, les objet speciaux et les capaciter des different poisson 
menu.add.button('Quitter', pygame_menu.events.EXIT)

# alternative way to manage the main loop explained here : https://pygame-menu.readthedocs.io/en/4.3.9/_source/create_menu.html#display-a-menu
menu.mainloop(screen)