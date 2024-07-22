import pygame
class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self):
        # Настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = pygame.image.load("images.jpg")
        self.bg_color_point=(0,0,0)

        # Настройки корабля
        self.ship_limit = 3
        self.ship_speed= 5

        # Параметры снаряда
        self.bullet_speed=10
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (28,170,214)
        self.bullets_allowed=3


        #Настройки пришельцев
        self.alien_speed=2
        self.fleet_drop_speed=10
        self.fleet_derection=1
        self.alien_points = 50



