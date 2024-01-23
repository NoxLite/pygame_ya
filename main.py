import pygame
import os
import random
import sys
import json

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
quest_form = [elem[:-1].split('/') for elem in open('quests.txt', 'r', encoding='utf8').readlines()]
houses = ['home_1.png', 'home_2.png', 'home_3.png', 'home_4.png']
choise = 1
types = {1: 'Выбор', 2: 'Дом(100)', 'c': 'Очистить карту'}
types_defeat = {1: 'Пушки', 2: 'Армия', 3: 'Ряд танков', 4: 'Самолеты'}
quest_info = {}
for elem in quest_form:
    quest_form[int(elem[0])] = [elem[1], int(elem[2]), elem[3], elem[4]]
choise_defeat = 1
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
info_build = {'type': 'None'}
with open('map.json') as mapjson:
    info_map = json.load(mapjson)
with open('info_playe.json') as playerjson:
    inf = json.load(playerjson)
    mojo = inf['mojo']
    peoples = inf['peoples']


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
        global info_map
        global mojo
        global peoples
        my_map = info_map
        if choise == 2:
            if my_map[f'{self.row}, {self.col}']['type'] == 'grass':
                my_map[f'{self.row}, {self.col}']['type'] = 'house'
                my_map[f'{self.row}, {self.col}']['current_level'] = '1'
                my_map[f'{self.row}, {self.col}']['max_level'] = '10'
                my_map[f'{self.row}, {self.col}']['image'] = 'home_' + str(random.randrange(1, 5)) + '.png'
                plus_peoples = random.randint(1, 123)
                my_map[f'{self.row}, {self.col}']['peoples'] = [plus_peoples]
                render_house(self.x_cell, self.y_cell, self.row, self.col)
                mojo -= 100
                money_png.change_stat(mojo)
                peoples += plus_peoples
                peoples_png.change_stat(peoples)
        if choise == 1:
            get_info_build(my_map[f'{self.row}, {self.col}'])
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
    def __init__(self, x, y, row, col):
        super().__init__()
        self.image = load_image(info_map[f'{row}, {col}']['image'])
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
        self.current_value = 0
        self.progress = 0
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

    def set_quest(self, id):
        global peoples
        self.completed_sprites = pygame.sprite.Group()
        self.money = Button('mojo_quest.png', self.x + 30, self.y - 10, 100, 150)
        self.type = id
        if self.type in [0, 3]:
            self.current_value = peoples
        if self.type in [1, 2]:
            self.current_value = get_houses_count()
        global quest_form
        self.completed_sprites.add(self.money)
        self.pay = text_font.render(str(quest_form[self.type][1]), True, 'green')
        self.completed = text_font.render(f'{self.progress}/{quest_form[self.type][3]}', True, 'white')
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
                if self.progress >= int(quest_form[self.type][3]):
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

    def check(self):
        if self.type in [0, 3]:
            global peoples
            if self.current_value != peoples:
                self.progress = peoples - self.current_value
        if self.type in [1, 2]:
            if get_houses_count() != self.current_value:
                self.progress = get_houses_count() - self.current_value
        if self.progress >= int(quest_form[self.type][3]):
            self.completed = text_font.render(f'{self.progress}/{quest_form[self.type][3]}', True, 'green')
        else:
            self.completed = text_font.render(f'{self.progress}/{quest_form[self.type][3]}', True, 'white')


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
    global choise, all_houses, mojo, running_game, choise_defeat, running_quest, info_build
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
                    clear_map()
                    all_houses = pygame.sprite.Group()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.get_click(event.pos):
                    board.place(choise)
                all_buttons.update(event.pos)
        quest_sprite_form_1.check()
        quest_sprite_form_2.check()
        quest_sprite_form_3.check()
        quest_sprite_form_4.check()
        screen.fill('black')
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, 'black', (0, 0, 300, 2000), 0)
        pygame.draw.rect(screen, 'black', (1250, 0, 300, 2000), 0)
        draw_info_build(screen)
        house_button.draw(screen)
        defeat_button.draw(screen)
        quest_button.draw(screen)
        escape_button.draw(screen)
        upgrade_button.draw(screen)

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
        if upgrade_button.is_clicked:
            check_info_build()
            upgrade_button.is_clicked = False
        if quest_button.is_clicked:
            money_png.change_stat(mojo)

            quest_button.draw_choise(screen)
            quest_button.is_clicked = False
            running_game = False
            running_quest = True
        pygame.display.update()
    if running_quest:
        sys.exit(quest())


