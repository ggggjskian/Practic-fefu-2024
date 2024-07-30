
from time import sleep
import pygame
import sys
import shutil
from random import randrange
import os
import subprocess

TEXT = [['Это папка Windows. В ней нет вируса, ведь эта игра не настолько', 'кровожадна, чтобы ломать чужую систему.'],
        ['Там ничего нет.'], ['Там ничего нет.'], ['Вы ведь обошли все комнаты?'], ['Там же ничего нет...'],
        ['Знаете, а ведь там действительно ничего нет.'], ['Как и ни за одной дверью этого лабиринта...'],
        ['Потому, что вирусом является сама игра.', 'Да, ведь это она заразила компьютер шифровальщиком и поставила локер'],
        ['Ведь так вирусы и поступают, верно?'], ['Любом случае, чтобы удалиь вирус, нужно удалить игру.'],
        ['Итак, Вы даете согласие на удаление данной программы?'], ['Хотя на самом деле, Вас никто и не спрашивает.']]


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

pygame.display.set_caption('From me with love')
infoObject = pygame.display.Info()
size = width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
# pygame.mixer.music.load("data/sound/main_theme.mp3")
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(1)
# open_door = pygame.mixer.Sound("data/sound/door.ogg")
# text_sound = pygame.mixer.Sound('data/sound/text_sound.ogg')
# attack = pygame.mixer.Sound("data/sound/attack.ogg")
# #modem_sound = pygame.mixer.Sound('data/sound/modem_sound.mp3')


def load_image(name, dir, colorkey=None):
    fullname = os.path.join('data', dir, name)
    if not os.path.isfile(fullname):
        raise ValueError
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Wall(pygame.sprite.Sprite):
    def __init__(self, n, type, *group):
        super().__init__(*group)
        self.name, self.n = 'Wall', n
        width_size = 1572 * 0.45 if type == 'walls' else 519 * 0.45
        self.image = pygame.transform.scale(load_image(f"{type}.png", 'walls'), (width_size, 1439 * 0.45))
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.x = width // 2 - 1572 * 0.45 * 0.5 + n * (1572 * 0.45 - 178)
        self.rect.y = height // 2 - 1439 * 0.45 * 0.5


