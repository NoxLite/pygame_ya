import pygame
import os
import random
import sys

pygame.init()
pygame.font.init()
buttons_clicked = [False, False, False]

all_houses = pygame.sprite.Group()
all_buttons = pygame.sprite.Group()
all_another_sprites = pygame.sprite.Group()
all_cells_sprites = pygame.sprite.Group()
anim_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
quest_sprites = pygame.sprite.Group()
info_file = [elem[:-1].split(' ') for elem in open('map.txt', 'r').readlines()]
quest_form = [elem[:-1].split('/') for elem in open('quests.txt', 'r', encoding='utf8').readlines()]
map = info_file[:-2]
houses = ['home_1.png', 'home_2.png', 'home_3.png']
choise = 1
types = {1: 'Ничего', 2: 'Дом', 'c': 'Очистить карту'}
types_defeat = {1: 'Пушки', 2: 'Армия', 3: 'Ряд танков', 4: 'Самолеты'}
quest_info = {}
for elem in quest_form:
    quest_form[int(elem[0])] = [elem[1], int(elem[2]), elem[3], elem[4]]
choise_defeat = 1
mojo = int(info_file[-2][0])
peoples = int(info_file[-1][0])
text_font = pygame.font.Font('text.ttf', 30)
tittle_font = pygame.font.Font('title.ttf', 180)
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
running_menu = True
running_game = False
running_quest = False
logo = tittle_font.render('YA_GAME', True, 'white')
clock = pygame.time.Clock()
clock.tick(10)
m = 11
p = 6
c = 7
completed_quest = 0


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
                    self.col = j
                    return True

    def place(self, choise):
        global map
        my_map = map
        if choise == 2:
            if my_map[self.row][self.col] == '*':
                my_map[self.row][self.col] = 'h' + str(random.randint(1, 3))
                render_house(self.x_cell, self.y_cell, self.row, self.col)
        return my_map


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('grass_texture.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.convert()


class Button(pygame.sprite.Sprite):
    def __init__(self, name_image, pos_x, pos_y, size1, size2, text='', rect_color=1):
        self.x = pos_x
        self.y = pos_y
        self.rect_color = rect_color
        self.size = (size1, size2)
        super().__init__()
        self.image = load_image(f'buttons_test\{name_image}')
        self.image.convert()
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.is_clicked = False
        self.text = text_font.render(text, True, 'green')

    def draw(self, screen):
        if self.rect_color == 1:
            pygame.draw.rect(screen, pygame.Color(0, 0, 0), (self.x, self.y, 210, 70), 0)
        screen.blit(self.text, (self.x + self.size[0] + 10, self.y + 10))

    def update(self, pos_mouse):
        if self.x <= pos_mouse[0] <= self.x + self.size[0] and self.y <= pos_mouse[1] <= self.y + self.size[1]:
            self.is_clicked = True
        else:
            self.is_clicked = False

    def draw_choise(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.size[0], self.size[1]), 0)


