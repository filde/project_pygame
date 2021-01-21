import os
import sys

import pygame


def terminate(): # выход из игры
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None): # загрузка картинки
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((5, 5))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Icon(pygame.sprite.Sprite): # иконка персонажа
    def __init__(self, name, x, *sprites):
        super().__init__(*sprites)
        self.name = name
        self.image = load_image(f'Icon/{name}.jpg')
        self.rect = self.image.get_rect().move(x, 287)

        
class Character(pygame.sprite.Sprite): # курсор игрока
    def __init__(self, name, characters, pers, *sprites):
        super().__init__(*sprites)
        self.characters = characters
        self.go = True
        self.pers = pers
        self.type = name
        self.ind = 0
        self.image = pygame.Surface((83, 83), pygame.SRCALPHA, 32)
        if name:
            pygame.draw.rect(self.image, pygame.Color('red'), (0, 0, 83, 83))
            self.x = 518
        else:
            pygame.draw.rect(self.image, pygame.Color('blue'), (0, 0, 83, 83))
            self.x = 18
        self.rect = pygame.Rect(self.x, 282, 83, 83)
        self.step = pygame.mixer.Sound('data/step.wav')
        self.enter = pygame.mixer.Sound('data/enter.wav')

    def move(self, dx): # перемещение курсора
        if self.go:
            self.ind = (self.ind + dx) % 5
            self.rect.x = self.x + 95 * self.ind
            self.step.play()

    def choice(self): # игрок нажал на кнопку, чтобы выбрать персонажа
        if self.go:
            ch = pygame.sprite.spritecollideany(self, self.pers)
            self.characters[self.type] = ch.name
            self.go = False
            self.enter.play()
        
        


def choice_character(screen, FPS, width, height):
    color = 255
    v = 127 / FPS
    k = v
    characters = [None, None] # персонажи, которых выбрали игроки
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    pers = pygame.sprite.Group()
    player1 = Character(0, characters, pers, all_sprites)
    player2 = Character(1, characters, pers, all_sprites)
    fon = load_image('fon2.jpg')
    font1 = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 30)
    text = font1.render('Выбор персонажа', True, pygame.Color('white'))
    for i in range(5):
        Icon(int(i + 1), 23 + 95 * i, all_sprites, pers)
        Icon(int(i + 1), 523 + 95  * i, all_sprites, pers)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player1.move(-1)
                elif event.key == pygame.K_d:
                    player1.move(1)
                elif event.key == pygame.K_LEFT:
                    player2.move(-1)
                elif event.key == pygame.K_RIGHT:
                    player2.move(1)
                elif event.key == pygame.K_SPACE:
                    player1.choice()
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    player2.choice()
        if color <= 100:
            k = -v
        elif color > 255:
            k = v
        if characters[0]:
            text1 = font2.render('Ожидайте другого игрока.',
                         True, pygame.Color('white'))
        else:
            text1 = font2.render('Чтобы выбрать персонажа, нажмите ПРОБЕЛ',
                                 True, pygame.Color('white'))
            text1.set_alpha(color)
        if characters[1]:
            text2 = font2.render('Ожидайте другого игрока.',
                         True, pygame.Color('white'))
        else:
            text2 = font2.render('Чтобы выбрать персонажа, нажмите ENTER',
                                 True, pygame.Color('white'))
            text2.set_alpha(color)
        x1 = 250 - text1.get_width() // 2
        x2 = 750 - text2.get_width() // 2
        screen.blit(fon, (0, 0))
        screen.blit(text, (350, 50))
        screen.blit(text1, (x1, 530))
        screen.blit(text2, (x2, 530))
        all_sprites.draw(screen)
        all_sprites.update()
        color -= k
        pygame.display.flip()
        clock.tick(FPS)
        if characters[0] and characters[1]:
            return characters
