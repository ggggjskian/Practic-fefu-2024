from pygame.sprite import Sprite
import pygame

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
