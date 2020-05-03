import math
import arcade
from random import randrange
from src.pcNpc.LivingBeing import LivingBeing


class Enemy(LivingBeing):
    # Cambiar medidas de la ventana por las de la Habitacion
    def __init__(self, position_x: int, position_y: int):
        super().__init__(position_x, position_y, "./resources/sprites/enemies/alienZombie.png", 1)
        self.center_x = position_x
        self.center_y = position_y

    def follow_sprite(self, player_sprite):
        if self.center_y < player_sprite.center_y:
            self.center_y += min(self.speed, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(self.speed, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(self.speed, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(self.speed, self.center_x - player_sprite.center_x)

    def go_to(self, x, y, delta_time):
        dx = self.center_x - x
        dy = self.center_y - y
        d = math.sqrt(dx ** 2 + dy ** 2)
        if d == 0:
            d = 0.0001
        self.change_x = -self.speed / d * dx * delta_time
        self.change_y = -self.speed / d * dy * delta_time

    def draw_debug(self):
        self.draw()
        self.draw_hit_box()
