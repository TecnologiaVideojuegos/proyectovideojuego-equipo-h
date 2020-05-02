import math
import arcade
from random import randrange
from src.pcNpc.LivingBeing import LivingBeing


class Player(LivingBeing):
    def __init__(self, position_x: int, position_y: int):
        super().__init__(position_x, position_y, "./resources/sprites/player/shotgun.png", 1)

        # Skins
        self.append_texture(arcade.Texture("./resources/sprites/player/machinegun.png"))

        # Weapon
        self.weapon = "shotgun"
        self.shotgun_sound = arcade.Sound("./resources/sounds/shotgun.wav")
        self.machinegun_sound = arcade.Sound("./resources/sounds/machinegun.wav")

        # Movement
        self.speed = 500
        self.mov_ud = ""
        self.mov_lr = ""

        # Bullseye
        self.bullseye = arcade.Sprite("./resources/sprites/player/bullseye.png", 0.75)
        self.mouse_position = [0, 0]

    def upd_orientation(self, x=None, y=None):
        x_ = self.bullseye.center_x - self.center_x
        y_ = self.bullseye.center_y - self.center_y
        length = math.sqrt(x_ ** 2 + y_ ** 2)
        if length == 0:
            length = 0.00001
        x_ /= length
        y_ /= length
        if y_ > 0:
            self.radians = math.acos(x_)
        else:
            self.radians = -math.acos(x_)

    def speed_up(self, delta_time):
        if self.mov_ud == "up":
            self.change_y = self.speed * delta_time
        elif self.mov_ud == "down":
            self.change_y = -self.speed * delta_time
        elif self.mov_ud == "":
            self.change_y = 0
        if self.mov_lr == "right":
            self.change_x = self.speed * delta_time
        elif self.mov_lr == "left":
            self.change_x = -self.speed * delta_time
        elif self.mov_lr == "":
            self.change_x = 0

    def draw(self):
        super().draw()
        self.bullseye.draw()

    def draw_debug(self):
        super().draw()
        super().draw_hit_box(arcade.color.GREEN, 1)
        self.bullseye.draw()

    def bullseye_pos(self, bottom_x, left_y):
        self.bullseye.center_x = self.mouse_position[0] + bottom_x
        self.bullseye.center_y = self.mouse_position[1] + left_y
