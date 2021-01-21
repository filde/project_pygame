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


class Border(pygame.sprite.Sprite): # стенка(справа, снизу, слева)
    def __init__(self, x, y, w, h, *sprites):
        super().__init__(*sprites)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("gold"),
                         (0, 0, w, h))
        self.rect = pygame.Rect(x, y, w, h)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite): # персонаж
    def __init__(self, name, ind, borders, screen, *sprites):
        super().__init__(*sprites)
        self.die = False
        self.jump = False
        self.hit = 0
        self.ind = ind
        self.screen = screen
        self.hp = 400
        self.borders = borders
        self.frames =[]
        self.cur = 0
        self.name = name
        if name == 4:
            self.load_start('start', 0, 12)
        else:
            self.load_start('start', 0, 7)
        self.rect = self.image.get_rect()
        self.rect.y = borders[1].rect.y
        self.dx = 0
        self.dy = 0
        self.gravity = 1
        if ind:
            self.rect.x = 900 - self.rect.w
        else:
            self.rect.x = 100

    def load_start(self, sheet, napr, columns): # загрузка анимаций
        self.frames = []
        for i in range(columns):
            frame = load_image(f'{self.name}/' + sheet + f'/img{i + 1}.png')
            self.frames.append(frame)
        if napr:
            self.frames = self.frames[::-1]
        self.cur = 0
        self.image = self.frames[self.cur]
        self.k = 10
        if self.ind:
            self.image = pygame.transform.flip(self.image, True, False)
        

    def update(self): # обновление при каждом игровом цикле
        self.k -= 1
        if self.k == 0 and not self.jump and self.hit == 0: # следуюший кадр анимации, если игрок стоит или двигается по горизонтали
            self.cur = (self.cur + 1) % len(self.frames)
            self.image = self.frames[self.cur]
            x = self.rect.x
            y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, y)
            self.k = 10
            if self.ind:
                self.image = pygame.transform.flip(self.image, True, False)
        if self.hit == 0: # передвижение игрока по горизнтали
            self.rect.x += self.dx
        self.rect.y += self.dy # передвижение игрока по вертикали
        self.dy += self.gravity
        if self.k == 0 and self.hit: # следующий кадр анимации удара
            self.cur += 1
            if self.cur < len(self.frames):
                self.image = self.frames[self.cur]
                x = self.rect.x
                y = self.rect.y
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(x, y)
                self.k = 10
                if self.ind:
                    self.image = pygame.transform.flip(self.image, True, False)
                    if self.name == 1:
                        self.rect.x -= 10
            else:
                self.hit = 0
                self.set_speedx(0)
                if self.ind:
                    self.rect.x += 50
        self.mask = pygame.mask.from_surface(self.image)
        if pygame.sprite.collide_mask(self, self.borders[1]): # отмена передвижения по вертикали, если игрок достиг нижней стенки
            if self.jump:
                self.jump = False
                self.set_speedx(0)
            self.dy = 0
        while pygame.sprite.collide_mask(self, self.borders[0]): # если игрок зашёл за левый край
            self.rect.x += 1
        while pygame.sprite.collide_mask(self, self.borders[1]): # если игрок ушёл вниз, зашёл в границы нижней стенки
            self.rect.y -= 1
        while pygame.sprite.collide_mask(self, self.borders[2]): # если игрок зашёл за правый край
            self.rect.x -= 1
        self.rect.y += 1
        if pygame.sprite.collide_mask(self, self.player): # нанесение урона другому игроку
            self.player.hp -= self.hit
        if self.ind: # отрисовывание количества здоровья у игрока, рамки для здоровья, и стрелочки для указания, где какой игрок
            if self.hp > 0:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (975 - self.hp, 25, self.hp, 25))
            pygame.draw.rect(self.screen, pygame.Color('gold'),
                             (575, 25, 400, 25), 5)
            pygame.draw.polygon(self.screen, pygame.Color('red'),
                                [(self.rect.x + self.rect.w // 2 - 30, 600),
                                 (self.rect.x + self.rect.w // 2 + 30, 600),
                                 (self.rect.x + self.rect.w // 2, 575)])
        else:
            if self.hp > 0:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (25, 25, self.hp, 25))
            pygame.draw.rect(self.screen, pygame.Color('gold'),
                             (25, 25, 400, 25), 5)
            pygame.draw.polygon(self.screen, pygame.Color('blue'),
                                [(self.rect.x + self.rect.w // 2 - 30, 600),
                                 (self.rect.x + self.rect.w // 2 + 30, 600),
                                 (self.rect.x + self.rect.w // 2, 575)])

    def add_player(self, player): # добавление другого игрока(для проверки столкновений и нанесения урона)
        self.player = player

    def set_speedx(self, dx): # начало или конец движения игрока влево или вправо
        self.dx += dx
        if self.jump or self.hit:
            return
        if self.dx == 0:
            if self.name == 4:
                self.load_start('start', 0, 12)
            else:
                self.load_start('start', 0, 7)
        elif self.dx > 0:
            if self.ind:
                self.load_start('walking', -1, 9)
            else:
                self.load_start('walking', 0, 9)
        elif self.ind:
            self.load_start('walking', 0, 9)
        else:
            self.load_start('walking', -1, 9)

    def set_speedy(self, dy): # прыжок
        if not self.jump and self.hit == 0:
            self.dy = dy
            self.jump = True
            x = self.rect.x
            y = self.rect.y
            self.image = load_image(f'{self.name}/jump.png')
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x, y)
            if self.ind:
                self.image = pygame.transform.flip(self.image, True, False)

    def hit_arm(self): # удар рукой
        if not self.jump and self.hit == 0:
            if self.name == 1:
                self.hit = 1
                self.load_start('arm', 0, 5)
            else:
                self.hit = 1
                self.load_start('arm', 0, 3)
                if self.ind:
                    self.rect.x -= 50

    def hit_leg(self): # удар ногой
        if not self.jump and self.hit == 0:
            if self.name != 1:
                self.hit = 2
                self.load_start('leg', 0, 6)
                if self.ind:
                    self.rect.x -= 50

    def set_die(self): # старт анимации смерти
        self.die = True
        if self.name == 1:
            self.load_start('die', 0, 6)
        elif self.name == 2:
            self.load_start('die', 0, 7)
        elif self.name == 4:
            self.load_start('die', 0, 10)
        else:
            self.load_start('die', 0, 9)

    def update_new(self): # обновление при каждом игровом цикле(если один из персонажей умер)
        if self.die: # если данный персонаж умер
            self.k -= 1
            if self.k == 0: # переключения кадра анмации
                self.cur = self.cur + 1
                if len(self.frames) > self.cur:
                    self.image = self.frames[self.cur]
                    x = self.rect.x
                    y = self.rect.y
                    self.rect = self.image.get_rect()
                    self.rect = self.rect.move(x, y)
                    self.k = 10
                    if self.ind:
                        self.image = pygame.transform.flip(self.image, True, False)
            self.mask = pygame.mask.from_surface(self.image)
            while pygame.sprite.collide_mask(self, self.borders[1]):
                self.rect.y -= 1
            while not pygame.sprite.collide_mask(self, self.borders[1]): # опусканий картинки на нужный уровень
                if self.name == 2:
                    self.rect.y += 20
                elif self.name == 4 and self.cur > 5:
                    if self.cur == 6:
                        self.rect.y += 2
                    elif self.cur == 8:
                        self.rect.y += 8
                    else:
                        self.rect.y += 6
                else:
                    self.rect.y += 1
            if self.ind:
                pygame.draw.rect(self.screen, pygame.Color('gold'),
                                 (575, 25, 400, 25), 5)
                pygame.draw.polygon(self.screen, pygame.Color('red'),
                                    [(self.rect.x + self.rect.w // 2 - 30, 600),
                                     (self.rect.x + self.rect.w // 2 + 30, 600),
                                     (self.rect.x + self.rect.w // 2, 575)])
            else:
                pygame.draw.rect(self.screen, pygame.Color('gold'),
                                 (25, 25, 400, 25), 5)
                pygame.draw.polygon(self.screen, pygame.Color('blue'),
                                    [(self.rect.x + self.rect.w // 2 - 30, 600),
                                     (self.rect.x + self.rect.w // 2 + 30, 600),
                                     (self.rect.x + self.rect.w // 2, 575)])
        else: # усли персонаж не умер
            self.update()
            
    def end(self): # проверка закончилась ли анимация смерти
        if self.die and self.cur >= len(self.frames):
            return True
        return False



def game(screen, FPS, width, height, pers): # сама игра
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    border_sprites = pygame.sprite.Group()
    borders = [Border(-1, 0, 1, 625, border_sprites), # левая и правая стенки и пол
               Border(0, 575, 1000, 50, border_sprites),
               Border(1000, 0, 1, 625, border_sprites)]
    player1 = Player(pers[0], 0, borders, screen, all_sprites)
    player2 = Player(pers[1], 1, borders, screen, all_sprites)
    player1.add_player(player2)
    player2.add_player(player1)
    fon = load_image('fon3.jpg')
    vs = load_image('vs.png', -1)
    gong = pygame.mixer.Sound('data/gong.wav')
    pygame.mixer.music.load('data/fight.mp3')
    pygame.mixer.music.play(-1)
    gong.play() 
    while True: # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player1.set_speedx(-3)
                elif event.key == pygame.K_d:
                    player1.set_speedx(3)
                elif event.key == pygame.K_LEFT:
                    player2.set_speedx(-3)
                elif event.key == pygame.K_RIGHT:
                    player2.set_speedx(3)
                elif event.key == pygame.K_j:
                    player1.set_speedy(-23)
                elif event.key == pygame.K_KP2:
                    player2.set_speedy(-23)
                elif event.key == pygame.K_h:
                    player1.hit_arm()
                elif event.key == pygame.K_k:
                    player1.hit_leg()
                elif event.key == pygame.K_KP1:
                    player2.hit_arm()
                elif event.key == pygame.K_KP3:
                    player2.hit_leg()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player1.set_speedx(3)
                elif event.key == pygame.K_d:
                    player1.set_speedx(-3)
                elif event.key == pygame.K_LEFT:
                    player2.set_speedx(3)
                elif event.key == pygame.K_RIGHT:
                    player2.set_speedx(-3)
        border_sprites.draw(screen)
        screen.blit(fon, (0, 0))
        screen.blit(vs, (450, 10))
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
        if player1.hp <= 0 or player2.hp <= 0:
            break
    if player2.hit:
        player2.rect.x += 50
    while True: # в цикле все персонажи перестают двигаться, бить и т.д.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        border_sprites.draw(screen)
        screen.blit(fon, (0, 0))
        screen.blit(vs, (450, 10))
        if pygame.sprite.collide_mask(player1, borders[1]) and (player1.dx != 0 or
                                                                player1.hit != 0):
            player1.hit = 0
            player1.set_speedx(-player1.dx)
        if pygame.sprite.collide_mask(player2, borders[1]) and (player2.dx != 0 or
                                                                player2.hit != 0):
            player2.hit = 0
            player2.set_speedx(-player2.dx)
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
        if (pygame.sprite.collide_mask(player1, borders[1]) and
            pygame.sprite.collide_mask(player2, borders[1])):
            break
    if player1.hp <= 0:
        player1.set_die()
    if player2.hp <= 0:
        player2.set_die()
    k = 0
    go = load_image('game-over.png')
    while True: # цикл с запуском смерти одного из персонажей и появлением надписи "Game over"
        k -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        border_sprites.draw(screen)
        screen.blit(fon, (0, 0))
        screen.blit(vs, (450, 10))
        player1.update_new()
        player2.update_new()
        all_sprites.draw(screen)
        if player1.end() or player2.end():
            if k < 0:
                k = FPS * 7
                pygame.mixer.music.load('data/end.mp3')
                pygame.mixer.music.play()
            if FPS * 7 - k > 255:
                alpha = 255
            else:
                alpha = FPS * 7 - k
            go.set_alpha(alpha)
            screen.blit(go, (250, 130))
        if k == 0:
            break
        clock.tick(FPS)
        pygame.display.flip()