def quest():
    global running_quest, running_game, m, c, completed_quest
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
        quest_sprite_form_1.set_quest(random.randint(0, 3))
        quest_sprite_form_2.set_quest(random.randint(0, 3))
        quest_sprite_form_3.set_quest(random.randint(0, 3))
        quest_sprite_form_4.set_quest(random.randint(0, 3))
        completed_quest = 0
    sys.exit(game())


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
        if info_map[f'{row}, {col}']['type'] != 'grass':
            sprite = House(x, y, row, col)
            all_houses.add(sprite)
    except IndexError:
        print(row, col)


def create_houses(x, y, row, col, size):
    for i in range(row):
        for j in range(col):
            render_house(x + i * size, y + j * size, i, j)


def clear_map():
    global info_map
    for x in range(9):
        for y in range(9):
            info_map[f'{x}, {y}'] = {"type": "grass",
                                     "current_level": 0,
                                     "max_level": 0,
                                     "image": None,
                                     "peoples":
                                         [0]}


def get_houses_count():
    h_c = 0
    for key in list(info_map.keys()):
        if info_map[key]['type'] == 'house':
            h_c += 1
    return h_c


def get_info_build(map_index):
    global info_build
    info_build = map_index


def draw_info_build(screen):
    texts = []
    global info_build
    choised_spite = pygame.sprite.Group()
    if info_build['type'] == 'None':
        texts.append(text_font.render('Выберите здание', True, 'white'))
        texts.append(text_font.render('Данный тип', True, 'red'))
        texts.append(text_font.render('нельзя', True, 'red'))
        texts.append(text_font.render('Прокачивать', True, 'red'))
    if info_build['type'] == 'grass':
        texts.append(text_font.render('Трава', True, 'white'))
        texts.append(text_font.render('Данный тип', True, 'red'))
        texts.append(text_font.render('нельзя', True, 'red'))
        texts.append(text_font.render('Прокачивать', True, 'red'))
    if 'house' == info_build['type']:
        texts.append(text_font.render(f'Жилой дом', True, 'white'))
        texts.append(text_font.render(f'Уровень: {info_build["current_level"]}', True, 'white'))
        choised_spite.add(upgrade_button)
    for i in range(len(texts)):
        screen.blit(texts[i], (1260, 20 + i * 40))


def check_info_build():
    global info_build, peoples
    if 'house' == info_build['type']:
        if int(info_build['current_level']) < int(info_build['max_level']):
            info_build['current_level'] = str(int(info_build['current_level']) + 1)
            peoples += random.randint(1, 100)
            peoples_png.change_stat(peoples)


peoples_png = Stat(0, 750, peoples, 'peoples.png')
money_png = Stat(0, 800, mojo, 'mojo.png')
house_button = Button('homes.png', 0, 0, 64, 64, 'Город')
defeat_button = Button('defeat.png', 0, 65, 64, 64, 'Защита')
quest_button = Button('quest.png', 0, 130, 64, 64, 'Квесты')
escape_button = Button('escape.png', 0, 195, 64, 64, 'Выход')
play_menu_button = Button('game.png', 600, 300, 64, 64, 'Играть', 0)
escape_menu_button = Button('escape.png', 600, 370, 64, 64, 'Выход из игры', 0)
escape_quest_button = Button('escape.png', 0, 0, 64, 64, '')
upgrade_button = Button('upgrade.png', 1460, 75, 64, 64, '')
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
all_buttons.add(upgrade_button)
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
    quest_sprite_form_1.set_quest(random.randint(0, 3))
    quest_sprite_form_2.set_quest(random.randint(0, 3))
    quest_sprite_form_3.set_quest(random.randint(0, 3))
    quest_sprite_form_4.set_quest(random.randint(0, 3))
    menu()

file = open('map.json', 'w')
json.dump(info_map, file)
file.close()
file = open('info_playe.json', 'w')
json.dump({'mojo': mojo, 'peoples': peoples}, file)
file.close()