class Hero(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.name = 'Hero'
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - 1572 * 0.45 * 0.5
        self.rect.y = height // 2 + 30
        self.s, self.a, self.moving, self.key, self.is_back = 1, 1, False, pygame.K_RIGHT, False
        self.x = 0  # смещение
        self.attempts = 0

    def move(self, key):
        global draw_dialog, current_hall
        if self.key == pygame.K_RIGHT and 'wall_back1' not in [i.type for i in pygame.sprite.spritecollide(self,
                                                                        wall_sprites, False)] and not plagy_disabled:
            self.rect.x += 60
            self.x += 60
            if draw_dialog: draw_dialog = False
        elif self.key == pygame.K_RIGHT and 'wall_back1' in [i.type for i in pygame.sprite.spritecollide(self,
                                                                        wall_sprites, False)] and not plagy_disabled:
            if current_hall == m and not dark_mode:
                if self.attempts < 12:
                    draw_dialog = True
                    dialog.clear()
                    dialog.text_to_show = TEXT[self.attempts]
                    dialog.text = [''] * len(dialog.text_to_show)
                else:
                    subprocess.Popen(os.path.join(os.getcwd(), 'decryptor.exe'))
                    callback()
            else:
                pygame.mixer.music.load('data/sound/main_theme.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.play(-1)
                current_hall = m
                build_hall(current_hall)
        elif self.key == pygame.K_LEFT and self.x - 60 >= 0 and not plagy_disabled:
            self.rect.x -= 60
            self.x -= 60
            if draw_dialog:
                draw_dialog = False
                self.attempts += 1

    def update(self):
        if not self.moving:
            self.change_frame('plagy' if not self.is_back else 'plagyback')
        else:
            if self.s < 5:
                self.change_frame('plagyfly')
            self.move(self.key)
        if self.is_back and 'Plate' in [i.name for i in pygame.sprite.spritecollide(self, all_sprites, False)]:
            plate = [i for i in pygame.sprite.spritecollide(self, all_sprites, False) if i.name == 'Plate'][0]
            draw_window(plate.text)
        elif self.is_back and 'Door' in [i.name for i in pygame.sprite.spritecollide(self, all_sprites, False)]:
            self.find_door()

    def find_door(self):
        global draw_dialog
        door = [i for i in pygame.sprite.spritecollide(self, all_sprites, False) if i.name == 'Door'][0]
        if door.plate.text.upper() != '$RECYCLE.BIN' and not dark_mode or dark_mode and door.plate.text == 'Here':
            if not door.is_opening:
                open_door.play()
            door.is_opening = True
        elif not draw_dialog and not dark_mode:
            draw_dialog = True
            dialog.clear()
            dialog.text_to_show = ['Никто не любит копаться в мусоре...']
            dialog.text = ['']
        return door

    def change_frame(self, name):
        self.image = load_image(name + str(self.s) + '.png', 'plagy') if self.key == pygame.K_RIGHT else \
            pygame.transform.flip(load_image(name + str(self.s) + '.png', 'plagy'), True, False)
        self.s += self.a
        if not self.moving:
            self.rect.y -= self.a * 5
        if self.s > 5 or self.s < 1:
            self.a = -self.a
            self.s += self.a


class Door(pygame.sprite.Sprite):
    def __init__(self, wall, type, plate, *group):
        super().__init__(*group)
        self.name = 'Door'
        self.image = pygame.transform.scale(load_image(f"{type}.png", 'door'), (700 * 0.70, 852 * 0.70))
        self.rect = self.image.get_rect()
        self.rect.x = wall.rect.x + 60
        self.rect.y = wall.rect.y + 22
        self.n = wall.n
        self.s, self.is_opening, self.is_closing, self.a = 1, False, False, 1
        self.plate = plate
        self.mode, self.effect_played = 'light', False

    def update(self):
        global lose, plagy_disabled
        if self.mode == 'dark' and plagy.find_door() == self and self.plate.text != 'Escape':
            self.image = pygame.transform.scale(load_image(f'hands{self.s - 1}.png', 'hands'), (700 * 0.70, 852 * 0.70))
            if self.s - 1 < 11 and self.a > 0:
                self.s += self.a
            elif self.s - 1 > 0:
                plagy.kill()
                plagy_disabled = True
                self.a = -1
                self.s += self.a
            else:
                self.image = pygame.transform.scale(load_image(f'door1_dark.png', 'door'), (700 * 0.70, 852 * 0.70))
                if not lose:
                    lose = True
                    loser()
            if not self.effect_played:
                open_door.play()
                attack.play()
                self.effect_played = True
        elif self.is_opening and not self.is_closing:
            try:
                self.image = pygame.transform.scale(load_image(f'door{self.s}.png', 'door'), (700 * 0.70, 852 * 0.70))
            except ValueError:
                self.s -= 1
            if self.s < 6:
                self.s += 1
        elif self.is_closing:
            try:
                self.image = pygame.transform.scale(load_image(f'door{self.s}.png', 'door'), (700 * 0.70, 852 * 0.70))
            except ValueError:
                self.s += 1
            if self.s > 1:
                self.s -= 1


class Plate(pygame.sprite.Sprite):
    def __init__(self, wall, text, n, *group):
        super().__init__(*group)
        self.name = 'Plate'
        self.text, self.n = text, n
        self.image = pygame.transform.scale(load_image("plate.png", 'other'), (800 * 0.15, 472 * 0.15))
        self.rect = self.image.get_rect()
        self.rect.x = wall.rect.x + 5
        self.rect.y = wall.rect.y + 290


class Torch(pygame.sprite.Sprite):
    def __init__(self, wall, *group):
        super().__init__(*group)
        self.name = 'Torch'
        self.image = pygame.transform.scale(load_image("torch1.png", 'other'), (800 * 0.4, 800 * 0.4))
        self.rect = self.image.get_rect()
        self.rect.x = wall.rect.x - 90
        self.rect.y = wall.rect.y - 20
        self.s, self.fire = 1, True

    def update(self):
        if self.fire:
            self.image = pygame.transform.scale(load_image(f'torch{self.s}.png', 'other'), (800 * 0.4, 800 * 0.4))
            self.s += 1
            if self.s > 5:
                self.s = 1


class DialogWindow(pygame.sprite.Sprite):
    def __init__(self, text, font_size, x, y, w, h, *group):
        super().__init__(*group)
        self.image = pygame.Surface((w, h))
        self.font = pygame.font.SysFont('monotypecorsiva', font_size)
        pygame.draw.rect(self.image, (230, 230, 230), (0, 0, w, h), 10)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = self.text_to_show = text
        self.n = 0

    def clear(self):
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (230, 230, 230), (0, 0, width - 800, 200), 10)
        self.n = 0

    def update(self):
        height = 30
        if self.text[self.n] != self.text_to_show[self.n]:
            self.text[self.n] += self.text_to_show[self.n][len(self.text[self.n])]
            if self.text[self.n] == self.text_to_show[self.n] and self.n + 1 != len(self.text_to_show):
                self.n += 1
            text_sound.play()
        for i in range(self.n + 1):
            try:
                self.image.blit(self.font.render(self.text[i], True, (230, 230, 230)), (30, height))
            except IndexError:
                self.image.blit(self.font.render(self.text[i - 1], True, (230, 230, 230)), (30, height))
            height += 30


class Camera():
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self):
        self.dx = -(plagy.rect.x + plagy.rect.w // 2 - width // 2)


def draw_window(text):
    font = pygame.font.SysFont('monotypecorsiva', 35)
    text = font.render(text, True, (200, 200, 200))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (200, 200, 200), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)


