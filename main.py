import pygame
import os
import random

pygame.init()
pygame.font.init()
buttons_clicked = [False, False, False]
all_houses = pygame.sprite.Group()
all_buttons = pygame.sprite.Group()
all_another_sprites = pygame.sprite.Group()
map = [elem[:-1].split(' ') for elem in open('map.txt', 'r').readlines()]
choise_map = [['*', '*', '*', '*', '*', '*', '*', '*']] * 8
houses = ['home_1.png', 'home_2.png', 'home_3.png']
choise = 1
types = {1: 'Ничего', 2: 'Дом', 'c': 'Очистить карту'}
types_defeat = {1: 'Пушки', 2: 'Армия', 3: 'Ряд танков', 4: 'Самолеты'}
choise_defeat = 1
mojo = 0
peoples = 0

class Board:
    def __init__(self, width, height):
        global map
        global choise_map
        self.choise_map = choise_map
        self.map = map
        self.width = width
        self.height = height
        self.left = 500
        self.top = 20
        self.cell_size = 100
        self.builds = [0]
        self.rectes = {}

    def render(self, screen):
        x = self.left
        y = self.top
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                self.rectes[f'{i}; {j}'] = [x + self.cell_size, y + self.cell_size]
                if self.choise_map[i][j] == '*':
                    pygame.draw.rect(screen, 'green', (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, 'black', (x, y, self.cell_size, self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, '#cffc03', (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, 'black', (x, y, self.cell_size, self.cell_size), 1)
                house(x + 20, y + 20, i, j)
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_click(self, mouse_pos, screen, choise):
        self.choise = choise
        self.on_click(mouse_pos)

    def on_click(self, pos):
        for elem in self.rectes.keys():
            if self.rectes[elem][0] - self.cell_size <= pos[0] <= self.rectes[elem][0] \
                    and self.rectes[elem][1] - self.cell_size <= pos[1] <= self.rectes[elem][1]:
                key = elem.split('; ')
                print(elem)
                if self.choise == 1:
                    if self.map[int(key[0])][int(key[1])] == '*':
                        self.map[int(key[0])][int(key[1])] = 'h' + random.choice(houses)[-5]
                break

    def get_peoples(self):
        return self.builds[0]

    def motion(self, pos):
        self.choise_map = [['*', '*', '*', '*', '*', '*', '*', '*'],
                           ['*', '*', '*', '*', '*', '*', '*', '*'],
                           ['*', '*', '*', '*', '*', '*', '*', '*'],
                           ['*', '*', '*', '*', '*', '*', '*', '*'],
                           ['*', '*', '*', '*', '*', '*', '*', '*'],
                           ['*', '*', '*', '*', '*', '*', '*', '*'],
                           ['*', '*', '*', '*', '*', '*', '*', '*'],
                           ['*', '*', '*', '*', '*', '*', '*', '*']]
        for elem in self.rectes.keys():
            if self.rectes[elem][0] - self.cell_size <= pos[0] <= self.rectes[elem][0] \
                    and self.rectes[elem][1] - self.cell_size <= pos[1] <= self.rectes[elem][1]:
                key = elem.split('; ')
                self.choise_map[int(key[0])][int(key[1])] = 'cur'
                break


class Button(pygame.sprite.Sprite):
    def __init__(self, name_image, pos_x, pos_y, position):
        self.x = pos_x
        self.y = pos_y
        self.position = position
        super().__init__()
        self.image = load_image(f'buttons_test\{name_image}')
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.is_clicked = False

    def update(self, pos_mouse):
        if self.x <= pos_mouse[0] <= self.x + 60 and self.y <= pos_mouse[1] <= self.y + 60:
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
        self.image = load_image(f'buttons_test\{image}')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        font = pygame.font.Font(None, 50)
        self.stat = font.render(str(stat), True, 'green')

    def render(self, screen):
        screen.blit(self.stat, (self.x + 50, self.y + 10))


def render_choise_hoses(scr):
    global choise
    global types
    font = pygame.font.Font(None, 50)
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
    font = pygame.font.Font(None, 50)
    keys = [elem for elem in types_defeat.keys()]
    for i in range(len(types_defeat.keys())):
        if choise == keys[i]:
            text = font.render(f'{keys[i]} {types_defeat[keys[i]]}', True, 'yellow')
        else:
            text = font.render(f'{keys[i]} {types_defeat[keys[i]]}', True, 'blue')
        screen.blit(text, (60, i * 50))


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def house(x, y, row, col):
    global all_houses
    global houses
    global map
    if map[row][col] != '*':
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image('home_' + str(map[row][col][1]) + '.png')
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = x
        sprite.rect.y = y
        all_houses.add(sprite)


def clear_map():
    cl_map = [['*'] * 8] * 8
    return cl_map


peoples_png = Stat(0, 750, peoples, 'peoples.png')
money_png = Stat(0, 800, mojo, 'mojo.png')
house_button = Button('homes.png', 0, 0, 0)
defeat_button = Button('defeat.png', 0, 65, 0)
escape_button = Button('escape.png', 0, 130, 0)
all_buttons.add(house_button)
all_buttons.add(escape_button)
all_buttons.add(defeat_button)
all_another_sprites.add(money_png)
all_another_sprites.add(peoples_png)
running = True
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    board = Board(8, 8)
    while running:
        screen.fill('black')
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
                    board.map = clear_map()
                    all_houses = pygame.sprite.Group()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos, screen, choise)
                all_buttons.update(event.pos)
        map = board.map
        peoples = board.get_peoples()
        board.render(screen)

        all_houses.draw(screen)
        all_buttons.draw(screen)

        all_another_sprites.draw(screen)
        money_png.render(screen)
        peoples_png.render(screen)

        if house_button.is_clicked:
            render_choise_hoses(screen)
            house_button.draw_choise(screen)
        if defeat_button.is_clicked:
            render_choise_defeat(screen)
            defeat_button.draw_choise(screen)
        if escape_button.is_clicked:
            running = False
            escape_button.draw_choise(screen)
        pygame.display.flip()

file = open('map.txt', 'w')
s = ''
for elem in map:
    s += ' '.join(elem) + '\n'
file.seek(0, 0)
file.write(s)
file.close()
