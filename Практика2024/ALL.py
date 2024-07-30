import sys
from time import sleep
import pygame
import pygame.font
from pygame.sprite import Sprite,Group


class Settings():
    #Класс для хранения всех настроек игры Alien Invasion.
    def __init__(self):
         #Настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = pygame.image.load("images.jpg")
        self.bg_color_point=(0,0,0)

         #Настройки корабля
        self.ship_limit = 2
        self.ship_speed= 5

         #Параметры снаряда
        self.bullet_speed=10
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (28,170,214)
        self.bullets_allowed=3


        #Настройки пришельцев
        self.alien_speed=4
        self.fleet_drop_speed=10
        self.fleet_derection=1
        self.alien_points = 50
class Button():
    def __init__(self, ai_game,msg): #msg - строка, название кнопки
        #Инициализирует атрибуты подсчета очков.
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height=200, 50
        self.button_color=(0,0,0)
        self.text_colour=(255,255,255)
        self.font=pygame.font.SysFont(None,48)
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self,msg):
        self.msg_image=self.font.render(msg,True,self.text_colour, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

class Ship(Sprite):
    #Класс для управления кораблем.
    def __init__(self, ai_game):
        #Инициализирует корабль и задает его начальную позицию.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

         #Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('Cosmosshiptrue.png')
        self.rect = self.image.get_rect()
         #Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom

         #Сохранение вещественной координаты центра корабля.
        self.x = float(self.rect.x)

         #Флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
         #Обновляется атрибут x, не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

         #Обновление атрибута rect на основании self.x.
        self.rect.x = self.x

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
    #Размещает корабль в центре нижней стороны.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.image=pygame.image.load("alien.png")
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.settings=ai_game.settings
        self.x=float(self.rect.x)

    def _check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right >=screen_rect.right or self.rect.left <=0:
            return True

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_derection
        self.rect.x = self.x

class Bullet(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0 ,0 ,self.settings.bullet_width ,self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class GameStats():
    #Отслеживание статистики для игры Alien Invasion.

    def __init__(self, ai_game):
        #Инициализирует статистику.
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_active = False
        self.high_score=0

    def reset_stats(self):
        #Инициализирует статистику, изменяющуюся в ходе игры.
        self.ships_left = self.settings.ship_limit
        self.score=0

class Scoreboard():
    def __init__(self, ai_game):

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
         #Подготовка изображений счетов.
        self.prep_score()
        self.prep_high_score()
        self.prep_ship()

    def prep_score(self):
        #Преобразует текущий счет в графическое изображение.
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

         #Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_ship(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship=Ship(self.ai_game)
            ship.rect.x = 10+ship_number*ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        #Преобразует рекордный счет в графическое изображение.
        high_score = str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score, True, self.text_color)
        #Рекорд выравнивается по центру верхней стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        #Проверяет, появился ли новый рекорд.
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


class AlienInvasion():
    def __init__(self):
        pygame.init()
        self.settings=Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Инопрешеленцы")
        self.ship = Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self.moving_right=False
        self.moving_left=False
        self.stats=GameStats(self)
        self.shoot_sound = pygame.mixer.Sound('lazer.wav')
        self.play_button=Button(self,"Играть")
        self.sb=Scoreboard(self)
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _create_fleet(self):
        alien=Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width-(2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height-(3*alien_height)-ship_height)
        number_rows = available_space_y//(2*alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._creat_alien(alien_number, row_number)


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_derection *=-1



    def _creat_alien(self,alien_number,row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_alien_bottom()

    def _ship_hit(self):
        if self.stats.ships_left>0:
            self.stats.ships_left-=1
            self.sb.prep_ship()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_bottom(mouse_pos)

    def _check_play_bottom(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_ship()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key ==pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        if len(self.bullets) <self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
            self.shoot_sound.play()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        self._check_bullet_alion_colision()


    def _check_bullet_alion_colision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_screen(self):
        self.screen.blit(self.settings.bg_color,(0,0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()


        pygame.display.flip()
if __name__ == '__main__':
     #Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()