def entering():
    global intro
    control_tm()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            intro = False
    pygame.display.flip()


def callback():
    pygame.quit()
    shutil.rmtree(os.getcwd())
    sys.exit()


def control_tm():
    for proc in psutil.process_iter():  # причина, по которой не открывается диспетчер задач :)
        if proc.name().lower() == 'taskmgr.exe':
            proc.terminate()


def screensaving():
    global screensaver
    control_tm()
    pyautogui.moveTo(text_x + 100, text_y + 10)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            screensaver = False
    pygame.display.flip()


maze = dict()
depth = 1





def build_hall(hall):
    global all_sprites, wall_sprites, dialog_sprite, plagy, clock, camera, current_hall
    all_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    current_hall = hall
    for d in range(len(hall.keys())):
        walls = Wall(d, 'walls', wall_sprites)
        all_sprites.add(walls)
        torch = Torch(walls, all_sprites)
        plate = Plate(walls, list(hall.keys())[d], d, all_sprites)
        door = Door(walls, 'door1', plate, all_sprites)
    walls = Wall(len(hall.keys()), 'wall_back1', wall_sprites)
    all_sprites.add(walls)
    plagy = Hero(all_sprites)


def darken(c):
    wall = [i for i in all_sprites.sprites() if i.name == 'Wall'][c // 15 - 1]
    wall.image = pygame.transform.scale(load_image("walls_dark.png", 'walls'), (1572 * 0.45, 1439 * 0.45))
    door = [i for i in all_sprites.sprites() if i.name == 'Door'][c // 15 - 1]
    door.image = pygame.transform.scale(load_image("door1_dark.png", 'door'), (700 * 0.70, 852 * 0.70))
    door.mode = 'dark'
    plate = [i for i in all_sprites.sprites() if i.name == 'Plate'][c // 15 - 1]
    plate.image = pygame.transform.scale(load_image("plate_dark.png", 'other'), (800 * 0.15, 472 * 0.15))
    torch = [i for i in all_sprites.sprites() if i.name == 'Torch'][c // 15 - 1]
    torch.image = pygame.transform.scale(load_image("torch_no_fire.png", 'other'), (800 * 0.4, 800 * 0.4))
    torch.fire = False


def loser():
    global draw_dialog, dialog, dialog_sprite
    dialog.kill()
    draw_dialog = True
    loser_window = DialogWindow('loseerrr', 60, width // 2 - 250, height // 2 - 100, 500, 200, dialog_sprite)
    loser_window.text_to_show = ['   Вы проиграли']
    loser_window.text = ['']


m = make_maze()
if 'yCharmProje' not in m.keys():
    m['PycharmProjects'] = {'???': []}

intro_text = 'Играть?'
font = pygame.font.SysFont('monotypecorsiva', 65)
text = font.render(intro_text, True, (230, 230, 230))
text_x = width // 2 - text.get_width() // 2
text_y = height // 2 - text.get_height() // 2
screen.blit(text, (text_x, text_y))

sleep(0.2)
screensaver, intro = True, True
while screensaver:
    screensaving()
screen.fill((0, 0, 0))
font = pygame.font.SysFont('monotypecorsiva', 30)
logo = pygame.transform.scale(load_image('icon.png', 'other'), (630 * 0.6, 630 * 0.6))
screen.blit(logo, (width - (630 * 0.6 + 70), height - (630 * 0.6 + 70)))
with open('data/opening.txt', encoding="utf8") as file:
    opening_text = file.readlines()
for n, line in enumerate(opening_text):
    screen.blit(font.render(line.strip(), True, (230, 230, 230)), (30, (n + 1) * 30))
while intro:
    entering()
current_hall = m
build_hall(current_hall)
clock = pygame.time.Clock()
camera = Camera()
dialog_sprite = pygame.sprite.Group()
dialog = DialogWindow('hey', 35, width // 2 - (width - 800) // 2, height - 200 - 50, width - 800, 200, dialog_sprite)
draw_dialog, dark_mode = False, False
e = 100000
lose, plagy_disabled = False, False
while True:
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    if draw_dialog:
        dialog_sprite.draw(screen)
        dialog_sprite.update()
    if not lose and not plagy_disabled:
        camera.update()
        for sprite in all_sprites:
            camera.apply(sprite)
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                plagy.moving = False
                plagy.is_back = False
        if event.type == pygame.KEYDOWN and not lose and not plagy_disabled:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                plagy.moving = True
                plagy.key = event.key
                plagy.s, plagy.a, plagy.is_back, plagy.rect.y = 1, 1, False, height // 2 + 30
            elif event.key == pygame.K_UP:
                if not plagy.is_back or not plagy.find_door().is_opening:
                    plagy.rect.y = height // 2 + 30
                    plagy.is_back = True
                else:
                    if plagy.find_door().plate.text == 'Here':
                        dark_mode = False
                        build_hall(m)
                        pygame.mixer.music.load('data/sound/main_theme.mp3')
                        pygame.mixer.music.play()
                        pygame.mixer.music.play(-1)
                    elif current_hall[plagy.find_door().plate.text] and plagy.find_door().plate.n != e:
                        if 'PycharmProject' in plagy.find_door().plate.text:
                            pygame.mixer.music.load('data/sound/modem_sound.mp3')
                            pygame.mixer.music.play()
                            draw_dialog = True
                            dialog.clear()
                            dialog.text_to_show = ['* Противные звуки шифрования файлов *']
                            dialog.text = ['']
                        build_hall(current_hall[plagy.find_door().plate.text])
                    elif plagy.find_door().plate.n == e:
                        draw_dialog = True
                        dialog.clear()
                        dialog.text_to_show = ['Там слишком темно.']
                        dialog.text = ['']
                        plagy.find_door().is_closing = True
                    else:
                        e = plagy.find_door().plate.n
                        dark_mode, c = True, 0
                        build_hall(m)
                        pygame.mixer.music.load('data/sound/chase.mp3')
                        pygame.mixer.music.play()
                        [i for i in wall_sprites if i.type == 'wall_back1'][0].image = \
                            pygame.transform.scale(load_image("wall_light.png", 'walls'), (400 * 0.45, 1439 * 0.45))
                        escape = randrange(len(m.keys()))
                        for i in [i for i in all_sprites.sprites() if i.name == 'Plate']:
                            i.text = 'Not Escape' if i.n != escape else 'Here'
                        for i in [i for i in all_sprites.sprites() if i.name == 'Door']:
                            i.s = 1
        elif event.type == pygame.KEYDOWN and lose:
            current_hall = m
            build_hall(current_hall)
            clock = pygame.time.Clock()
            camera = Camera()
            dialog_sprite = pygame.sprite.Group()
            dialog = DialogWindow('hey', 35, width // 2 - (width - 800) // 2, height - 200 - 50, width - 800, 200,
                                  dialog_sprite)
            draw_dialog, dark_mode = False, False
            e = 100000
            lose, plagy_disabled = False, False
            pygame.mixer.music.load('data/sound/main_theme.mp3')
            pygame.mixer.music.play()
            pygame.mixer.music.play(-1)
    if dark_mode and not lose and not plagy_disabled:
        c += 1
        if not c % 15 and c // 15 < len(m.keys()) + 1:
            darken(c)
        if not c % 15 and c // 15 == len(m.keys()):
            [i for i in wall_sprites if i.type == 'wall_back1'][0].image = \
                pygame.transform.scale(load_image("wall_back_dark.png", 'walls'), (400 * 0.45, 1439 * 0.45))
    all_sprites.update()
    clock.tick(15)
    pygame.display.flip()



