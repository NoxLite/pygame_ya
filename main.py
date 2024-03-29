import pygame
import os
import random
import sys
import json

'''подготовка данных'''
pygame.init()
pygame.font.init()
buttons_clicked = [False, False, False]
all_houses = pygame.sprite.Group()
all_buttons = pygame.sprite.Group()
all_another_sprites = pygame.sprite.Group()
all_cells_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
quest_sprites = pygame.sprite.Group()
save_sprites = pygame.sprite.Group()
confirmation_sprites = pygame.sprite.Group()
quest_form = None
houses = ['home_1.png', 'home_2.png', 'home_3.png', 'home_4.png']
choise = 1
choise_type = 'Houses'
types = {1: 'Выбор', 2: 'Дом(100)'}
types_school = {1: 'Выбор', 2: 'Школа'}
types_work = {1: 'Выбор', 2: 'Завод', 3: 'Оффис'}
quest_info = {}
pygame.mixer.music.load(r'data\sound.mp3')
text_font = pygame.font.Font('text.ttf', 30)
tittle_font = pygame.font.Font('title.ttf', 180)
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
running_menu = True
running_game = False
running_quest = False
running_save = False
running_confirmation = False
logo = tittle_font.render('YA_GAME', True, 'white')
clock = pygame.time.Clock()
clock.tick(10)
delete_save = 0
info_build = {'type': 'None'}
info_map = {}
inf = {}
mojo = 0
peoples = 0
completed_quest = 0
completed_quest_info = [{}, {}, {}, {}]
address = 1


# карта
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

    #  проверка нажатий
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

    # размещение новых объектов на карте
    def place(self, choise):
        global info_map
        global mojo
        global peoples
        my_map = info_map
        print(choise, choise_type)
        if choise == 2 and choise_type == 'Houses':
            if my_map[f'{self.row}, {self.col}']['type'] == 'grass':
                if mojo >= 100:
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
        if choise == 2 and choise_type == 'Edu':
            if my_map[f'{self.row}, {self.col}']['type'] == 'grass':
                if mojo >= 200:
                    my_map[f'{self.row}, {self.col}']['type'] = 'school'
                    my_map[f'{self.row}, {self.col}']['current_level'] = '1'
                    my_map[f'{self.row}, {self.col}']['max_level'] = '5'
                    my_map[f'{self.row}, {self.col}']['image'] = 'school.png'
                    render_house(self.x_cell, self.y_cell, self.row, self.col)
                    mojo -= 200
                    money_png.change_stat(mojo)
        if choise == 2 and choise_type == 'Work':
            if my_map[f'{self.row}, {self.col}']['type'] == 'grass':
                if mojo >= 200:
                    my_map[f'{self.row}, {self.col}']['type'] = 'factory'
                    my_map[f'{self.row}, {self.col}']['current_level'] = '1'
                    my_map[f'{self.row}, {self.col}']['max_level'] = '20'
                    my_map[f'{self.row}, {self.col}']['image'] = 'factory.png'
                    render_house(self.x_cell, self.y_cell, self.row, self.col)
                    mojo -= 200
                    money_png.change_stat(mojo)
        if choise == 3 and choise_type == 'Work':
            if my_map[f'{self.row}, {self.col}']['type'] == 'grass':
                if mojo >= 200:
                    my_map[f'{self.row}, {self.col}']['type'] = 'office'
                    my_map[f'{self.row}, {self.col}']['current_level'] = '1'
                    my_map[f'{self.row}, {self.col}']['max_level'] = '20'
                    my_map[f'{self.row}, {self.col}']['image'] = 'office.png'
                    render_house(self.x_cell, self.y_cell, self.row, self.col)
                    mojo -= 200
                    money_png.change_stat(mojo)
        info_map = my_map


