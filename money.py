import os
import sys

import pygame


def draw(screen, text, y, width, shrift): # написание текста
    font = pygame.font.Font(None, shrift)
    text = font.render(text, True, pygame.Color('black'))
    x = width // 2 - text.get_width() // 2
    screen.blit(text, (x, y))


def load_image(name, colorkey=None): # загрузка картинки
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate(): # выход из игры
    pygame.quit()
    sys.exit()


class Cross(pygame.sprite.Sprite): # "Крестик"
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('cross.png')
        self.rect = self.image.get_rect()
        self.rect.x = 715
        self.rect.y = 20


def money(screen, FPS, width, height): # экран с просьбой поддержать авторов 
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    fon = load_image('fon.jpg')
    fon.set_alpha(150)
    surface = pygame.Surface((510, 605))
    cat = load_image('кот.jpg')
    all_sprites = pygame.sprite.Group()
    cross = Cross(all_sprites)
    pygame.mixer.music.load('data/money.mp3')
    pygame.mixer.music.play(-1)
    while True:
        surface.fill((245, 149, 86))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  cross.rect.collidepoint(event.pos)):
                return
        draw(surface, 'Поддержите авторов!', 60, 500, 60)
        draw(surface, 'юmoney: 4100112260708902', 500, 500, 50)
        surface.blit(cat, (5, 160))
        screen.fill(pygame.Color('black'))
        screen.blit(fon, (0, 0))
        screen.blit(surface, (245, 10))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
