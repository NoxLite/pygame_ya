import pygame
import os
import random

pygame.init()
pygame.font.init()
buttons_clicked = [False, False, False]

all_houses = pygame.sprite.Group()
all_buttons = pygame.sprite.Group()
all_another_sprites = pygame.sprite.Group()
all_cells_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
info_file = [elem[:-1].split(' ') for elem in open('map.txt', 'r').readlines()]
map = info_file[:-2]
houses = ['home_1.png', 'home_2.png', 'home_3.png']
choise = 1
types = {1: 'Ничего', 2: 'Дом', 'c': 'Очистить карту'}
types_defeat = {1: 'Пушки', 2: 'Армия', 3: 'Ряд танков', 4: 'Самолеты'}
choise_defeat = 1
mojo = int(info_file[-2][0])
peoples = int(info_file[-1][0])
font = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)


class Map:
    def __init__(self, width, height, size, x, y):
        self.width = width
        self.height = height
        self.size = size
        self.coords_map = []
        self.x_cell = 0
        self.y_cell = 0
        self.row = 0
        self.col = 0
        for i in range(width):
            one = []
            for j in range(height):
                sprite = Cell(x + size * i, y + size * j)
                all_cells_sprites.add(sprite)
                one.append([x + size * i, y + size * j])
            self.coords_map.append(one)

    def get_click(self, mouse_pos):
        for i in range(self.width):
            for j in range(self.height):
                x = self.coords_map[i][j][0]
                y = self.coords_map[i][j][1]
                if x < mouse_pos[0] < x + self.size and y < mouse_pos[1] < y + self.size:
                    self.y_cell = y
                    self.x_cell = x
                    self.row = i
                    self.row = j
                    return True

    def place(self, choise):
        if choise == 2:
            global map
            map[self.row][self.col] = 'h' + str(random.randint(1, 3))
            render_house(self.x_cell, self.y_cell, self.row, self.col)


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('grass_texture.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.convert()


class Button(pygame.sprite.Sprite):
    def __init__(self, name_image, pos_x, pos_y, size1, size2):
        self.x = pos_x
        self.y = pos_y
        self.size = (size1, size2)
        super().__init__()
        self.image = load_image(f'buttons_test\{name_image}')
        self.image.convert()
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.is_clicked = False

    def update(self, pos_mouse):
        if self.x <= pos_mouse[0] <= self.x + self.size[0] and self.y <= pos_mouse[1] <= self.y + self.size[1]:
            self.is_clicked = True
        else:
            self.is_clicked = False

    def draw_choise(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 60, 60), 0)


class Stat(pygame.sprite.Sprite):
    def __init__(self, x, y, stat, image):
        self.x = x
        self.y = y
        self.stat = stat
        super().__init__()
        self.image = load_image(f'buttons_test\{image}').convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = pygame.font.Font(None, 50)
        self.stat = self.font.render(str(stat), True, 'black')

    def render(self, screen):
        pygame.draw.rect(screen, 'green', (self.x, self.y, 200, 60), 0)
        screen.blit(self.stat, (self.x + 50, self.y + 10))

    def change_stat(self, stat):
        self.stat = self.font.render(str(stat), True, 'black')


class House(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col, map):
        super().__init__()
        self.image = load_image('home_' + str(map[row][col][1]) + '.png')
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def render_choise_hoses(scr):
    global choise
    global types
    keys = [elem for elem in types.keys()]
    for i in range(len(types.keys())):
        if choise == keys[i]:
            text = font.render(f'{keys[i]} {types[keys[i]]}', True, 'yellow')
        else:
            text = font.render(f'{keys[i]} {types[keys[i]]}', True, 'blue')
        scr.blit(text, (60, i * 50))


def render_choise_defeat(screen):
    global choise_defeat
    global types_defeat
    keys = [elem for elem in types_defeat.keys()]
    for i in range(len(types_defeat.keys())):
        if choise_defeat == keys[i]:
            text = font.render(f'{keys[i]} {types_defeat[keys[i]]}', True, 'yellow')
        else:
            text = font.render(f'{keys[i]} {types_defeat[keys[i]]}', True, 'blue')
        screen.blit(text, (60, i * 50))


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def render_house(x, y, row, col):
    global all_houses
    global houses
    global map
    if map[row][col] != '*':
        sprite = House(x, y, row, col, map)
        all_houses.add(sprite)


def create_houses(x, y, row, col, size):
    for i in range(row):
        for j in range(col):
            render_house(x + i * size, y + j * size, i, j)


def clear_map():
    cl_map = [['*'] * 8] * 8
    return cl_map


def game():
    pygame.display.update()
    global running, choise, flag, map, all_houses, mojo
    board = Map(8, 8, 100, 400, 20)
    create_houses(400, 20, 8, 8, 100)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    running = False
                if event.key in range(49, 52):
                    if house_button.is_clicked:
                        choise = event.key - 48
                    if defeat_button.is_clicked:
                        choise_defeat = event.key - 48
                if event.key == pygame.K_c:
                    map = clear_map()
                    all_houses = pygame.sprite.Group()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.get_click(event.pos):
                    board.place(choise)
                all_buttons.update(event.pos)
        screen.fill('black')
        screen.blit(background, (0, 0))
        all_cells_sprites.draw(screen)
        all_houses.draw(screen)
        all_buttons.draw(screen)

        money_png.render(screen)
        peoples_png.render(screen)
        all_another_sprites.draw(screen)

        if house_button.is_clicked:
            render_choise_hoses(screen)
            house_button.draw_choise(screen)
        if defeat_button.is_clicked:
            render_choise_defeat(screen)
            defeat_button.draw_choise(screen)
        if escape_button.is_clicked:
            menu()
            pygame.display.update()
        if quest_button.is_clicked:
            mojo += 100
            money_png.change_stat(mojo)
            quest_button.draw_choise(screen)
            quest_button.is_clicked = False
        pygame.display.flip()


def menu():
    pygame.display.update()
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_sprites.update(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    running = False
        screen.fill('blue')
        text_1 = font.render('Играть', True, 'green')
        text_2 = font.render('Выход', True, 'red')
        menu_sprites.draw(screen)
        screen.blit(text_1, (680, 330))
        screen.blit(text_2, (680, 440))
        if play_menu_button.is_clicked:
            game()
            pygame.display.update()
        if escape_menu_button.is_clicked:
            running = False
        pygame.display.flip()


peoples_png = Stat(0, 750, peoples, 'peoples.png')
money_png = Stat(0, 800, mojo, 'mojo.png')
house_button = Button('homes.png', 0, 0, 60, 60)
defeat_button = Button('defeat.png', 0, 65, 60, 60)
quest_button = Button('quest.png', 0, 130, 60, 60)
escape_button = Button('escape.png', 0, 195, 60, 60)
play_menu_button = Button('play.png', 600, 300, 300, 100)
escape_menu_button = Button('play.png', 600, 410, 300, 100)
background = load_image('background.png')
all_buttons.add(house_button)
all_buttons.add(escape_button)
all_buttons.add(defeat_button)
all_buttons.add(quest_button)
all_another_sprites.add(money_png)
all_another_sprites.add(peoples_png)
menu_sprites.add(play_menu_button)
menu_sprites.add(escape_menu_button)
running = True
if __name__ == '__main__':
    menu()
file = open('map.txt', 'w')
s = ''
for elem in map:
    s += ' '.join(elem) + '\n'
file.seek(0, 0)
file.write(s)
file.write(str(mojo) + '\n')
file.write(str(peoples) + '\n')
file.close()
