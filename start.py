import os
import sys

import pygame


def draw_rules(screen, width, height): # написание управления
    font = pygame.font.Font(None, 20)
    font1 = pygame.font.Font(None, 30)
    left = ['идти влево - клавиша "A"',
            'идти вправо - клавиша "D"',
            'прыжок - клавиша "J"',
            'удар рукой - клавиша "H"',
            'удар ногой - клавиша "K"']
    right = ['идти влево - клавиша "<-"',
             'идти вправо - клавиша "->"',
             'прыжок - клавиша "2" на дополнительной клавиатуре',
             'удар рукой - клавиша "1" на дополнительной клавиатуре',
             'удар ногой - клавиша "3" на дополнительной клавиатуре']
    text_coord = 230
    surface = pygame.Surface((396, 155))
    surface.set_alpha(200)
    pygame.draw.rect(surface, pygame.Color('black'), (0, 0, 396, 155))
    screen.blit(surface, (52, 200))
    screen.blit(surface, (552, 200))
    title1 = font1.render('Синий игрок', 1, pygame.Color('blue'))
    screen.blit(title1, (188, 210))
    title2 = font1.render('Красный игрок', 1, pygame.Color('red'))
    screen.blit(title2, (675, 210))
    for line in left:
        text = font.render(line, 1, pygame.Color('blue'))
        intro_rect = text.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 62
        text_coord += intro_rect.height
        screen.blit(text, intro_rect)
    text_coord = 230
    for line in right:
        text = font.render(line, 1, pygame.Color('red'))
        intro_rect = text.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 562
        text_coord += intro_rect.height
        screen.blit(text, intro_rect)


def draw_authors(screen, intro_text, width, height): # написание авторов
    font = pygame.font.Font(None, 30)
    text_coord = 130
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - string_rendered.get_width() // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def draw(screen, text, y, alpha, width, height): # написание текста
    font = pygame.font.Font(None, 50)
    text = font.render(text, True, pygame.Color('white'))
    x = width // 2 - text.get_width() // 2
    surface = pygame.Surface((273, 55))
    if alpha:
        surface.set_alpha(127)
    pygame.draw.rect(surface, pygame.Color('black'), (0, 0, 273, 55))
    screen.blit(surface, (364, y - 10))
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


def start_screen(screen, FPS, width, height): # заставка(появляется только в начале игры)   
    clock = pygame.time.Clock()
    color = 255
    v = 256 / FPS
    k = v
    font = pygame.font.Font(None, 50)
    fon = load_image('fon.jpg')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        if color <= 0: # мигание надписи
            k = -v
        elif color > 255:
            k = v
        text = font.render("Press SPACE to continue", True,
                           pygame.Color('white'))
        text.set_alpha(color)
        screen.blit(fon, (0, 0))
        text_x = width // 2 - text.get_width() // 2
        screen.blit(text, (292, 500))
        color -= k
        pygame.display.flip()
        clock.tick(FPS)


def start_menu(screen, FPS, width, height): # главное меню
    clock = pygame.time.Clock()
    fon = load_image('fon.jpg')
    alpha1 = True # прозрачность каждой из кнопок
    alpha2 = True
    alpha3 = True
    alpha4 = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                alpha1 = True
                alpha2 = True
                alpha3 = True
                alpha4 = True
                if 364 <= x <= 637 and 140 <= y <= 195:
                    alpha1 = False
                elif 364 <= x <= 637 and 240 <= y <= 295:
                    alpha2 = False
                elif 364 <= x <= 637 and 340 <= y <= 395:
                    alpha3 = False
                elif 364 <= x <= 637 and 440 <= y <= 495:
                    alpha4 = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 364 <= x <= 637 and 140 <= y <= 195:
                    return 
                elif 364 <= x <= 637 and 240 <= y <= 295:
                    alpha2 = True
                    authors(screen, FPS, width, height)
                elif 364 <= x <= 637 and 340 <= y <= 395:
                    alpha3 = True
                    rules(screen, FPS, width, height)
                elif 364 <= x <= 637 and 440 <= y <= 495:
                    terminate()
        screen.blit(fon, (0, 0))
        draw(screen, 'Новая игра', 150, alpha1, width, height)
        draw(screen, 'Авторы', 250, alpha2, width, height)
        draw(screen, 'Управление', 350, alpha3, width, height)
        draw(screen, 'Выйти из игры', 450, alpha4, width, height)
        pygame.display.flip()
        clock.tick(FPS)


def authors(screen, FPS, width, height): # экран с авторами
    clock = pygame.time.Clock()
    fon = load_image('fon.jpg')
    alpha = True
    font = pygame.font.Font(None, 50)
    text = font.render('Назад', True, pygame.Color('white'))
    names = ['Авторы:', 'Дмитрии:', 'ЛОБАНЕВ и ФИЛИМОНОВ', '',
              'Поддержать авторов:', 'юmoney: 4100112260708902']
    alpha = 127
    author = pygame.Surface((297, 190)) # фон для места, где написан авторы
    author.set_alpha(127)
    pygame.draw.rect(author, pygame.Color('black'), (0, 0, 297, 190))
    surface = pygame.Surface((129, 55)) # фон для кнопки "Назад"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if 446 <= x <= 565 and 500 <= y <= 555:
                    alpha = 255
                else:
                    alpha = 127
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 446 <= x <= 565 and 500 <= y <= 555:
                    return
        surface.set_alpha(alpha)
        pygame.draw.rect(surface, pygame.Color('black'), (0, 0, 129, 55))
        screen.blit(fon, (0, 0))
        screen.blit(author, (353, 130))
        screen.blit(surface, (436, 500))
        draw_authors(screen, names, width, height)
        screen.blit(text, (446, 510))
        pygame.display.flip()
        clock.tick(FPS)


def rules(screen, FPS, width, height): # экран с описанием управления
    clock = pygame.time.Clock()
    fon = load_image('fon.jpg')
    alpha = True # прозрачность кнопки "Назад"
    font = pygame.font.Font(None, 50)
    text = font.render('Назад', True, pygame.Color('white'))
    title = font.render('Управление', True, pygame.Color('white'))
    alpha = 200
    surface = pygame.Surface((129, 55))
    titlesur = pygame.Surface((226, 55))
    titlesur.set_alpha(200)
    pygame.draw.rect(surface, pygame.Color('black'), (0, 0, 129, 55))
    pygame.draw.rect(titlesur, pygame.Color('black'), (0, 0, 206, 55))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if 446 <= x <= 565 and 500 <= y <= 555:
                    alpha = 255
                else:
                    alpha = 200
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 446 <= x <= 565 and 500 <= y <= 555:
                    return
        surface.set_alpha(alpha)
        screen.blit(fon, (0, 0))
        screen.blit(surface, (436, 500))
        screen.blit(titlesur, (387, 30))
        screen.blit(text, (446, 510))
        screen.blit(title, (397, 40))
        draw_rules(screen, width, height)
        pygame.display.flip()
        clock.tick(FPS)
