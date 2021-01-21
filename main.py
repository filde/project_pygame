import os
import sys

import pygame
from start import *
from choice_of_character import *
from game import *
from money import *


pygame.init()
SIZE = width, height = 1000, 625
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Untitled fighting')
FPS = 60
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play(-1)
start_screen(screen, FPS, *SIZE)
while True:
    start_menu(screen, FPS, *SIZE)
    pers = choice_character(screen, FPS, *SIZE)
    pygame.mixer.music.stop()
    game(screen, FPS, *SIZE, pers)
    money(screen, FPS, *SIZE)
    pygame.mixer.music.load('data/music.mp3')
    pygame.mixer.music.play(-1)
    
