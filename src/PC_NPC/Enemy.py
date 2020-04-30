import math
import arcade
from random import randrange


class Enemy(LivingBeing):
    #Cambiar medidas de la ventana por las de la Habitacion
    def __init__(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int, image: str, scale: float):
        self.eje_x = SCREEN_WIDTH
        self.eje_y = SCREEN_HEIGHT
        self.position_x = randrange(1, SCREEN_WIDTH, 1)
        self.position_y = randrange(1, SCREEN_HEIGHT, 1)
        super().__init__(self.position_x, self.position_y, image, scale)

    def follow_sprite(self,SPRITE_SPEED, player_sprite):
        if self.center_y < player_sprite.center_y:
            self.center_y += min(SPRITE_SPEED, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(SPRITE_SPEED, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(SPRITE_SPEED, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(SPRITE_SPEED, self.center_x - player_sprite.center_x)

    def draw_debug(self):
        self.sprite.draw()
