import pygame
from ship import Ship
from pygame.sprite import Group

class Scoreboard():
    def __init__(self, ai_game):

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка изображений счетов.
        self.prep_score()
        self.prep_high_score()
        self.prep_ship()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Вывод счета в правой верхней части экрана.
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
        """Преобразует рекордный счет в графическое изображение."""
        high_score = str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score, True, self.text_color)
        # Рекорд выравнивается по центру верхней стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