class House(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col, map):
        super().__init__()
        self.image = load_image('home_' + str(map[row][col][1]) + '.png')
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Stat(pygame.sprite.Sprite):
    def __init__(self, x, y, stat, image):
        self.x = x
        self.y = y
        self.stat = stat
        super().__init__()
        self.image = load_image(f'buttons_test\{image}')
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.stat = text_font.render(str(stat), True, 'green')

    def render(self, screen):
        pygame.draw.rect(screen, 'black', (self.x, self.y, 200, 50), 0)
        screen.blit(self.stat, (self.x + 60, self.y + 10))

    def change_stat(self, stat):
        self.stat = text_font.render(str(stat), True, 'green')


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(anim_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.convert_alpha()
        self.rect = self.rect.move(x, y)
        self.end = columns * rows
        self.d = 4

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def check(self):
        if self.cur_frame != self.end - 1:
            return False
        else:
            return True


class Quest(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        global quest_sprites
        super().__init__()
        self.x = x
        self.y = y
        self.image = load_image(f'buttons_test\{image}')
        self.money = Button('mojo_quest.png', self.x + 30, self.y - 10, 100, 150)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.get_it = False
        self.completed_sprites = pygame.sprite.Group()

    def set_quest(self, id, screen):
        self.completed_sprites = pygame.sprite.Group()
        self.money = Button('mojo_quest.png', self.x + 30, self.y - 10, 100, 150)
        self.type = id
        global quest_form
        self.completed_sprites.add(self.money)
        self.pay = text_font.render(str(quest_form[self.type][1]), True, 'green')
        self.completed = text_font.render(f'{quest_form[self.type][2]}/{quest_form[self.type][3]}', True, 'green')
        self.text = quest_form[self.type][0].split(' ')
        self.about1 = text_font.render(' '.join(self.text[:2]), True, 'green')
        self.about2 = text_font.render(' '.join(self.text[2:5]), True, 'green')
        self.about3 = text_font.render(' '.join(self.text[5:7]), True, 'green')
        self.get_it = False

    def render_text(self, screen):
        screen.blit(self.pay, (self.x + 58, self.y + 100))
        screen.blit(self.completed, (self.x + 200, self.y + 100))
        screen.blit(self.about1, (self.x + 180, self.y))
        screen.blit(self.about2, (self.x + 180, self.y + 30))
        screen.blit(self.about3, (self.x + 180, self.y + 60))
        self.completed_sprites.draw(screen)

    def update(self, pos_mouse):
        global mojo, completed_quest
        if self.get_it is False:
            self.money.update(pos_mouse)
            if self.money.is_clicked:
                if quest_form[self.type][2] == quest_form[self.type][3]:
                    mojo += quest_form[self.type][1]
                    money_png.change_stat(mojo)
                    self.money = pygame.sprite.Sprite()
                    self.money.image = load_image(r'buttons_test\completed7.png')
                    self.money.rect = self.money.image.get_rect()
                    self.money.rect.x = self.x + 30
                    self.money.rect.y = self.y - 10
                    self.completed_sprites = pygame.sprite.Group()
                    self.completed_sprites.add(self.money)
                    completed_quest += 1
                    self.get_it = True


def menu():
    global running_menu
    global running_game
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_sprites.update(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    running_menu = False
        screen.fill('blue')
        menu_sprites.draw(screen)
        play_menu_button.draw(screen)
        escape_menu_button.draw(screen)
        screen.blit(logo, (400, 10))
        pygame.display.update()
        if play_menu_button.is_clicked:
            running_menu = False
            running_game = True
        if escape_menu_button.is_clicked:
            running_menu = False
        pygame.display.flip()
    if running_game:
        game()


def game():
    global choise, all_houses, mojo, running_game, map, choise_defeat, running_quest
    board = Map(8, 8, 100, 400, 20)
    create_houses(400, 20, 8, 8, 100)

    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    running_game = False
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
                    map = board.place(choise)
                all_buttons.update(event.pos)
        screen.fill('black')
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, 'black', (0, 0, 300, 2000), 0)

        house_button.draw(screen)
        defeat_button.draw(screen)
        quest_button.draw(screen)
        escape_button.draw(screen)

        all_cells_sprites.draw(screen)
        all_houses.draw(screen)
        all_buttons.draw(screen)

        money_png.render(screen)
        peoples_png.render(screen)

        all_another_sprites.draw(screen)
        anim_sprites.draw(screen)

        pygame.display.update()
        if house_button.is_clicked:
            render_choise_hoses(screen)
            house_button.draw_choise(screen)
        if defeat_button.is_clicked:
            render_choise_defeat(screen)
            defeat_button.draw_choise(screen)
        if escape_button.is_clicked:
            running_game = False
        if quest_button.is_clicked:
            money_png.change_stat(mojo)

            quest_button.draw_choise(screen)
            quest_button.is_clicked = False
            running_game = False
            running_quest = True

        pygame.display.flip()
    if running_quest:
        quest()


def quest():
    global running_quest, running_game, m, c, completed_quest
    quest_sprite_form_1.set_quest(random.randint(0, 3), screen)
    quest_sprite_form_2.set_quest(random.randint(0, 3), screen)
    quest_sprite_form_3.set_quest(random.randint(0, 3), screen)
    quest_sprite_form_4.set_quest(random.randint(0, 3), screen)
    while running_quest:
        screen.fill('blue')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_quest = False
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    running_quest = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                quest_sprites.update(event.pos)
        if escape_quest_button.is_clicked:
            running_quest = False
            escape_quest_button.is_clicked = False
        money_png.render(screen)
        peoples_png.render(screen)
        all_another_sprites.draw(screen)
        quest_sprites.draw(screen)
        quest_sprite_form_1.render_text(screen)
        quest_sprite_form_2.render_text(screen)
        quest_sprite_form_3.render_text(screen)
        quest_sprite_form_4.render_text(screen)
        if m < 11:
            mojo_anim.update()
            m += 1
        pygame.display.flip()
    running_game = True
    if completed_quest == 4:
        quest_sprite_form_1.set_quest(random.randint(0, 3), screen)
        quest_sprite_form_2.set_quest(random.randint(0, 3), screen)
        quest_sprite_form_3.set_quest(random.randint(0, 3), screen)
        quest_sprite_form_4.set_quest(random.randint(0, 3), screen)
        completed_quest = 0
    game()


def render_choise_hoses(scr):
    global choise
    global types
    keys = [elem for elem in types.keys()]
    for i in range(len(types.keys())):
        if choise == keys[i]:
            text = text_font.render(f'{keys[i]} {types[keys[i]]}', True, 'yellow')
        else:
            text = text_font.render(f'{keys[i]} {types[keys[i]]}', True, 'blue')
        scr.blit(text, (0, 300 + i * 50))


def render_choise_defeat(screen):
    global choise_defeat
    global types_defeat
    keys = [elem for elem in types_defeat.keys()]
    for i in range(len(types_defeat.keys())):
        if choise_defeat == keys[i]:
            text = text_font.render(f'{keys[i]} {types_defeat[keys[i]]}', True, 'yellow')
        else:
            text = text_font.render(f'{keys[i]} {types_defeat[keys[i]]}', True, 'blue')
        screen.blit(text, (0, 300 + i * 50))


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def render_house(x, y, row, col):
    global all_houses
    global map
    try:
        if map[row][col] != '*':
            sprite = House(x, y, row, col, map)
            all_houses.add(sprite)
    except IndexError:
        print(row, col)


def create_houses(x, y, row, col, size):
    for i in range(row):
        for j in range(col):
            render_house(x + i * size, y + j * size, i, j)


def clear_map():
    cl_map = [['*'] * 8] * 8
    return cl_map


peoples_png = Stat(0, 750, peoples, 'peoples.png')
money_png = Stat(0, 800, mojo, 'mojo.png')
house_button = Button('homes.png', 0, 0, 64, 64, 'Город')
defeat_button = Button('defeat.png', 0, 65, 64, 64, 'Защита')
quest_button = Button('quest.png', 0, 130, 64, 64, 'Квесты')
escape_button = Button('escape.png', 0, 195, 64, 64, 'Выход')
play_menu_button = Button('game.png', 600, 300, 64, 64, 'Играть', 0)
escape_menu_button = Button('escape.png', 600, 370, 64, 64, 'Выход из игры', 0)
escape_quest_button = Button('escape.png', 0, 0, 64, 64, '')

mojo_anim = AnimatedSprite(load_image(r'test_animations\mojo_anim.png'), 11, 1, 0, 800)
peoples_anim = AnimatedSprite(load_image(r'test_animations\peoples_anim.png'), 6, 1, 0, 750)
quest_sprite_form_1 = Quest('quest_form.png', 500, 100)
quest_sprite_form_2 = Quest('quest_form.png', 500, 250)
quest_sprite_form_3 = Quest('quest_form.png', 500, 400)
quest_sprite_form_4 = Quest('quest_form.png', 500, 550)
background = load_image('background.png')
all_buttons.add(house_button)
all_buttons.add(escape_button)
all_buttons.add(defeat_button)
all_buttons.add(quest_button)
all_another_sprites.add(money_png)
all_another_sprites.add(peoples_png)
anim_sprites.add(mojo_anim)
anim_sprites.add(peoples_anim)
menu_sprites.add(play_menu_button)
menu_sprites.add(escape_menu_button)
quest_sprites.add(quest_sprite_form_1)
quest_sprites.add(quest_sprite_form_2)
quest_sprites.add(quest_sprite_form_3)
quest_sprites.add(quest_sprite_form_4)
quest_sprites.add(escape_quest_button)
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
