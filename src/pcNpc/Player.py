import math
import arcade
from random import randrange
from src.pcNpc.LivingBeing import LivingBeing


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