# спрайт клетки карты
class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('grass_texture.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.convert()


#  кнопка
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


#  спрайт дома
class House(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col):
        super().__init__()
        self.image = load_image(info_map[f'{row}, {col}']['image'])
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# спрайт школы
class School(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col):
        super().__init__()
        self.image = load_image(info_map[f'{row}, {col}']['image'])
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# спрайт оффиса
class Office(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col):
        super().__init__()
        self.image = load_image(info_map[f'{row}, {col}']['image'])
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# спрайт завода
class Factory(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col):
        super().__init__()
        self.image = load_image(info_map[f'{row}, {col}']['image'])
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#  спрайты для статистики (монеты, количество людей)
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

    # прорисовка
    def render(self, screen):
        pygame.draw.rect(screen, 'black', (self.x, self.y, 200, 50), 0)
        screen.blit(self.stat, (self.x + 60, self.y + 10))

    def change_stat(self, stat):
        self.stat = text_font.render(str(stat), True, 'green')


#  квест
class Quest(pygame.sprite.Sprite):
    def __init__(self, image, x, y, num_of_que):
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
        self.num_of_que = num_of_que

    # создание информации для квеста
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
        if self.get_it is False:
            self.money.image = load_image(r'buttons_test\mojo_quest.png')
        else:
            self.money.image = load_image(r'buttons_test\completed7.png')
        self.money.rect = self.money.image.get_rect()
        self.money.rect.x = self.x + 30
        self.money.rect.y = self.y - 10
        self.completed_sprites = pygame.sprite.Group()
        self.completed_sprites.add(self.money)
        self.completed_sprites.draw(screen)

    # проверка нажатий
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
                    completed_quest_info[self.num_of_que]['getting'] = True

    #  проверка выполнения квеста
    def check(self):
        if self.type in [0, 3]:
            global peoples
            if self.current_value != peoples:
                self.progress = peoples - self.current_value
        if self.type in [1, 2]:
            if get_houses_count() != self.current_value:
                self.progress = get_houses_count() - self.current_value
        completed_quest_info[self.num_of_que]['comp'] = self.progress
        if self.progress >= int(quest_form[self.type][3]):
            self.completed = text_font.render(f'{self.progress}/{quest_form[self.type][3]}', True, 'green')
        else:
            self.completed = text_font.render(f'{self.progress}/{quest_form[self.type][3]}', True, 'white')


# меню
def menu():
    global running_menu
    global running_game
    global running_save
    screen.fill('blue')
    while running_menu:
        screen.fill('blue')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_sprites.update(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    running_menu = False
        menu_sprites.draw(screen)
        play_menu_button.draw(screen)
        escape_menu_button.draw(screen)
        screen.blit(logo, (400, 10))
        pygame.display.update()
        if play_menu_button.is_clicked:
            running_menu = False
            running_save = True
            play_menu_button.is_clicked = False
        if escape_menu_button.is_clicked:
            running_menu = False
        pygame.display.flip()


# игра и её интерфейс
def game():
    global choise, all_houses, mojo, running_game, choise_defeat, running_quest, info_build, choise_type, running_menu
    board = Map(8, 8, 100, 400, 20)
    create_houses(400, 20, 8, 8, 100)
    work_active = False
    edu_active = False
    house_active = True
    houses_info = []
    keys = [elem for elem in types.keys()]
    for i in range(len(types.keys())):
        if choise == keys[i]:
            text = text_font.render(f'{keys[i]} {types[keys[i]]}', True, 'yellow')
        else:
            text = text_font.render(f'{keys[i]} {types[keys[i]]}', True, 'blue')
        houses_info.append(text)
    money_png.change_stat(mojo)
    peoples_png.change_stat(peoples)
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
                        keys = [elem for elem in types.keys()]
                        houses_info = []
                        for i in range(len(types.keys())):
                            if choise == keys[i]:
                                text = text_font.render(f'{keys[i]} {types[keys[i]]}', True, 'yellow')
                            else:
                                text = text_font.render(f'{keys[i]} {types[keys[i]]}', True, 'blue')
                            houses_info.append(text)
                    if education_button.is_clicked:
                        choise = event.key - 48
                        keys = [elem for elem in types_school.keys()]
                        houses_info = []
                        for i in range(len(types_school.keys())):
                            if choise == keys[i]:
                                text = text_font.render(f'{keys[i]} {types_school[keys[i]]}', True, 'yellow')
                            else:
                                text = text_font.render(f'{keys[i]} {types_school[keys[i]]}', True, 'blue')
                            houses_info.append(text)
                    if work_button.is_clicked:
                        choise = event.key - 48
                        keys = [elem for elem in types_work.keys()]
                        houses_info = []
                        for i in range(len(types_work.keys())):
                            if choise == keys[i]:
                                text = text_font.render(f'{keys[i]} {types_work[keys[i]]}', True, 'yellow')
                            else:
                                text = text_font.render(f'{keys[i]} {types_work[keys[i]]}', True, 'blue')
                            houses_info.append(text)
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
        work_button.draw(screen)
        quest_button.draw(screen)
        escape_button.draw(screen)
        upgrade_button.draw(screen)
        education_button.draw(screen)
        all_cells_sprites.draw(screen)
        all_houses.draw(screen)
        all_buttons.draw(screen)

        money_png.render(screen)
        peoples_png.render(screen)

        all_another_sprites.draw(screen)

        if house_button.is_clicked:
            if house_active is False:
                keys = [elem for elem in types.keys()]
                houses_info = []
                for i in range(len(types.keys())):
                    if choise == keys[i]:
                        text = text_font.render(f'{keys[i]} {types[keys[i]]}', True, 'yellow')
                    else:
                        text = text_font.render(f'{keys[i]} {types[keys[i]]}', True, 'blue')
                    houses_info.append(text)
                house_active = True
                edu_active = False
                work_active = False
                choise_type = 'Houses'
                choise = 1
            for i in range(len(houses_info)):
                screen.blit(houses_info[i], (0, 320 + i * 50))
        if education_button.is_clicked:
            if edu_active is False:
                keys = [elem for elem in types_school.keys()]
                houses_info = []
                for i in range(len(types_school.keys())):
                    if choise == keys[i]:
                        text = text_font.render(f'{keys[i]} {types_school[keys[i]]}', True, 'yellow')
                    else:
                        text = text_font.render(f'{keys[i]} {types_school[keys[i]]}', True, 'blue')
                    houses_info.append(text)
                edu_active = True
                house_active = False
                work_active = False
                choise_type = 'Edu'
                choise = 1
            for i in range(len(houses_info)):
                screen.blit(houses_info[i], (0, 320 + i * 50))
        if work_button.is_clicked:
            if work_active is False:
                keys = [elem for elem in types_work.keys()]
                houses_info = []
                for i in range(len(types_work.keys())):
                    if choise == keys[i]:
                        text = text_font.render(f'{keys[i]} {types_work[keys[i]]}', True, 'yellow')
                    else:
                        text = text_font.render(f'{keys[i]} {types_work[keys[i]]}', True, 'blue')
                    houses_info.append(text)
                edu_active = False
                house_active = False
                work_active = True
                choise_type = 'Work'
                choise = 1
            for i in range(len(houses_info)):
                screen.blit(houses_info[i], (0, 320 + i * 50))
        if escape_button.is_clicked:
            saving()
            clear_map()
            running_game = False
            running_menu = True
            escape_button.is_clicked = False
        if upgrade_button.is_clicked:
            check_info_build()
            upgrade_button.is_clicked = False
        if quest_button.is_clicked:
            money_png.change_stat(mojo)

            quest_button.draw_choise(screen)
            quest_button.is_clicked = False
            running_game = False
            running_quest = True
        pygame.display.flip()


# экран квестов
def quest():
    global running_quest, running_game, completed_quest, completed_quest_info
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
        pygame.display.flip()
    running_game = True
    if completed_quest == 4:
        for i in range(len(completed_quest_info)):
            completed_quest_info[i]['type'] = random.randint(0, 3)
        quest_sprite_form_1.set_quest(completed_quest_info[0]['type'])
        quest_sprite_form_2.set_quest(completed_quest_info[1]['type'])
        quest_sprite_form_3.set_quest(completed_quest_info[2]['type'])
        quest_sprite_form_4.set_quest(completed_quest_info[3]['type'])
        completed_quest_info[0]['comp'] = 0
        completed_quest_info[1]['comp'] = 0
        completed_quest_info[2]['comp'] = 0
        completed_quest_info[3]['comp'] = 0
        completed_quest_info[0]['getting'] = False
        completed_quest_info[1]['getting'] = False
        completed_quest_info[2]['getting'] = False
        completed_quest_info[3]['getting'] = False
        quest_sprite_form_1.progress = completed_quest_info[0]['comp']
        quest_sprite_form_2.progress = completed_quest_info[1]['comp']
        quest_sprite_form_3.progress = completed_quest_info[2]['comp']
        quest_sprite_form_4.progress = completed_quest_info[3]['comp']
        quest_sprite_form_1.get_it = False
        quest_sprite_form_2.get_it = False
        quest_sprite_form_3.get_it = False
        quest_sprite_form_4.get_it = False
        completed_quest = 0


# окно с выбором сохранения
def load_save():
    global screen, running_save, running_menu, running_game, address, delete_save, running_confirmation
    while running_save:
        screen.fill('blue')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_save = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                save_sprites.update(event.pos)

        save_sprites.draw(screen)
        save_1.draw(screen)
        save_2.draw(screen)
        save_3.draw(screen)
        escape_save_button.draw(screen)

        if escape_save_button.is_clicked:
            running_save = False
            running_menu = True
            escape_save_button.is_clicked = False

        if save_1.is_clicked:
            address = '1'
            load_files()
            save_1.is_clicked = False
            running_game = True
            running_save = False
        elif save_2.is_clicked:
            address = '2'
            load_files()
            save_2.is_clicked = False
            running_game = True
            running_save = False
        elif save_3.is_clicked:
            address = '3'
            load_files()
            save_3.is_clicked = False
            running_game = True
            running_save = False
        if delete_1.is_clicked:
            running_save = False
            running_confirmation = True
            delete_1.is_clicked = False
            delete_save = 1
        if delete_2.is_clicked:
            running_save = False
            running_confirmation = True
            delete_2.is_clicked = False
            delete_save = 2
        if delete_3.is_clicked:
            running_save = False
            running_confirmation = True
            delete_3.is_clicked = False
            delete_save = 3
        pygame.display.flip()


# окно с подтверждением
def confirmation():
    global running_confirmation, running_save, running_menu, confirmation_sprites
    while running_confirmation:
        screen.fill('blue')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                confirmation_sprites.update(event.pos)
        confirmation_sprites.draw(screen)
        ok.draw(screen)
        no.draw(screen)
        if ok.is_clicked:
            deleter()
            ok.is_clicked = False
            running_confirmation = False
            running_save = True
        if no.is_clicked:
            no.is_clicked = False
            running_confirmation = False
            running_save = True
        pygame.display.flip()


#  удаление сохранения
def deleter():
    global completed_quest_info, mojo, peoples, completed_quest, info_map
    completed_quest_info = [{}, {}, {}, {}]
    for i in range(4):
        completed_quest_info[i]['type'] = -1
        completed_quest_info[i]['comp'] = 0
        completed_quest_info[i]['getting'] = False
    mojo = 1000
    peoples = 0
    completed_quest = 0
    for i in range(0, 9):
        for j in range(0, 9):
            info_map[f'{i}, {j}'] = {}
            info_map[f'{i}, {j}']['type'] = 'grass'
            info_map[f'{i}, {j}']['current_level'] = 0
            info_map[f'{i}, {j}']['max_level'] = 0
            info_map[f'{i}, {j}']['image'] = None
            info_map[f'{i}, {j}']['peoples'] = [0]
    file = open(f'saves\\{delete_save}\\map.json', 'w')
    json.dump(info_map, file)
    file.close()
    file = open(f'saves\\{delete_save}\\info_player.json', 'w')
    json.dump({'mojo': mojo, 'peoples': peoples, 'completed': completed_quest}, file)
    file.close()
    file = open(f'saves\\{delete_save}\\completed_quests.json', 'w')
    json.dump(completed_quest_info, file)
    file.close()


#  загрузка изображения
def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


# прорисовка домов
def render_house(x, y, row, col):
    global all_houses, info_map
    try:
        if info_map[f'{row}, {col}']['type'] == 'house':
            sprite = House(x, y, row, col)
            all_houses.add(sprite)
        if info_map[f'{row}, {col}']['type'] == 'school':
            sprite = School(x, y, row, col)
            all_houses.add(sprite)
        if info_map[f'{row}, {col}']['type'] == 'factory':
            sprite = Factory(x, y, row, col)
            all_houses.add(sprite)
        if info_map[f'{row}, {col}']['type'] == 'office':
            sprite = Office(x, y, row, col)
            all_houses.add(sprite)
    except IndexError:
        print(row, col)


def create_houses(x, y, row, col, size):
    for i in range(row):
        for j in range(col):
            render_house(x + i * size, y + j * size, i, j)


def clear_map():
    global info_map, all_houses
    for x in range(9):
        for y in range(9):
            info_map[f'{x}, {y}'] = {"type": "grass",
                                     "current_level": 0,
                                     "max_level": 0,
                                     "image": None,
                                     "peoples":
                                         [0]}
    all_houses = pygame.sprite.Group()


def get_houses_count():
    h_c = 0
    for key in list(info_map.keys()):
        if info_map[key]['type'] == 'house':
            h_c += 1
    return h_c


def get_info_build(map_index):
    global info_build
    info_build = map_index


# прорисовка информации о здании
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


#  проверка информации о здании
def check_info_build():
    global info_build, peoples, mojo
    if 'house' == info_build['type']:
        if mojo >= 100:
            if int(info_build['current_level']) < int(info_build['max_level']):
                info_build['current_level'] = str(int(info_build['current_level']) + 1)
                peoples += random.randint(1, 100)
                peoples_png.change_stat(peoples)
                mojo -= 100
                money_png.change_stat(mojo)


# очистка сохранения
def clear_files():
    global info_map, inf, mojo, peoples, completed_quest, completed_quest_info, all_houses, choise, choise_type
    info_map = {}
    inf = {}
    mojo = 1000
    peoples = 0
    completed_quest = 0
    completed_quest_info = {}
    choise = 1
    choise_type = 'Houses'
    all_houses = pygame.sprite.Group()
    clear_map()


# загрузка сохранения
def load_files():
    global quest_form, info_map, inf, mojo, peoples, completed_quest, completed_quest_info, address
    quest_form = [elem[:-1].split('/') for elem in open('''quests.txt''', 'r', encoding='utf8').readlines()]
    print(address)
    for elem in quest_form:
        quest_form[int(elem[0])] = [elem[1], int(elem[2]), elem[3], elem[4]]
    with open(f'saves\{address}\map.json') as mapjson:
        info_map = json.load(mapjson)
    with open(f'saves\{address}\info_player.json') as playerjson:
        inf = json.load(playerjson)
        mojo = inf['mojo']
        peoples = inf['peoples']
        completed_quest = inf['completed']
    with open(f'saves\{address}\completed_quests.json') as quesjson:
        completed_quest_info = json.load(quesjson)
    for i in range(len(completed_quest_info)):
        if completed_quest_info[i]['type'] == -1:
            completed_quest_info[i]['type'] = random.randint(0, 3)
    quest_sprite_form_1.set_quest(completed_quest_info[0]['type'])
    quest_sprite_form_2.set_quest(completed_quest_info[1]['type'])
    quest_sprite_form_3.set_quest(completed_quest_info[2]['type'])
    quest_sprite_form_4.set_quest(completed_quest_info[3]['type'])
    quest_sprite_form_1.progress = completed_quest_info[0]['comp']
    quest_sprite_form_2.progress = completed_quest_info[1]['comp']
    quest_sprite_form_3.progress = completed_quest_info[2]['comp']
    quest_sprite_form_4.progress = completed_quest_info[3]['comp']
    quest_sprite_form_1.get_it = completed_quest_info[0]['getting']
    quest_sprite_form_2.get_it = completed_quest_info[1]['getting']
    quest_sprite_form_3.get_it = completed_quest_info[2]['getting']
    quest_sprite_form_4.get_it = completed_quest_info[3]['getting']


# сохранение игры
# происходит при каждом выходе в меню
def saving():
    global info_map, mojo, peoples, completed_quest, completed_quest_info
    file = open(f'saves\\{address}\\map.json', 'w')
    json.dump(info_map, file)
    file.close()
    file = open(f'saves\\{address}\\info_player.json', 'w')
    json.dump({'mojo': mojo, 'peoples': peoples, 'completed': completed_quest}, file)
    file.close()
    file = open(f'saves\\{address}\\completed_quests.json', 'w')
    json.dump(completed_quest_info, file)
    file.close()


# создание всех спрайтов, необходимых для игры
peoples_png = Stat(0, 750, peoples, 'peoples.png')
money_png = Stat(0, 800, mojo, 'mojo.png')
house_button = Button('homes.png', 0, 0, 64, 64, 'Город')
defeat_button = Button('defeat.png', 0, 65, 64, 64, 'Защита')
quest_button = Button('quest.png', 0, 130, 64, 64, 'Квесты')
education_button = Button('education.png', 0, 195, 64, 64, 'Образование')
escape_button = Button('escape.png', 0, 260, 64, 64, 'Выход')
play_menu_button = Button('game.png', 600, 300, 64, 64, 'Играть', 0)
escape_menu_button = Button('escape.png', 600, 370, 64, 64, 'Выход из игры', 0)
escape_quest_button = Button('escape.png', 0, 0, 64, 64, '')
upgrade_button = Button('upgrade.png', 1460, 75, 64, 64, '')
work_button = Button('work.png', 0, 65, 64, 64, 'Работа')
save_1 = Button('game.png', 600, 230, 64, 64, 'Сохранение 1', 0)
save_2 = Button('game.png', 600, 300, 64, 64, 'Сохранение 2', 0)
save_3 = Button('game.png', 600, 370, 64, 64, 'Сохранение 3', 0)
delete_1 = Button('delete.png', 530, 230, 64, 64, '', 0)
delete_2 = Button('delete.png', 530, 300, 64, 64, '', 0)
delete_3 = Button('delete.png', 530, 370, 64, 64, '', 0)
ok = Button('ok.png', 600, 300, 64, 64, 'Да', 0)
no = Button('delete.png', 600, 370, 64, 64, 'Нет', 0)
escape_save_button = Button('escape.png', 600, 440, 64, 64, 'Обратно в меню', 0)
quest_sprite_form_1 = Quest('quest_form.png', 500, 100, 0)
quest_sprite_form_2 = Quest('quest_form.png', 500, 250, 1)
quest_sprite_form_3 = Quest('quest_form.png', 500, 400, 2)
quest_sprite_form_4 = Quest('quest_form.png', 500, 550, 3)
background = load_image('background.png')
all_buttons.add(house_button)
all_buttons.add(escape_button)
all_buttons.add(work_button)
all_buttons.add(upgrade_button)
all_buttons.add(quest_button)
all_buttons.add(education_button)
all_another_sprites.add(money_png)
all_another_sprites.add(peoples_png)
save_sprites.add(save_1)
save_sprites.add(save_2)
save_sprites.add(save_3)
save_sprites.add(delete_1)
save_sprites.add(delete_2)
save_sprites.add(delete_3)
save_sprites.add(escape_save_button)
menu_sprites.add(play_menu_button)
menu_sprites.add(escape_menu_button)
quest_sprites.add(quest_sprite_form_1)
quest_sprites.add(quest_sprite_form_2)
quest_sprites.add(quest_sprite_form_3)
quest_sprites.add(quest_sprite_form_4)
quest_sprites.add(escape_quest_button)
confirmation_sprites.add(ok)
confirmation_sprites.add(no)
if __name__ == '__main__':
    pygame.mixer.music.play(-1)
    while running_menu or running_game or running_quest or running_save:
        if running_menu:
            menu()
        if running_save:
            load_save()
        if running_game:
            game()
        if running_quest:
            quest()
        if running_confirmation:
            confirmation()
