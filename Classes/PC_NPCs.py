import math
import arcade
from random import randrange


class LivingBeing(arcade.Sprite):
    def __init__(self, position_x, position_y, image: str, scale: float):
        super().__init__(image, scale)
        self.alive = True
        self.health = None
        self.center_x = position_x
        self.center_y = position_y
        self.change_x = 0
        self.change_y = 0
        self.radians = 0

    def upd_orientation(self, x, y):
        x_ = x - self.center_x
        y_ = y - self.center_y
        length = math.sqrt(x_ ** 2 + y_ ** 2)
        x_ /= length
        y_ /= length
        if y_ > 0:
            self.radians = math.acos(x_)
        else:
            self.radians = -math.acos(x_)

    def upd_position(self, screen_width, screen_height):
        # Move the ball
        self.center_y += self.change_y
        self.center_x += self.change_x

        # See if the ball hit the edge of the screen. If so, change direction
        if self.center_x < 0:
            self.center_x = 0
        if self.center_x > screen_width:
            self.center_x = screen_width
        if self.center_y < 0:
            self.center_y = 0
        if self.center_y > screen_height:
            self.center_y = screen_height

    def damage(self):
        if self.alive:
            self.health -= 1
            if self.health <= 0:
                self.alive = False

    def revive(self):
        if not self.alive:
            self.alive = True
            self.health = 1


class Player(LivingBeing):
    def __init__(self, position_x: int, position_y: int, image: str, scale: float):
        super().__init__(position_x, position_y, image, scale)
        self.weapon = "Machinegun"

    def speed_up(self, ud, lr, speed):
        if ud == "up":
            self.change_y = speed
        elif ud == "down":
            self.change_y = -speed
        if lr == "right":
            self.change_x = speed
        elif lr == "left":
            self.change_x = -speed

    def full_stop(self, axis: str):
        if axis == "x":
            self.change_x = 0
        if axis == "y":
            self.change_y = 0

    def draw_debug(self):
        self.sprite.draw()
        self.sprite.draw_hit_box(arcade.color.GREEN, 1)


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