import math
import arcade
from random import randrange
from src.pcNpc.Bullet import Bullet
from src.pcNpc.LivingBeing import LivingBeing


class Player(LivingBeing):
    def __init__(self, position_x: int, position_y: int):
        """
        Creates an instance of the player (wielding a shotgun by default),
        although it contains the skin of every weapon.

        :param position_x: The initial x position of the player.
        :param position_y: The initial y position of the player.
        """

        super().__init__(position_x, position_y, "./resources/sprites/player/shotgun.png", 1)

        # Weapons
        self.textures = []
        self.textures.append("./resources/sprites/player/shotgun.png")
        self.textures.append("./resources/sprites/player/machinegun.png")

        # Health
        self.health = 10

        # Skins
        # self.append_texture(arcade.Texture("./resources/sprites/player/machinegun.png"))

        # Weapon
        self.weapon = "shotgun"
        # self.shooting = False
        self.shotgun_sound = arcade.Sound("./resources/sounds/shotgun.wav")
        self.machinegun_sound = arcade.Sound("./resources/sounds/machinegun.wav")
        self.shoot_count = 0

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

    def speed_up(self):
        if self.mov_ud == "up":
            self.change_y = self.speed
        elif self.mov_ud == "down":
            self.change_y = -self.speed
        elif self.mov_ud == "":
            self.change_y = 0
        if self.mov_lr == "right":
            self.change_x = self.speed
        elif self.mov_lr == "left":
            self.change_x = -self.speed
        elif self.mov_lr == "":
            self.change_x = 0

    def draw(self):
        super().draw()
        self.bullseye.draw()

    def draw_debug(self):
        super().draw()
        super().draw_hit_box(arcade.color.GREEN, 1)
        self.bullseye.draw()

    def bullseye_pos(self, left_x, bottom_y):
        self.bullseye.center_x = self.mouse_position[0] + left_x
        self.bullseye.center_y = self.mouse_position[1] + bottom_y

    def shoot(self, delta_time: float, reloading: bool):
        """
        Creates the bullets shot by the player depending on the weapon he's wielding.

        :param reloading: Parameter to reload even if the player ain't shooting
        :param delta_time: To wait a fixed amount of time between shots (depending on the weapon).
        :return bullet_list: List of all the bullets created by the shot.
        """
        bullet_list = []

        if self.weapon == "shotgun":
            if self.shoot_count > 0:
                self.shoot_count -= 1 * delta_time
            elif self.shoot_count <= 0 and not reloading:
                self.shoot_count = 0.75  # time between shots
                for i in range(5):  # amount of simultaneous bullets
                    rnd_angle = math.pi / 225 * randrange(25)  # random "angle" (0º to 30º)
                    angle = self.radians - math.pi / 12 + rnd_angle  # random angle is added (-15º + (0º->30º))
                    bullet = Bullet(self.center_x, self.center_y, 2000, 600, 3, angle)  # speed, max_distance, damage
                    bullet_list.append(bullet)
                arcade.play_sound(self.shotgun_sound)
                # self.shooting = False

        elif self.weapon == "machinegun":
            if self.shoot_count > 0:
                self.shoot_count -= 1 * delta_time
            elif self.shoot_count <= 0 and not reloading:
                self.shoot_count = 0.05  # time between shots
                for i in range(1):  # amount of simultaneous bullets
                    rnd_angle = math.pi / 225 * randrange(25)  # random "angle" (0º to 10º)
                    angle = self.radians - math.pi / 12 + rnd_angle  # random angle is added (-5º + (0º->10º))
                    bullet = Bullet(self.center_x, self.center_y, 2000, 1500, 1, angle)  # speed, max_distance, damage
                    bullet_list.append(bullet)
                arcade.play_sound(self.machinegun_sound)
                self.shooting = False

        else:
            pass

        return bullet_list
