""" The darkness within """

import arcade
import math
# import gtk
from random import randrange
from src.pcNpc.Player import Player
from src.pcNpc.Enemy import Enemy
from src.mapGeneration.Map import Map
from src.mapGeneration.Room import Room
from src.Physics import Physics


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Game config
        self.set_update_rate(1 / 60)
        self.set_mouse_visible(False)
        self.width = 800
        self.height = 600
        # width = gtk.gdk.screen_width()
        # height = gtk.gdk.screen_height()
        super().__init__(self.width, self.height, "Game name")
        self.set_fullscreen()

        # Viewport
        self.view_bottom = 0
        self.view_left = 0
        self.viewport_margin_di = self.width // 2
        self.viewport_margin_aa = self.height // 2

        # Physics
        self.physics = None

        # Every Sprite, SpriteList or SpriteList container is declared here
        self.map = Room(0, 0)
        self.player = Player(self.width // 2, self.height // 2)
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

    def setup(self):
        self.enemy_list = arcade.SpriteList()

        for i in range(2):
            enemy = Enemy(randrange(self.width), randrange(self.height))
            self.enemy_list.append(enemy)

        self.map.setup_room(True, True, True, True)
        self.physics = Physics(self.player, self.enemy_list, self.bullet_list, self.map.wall_list)

    def on_draw(self):
        arcade.start_render()

        # Map
        self.map.draw()

        # Player
        self.player.draw()

        # Enemy
        self.enemy_list.draw()

        # Bullet
        self.bullet_list.draw()

    def fix_viewport(self):
        changed = False

        # Scroll left
        left_boundary = self.view_left + self.viewport_margin_di
        if self.player.center_x < left_boundary:
            self.view_left -= left_boundary - self.player.center_x
            changed = True

        # Scroll right
        right_boundary = self.view_left + self.width - self.viewport_margin_di
        if self.player.center_x > right_boundary:
            self.view_left += self.player.center_x - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + self.height - self.viewport_margin_aa
        if self.player.center_y > top_boundary:
            self.view_bottom += self.player.center_y - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + self.viewport_margin_aa
        if self.player.center_y < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.center_y
            changed = True

        if changed:
            self.on_mouse_motion(self.player.mouse_position[0], self.player.mouse_position[1], 0, 0)
            arcade.set_viewport(self.view_left, self.width + self.view_left,
                                self.view_bottom, self.height + self.view_bottom)

    def on_update(self, delta_time: float):
        """Here goes the game logic

        :param delta_time: The time that passed since the last frame was updated
        """
        # Update enemy speed
        for enemy in self.enemy_list:
            assert(isinstance(enemy, Enemy))
            enemy.go_to(self.player.center_x, self.player.center_y, delta_time)

        # Update player speed and orientation
        self.player.upd_orientation()
        self.player.speed_up(self.player.mov_ud, self.player.mov_lr, delta_time * self.player.speed)

        # Update bullseye position
        self.player.bullseye_pos(self.view_bottom, self.view_left)

        # Move everything and resolve collisions
        hit_list = self.physics.update()

        # Adjusting viewport
        self.fix_viewport()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.player.mov_ud = "up"
        elif symbol == arcade.key.A:
            self.player.mov_lr = "left"
        elif symbol == arcade.key.S:
            self.player.mov_ud = "down"
        elif symbol == arcade.key.D:
            self.player.mov_lr = "right"

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W and self.player.mov_ud == "up":
            self.player.mov_ud = ""
            self.player.full_stop("y")
        elif symbol == arcade.key.S and self.player.mov_ud == "down":
            self.player.mov_ud = ""
            self.player.full_stop("y")
        elif symbol == arcade.key.A and self.player.mov_lr == "left":
            self.player.mov_lr = ""
            self.player.full_stop("x")
        elif symbol == arcade.key.D and self.player.mov_lr == "right":
            self.player.mov_lr = ""
            self.player.full_stop("x")

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.player.mouse_position = [x, y]

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT and self.player.weapon == "shotgun":
            arcade.play_sound(self.player.shotgun_sound)
