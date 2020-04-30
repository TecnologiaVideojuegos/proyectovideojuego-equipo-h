""" The darkness within """

import arcade
import math
from src.pcNpc.Player import Player
from src.pcNpc.Enemy import Enemy
from src.mapGeneration.Map import Map
from src.mapGeneration.Room import Room

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
VIEWPORT_MARGIN_DI = 400
VIEWPORT_MARGIN_AA = 300


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Game name")

        self.set_update_rate(1 / 60)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "./resources/sprites/player/shotgun.png", 1)
        self.enemy_list = None
        self.bullseye = arcade.Sprite("./resources/sprites/player/bullseye.png", 0.75)
        self.laser = [0, 0]
        self.speed = 500
        self.speed_enemies = 250
        self.mov_ud = ""
        self.mov_lr = ""
        self.set_mouse_visible(False)
        self.shot = None
        self.player_wall_physics = None
        self.enemy_wall_physics = None
        self.map = Room(0, 0)
        self.view_bottom = 0
        self.view_left = 0
        self.mouse_position = [0, 0]

    def setup(self):
        self.shot = arcade.Sound("./resources/sounds/shotgun.wav")
        self.enemy_list = arcade.SpriteList()

        for i in range(2):
            enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, "./resources/sprites/enemies/alienZombie.png", 1)
            self.enemy_list.append(enemy)

        self.map.setup_room(True, True, True, True)
        self.player_wall_physics = arcade.PhysicsEngineSimple(self.player, self.map.wall_list)
        self.enemy_wall_physics = arcade.PhysicsEngineSimple(self.enemy_list, self.map.wall_list)

    def on_draw(self):
        arcade.start_render()
        self.map.draw()
        arcade.draw_line(self.player.center_x, self.player.center_y, self.player.center_x + self.laser[0],
                         self.player.center_y + self.laser[1], arcade.color.PUCE_RED, line_width=2)
        self.player.draw()
        # self.player.draw_hit_box()
        self.bullseye.draw()
        # Enemigo
        self.enemy_list.draw()

    def update_bullseye(self):
        self.laser = [self.bullseye.center_x - self.player.center_x, self.bullseye.center_y - self.player.center_y]
        laser_len = math.sqrt(self.laser[0] ** 2 + self.laser[1] ** 2)
        self.laser[0] /= laser_len
        self.laser[1] /= laser_len
        self.laser[0] *= math.sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2)
        self.laser[1] *= math.sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2)

    def fix_viewport(self):
        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN_DI
        if self.player.center_x < left_boundary:
            self.view_left -= left_boundary - self.player.center_x
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN_DI
        if self.player.center_x > right_boundary:
            self.view_left += self.player.center_x - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN_AA
        if self.player.center_y > top_boundary:
            self.view_bottom += self.player.center_y - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN_AA
        if self.player.center_y < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.center_y
            changed = True

        if changed:
            self.on_mouse_motion(self.mouse_position[0], self.mouse_position[1], 0, 0)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_update(self, delta_time: float):
        self.update_bullseye()
        self.player.upd_orientation(self.bullseye.center_x, self.bullseye.center_y)
        self.player.speed_up(self.mov_ud, self.mov_lr, delta_time * self.speed)
        self.player_wall_physics.update()
        self.enemy_wall_physics.update()
        for enemy in self.enemy_list:
            enemy.follow_sprite(self.speed_enemies * delta_time, self.player)
            enemy.upd_orientation(self.player.center_x, self.player.center_y)
        self.fix_viewport()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.mov_ud = "up"
        elif symbol == arcade.key.A:
            self.mov_lr = "left"
        elif symbol == arcade.key.S:
            self.mov_ud = "down"
        elif symbol == arcade.key.D:
            self.mov_lr = "right"

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W and self.mov_ud == "up":
            self.mov_ud = ""
            self.player.full_stop("y")
        elif symbol == arcade.key.S and self.mov_ud == "down":
            self.mov_ud = ""
            self.player.full_stop("y")
        elif symbol == arcade.key.A and self.mov_lr == "left":
            self.mov_lr = ""
            self.player.full_stop("x")
        elif symbol == arcade.key.D and self.mov_lr == "right":
            self.mov_lr = ""
            self.player.full_stop("x")

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_position = [x, y]
        self.bullseye.center_x, self.bullseye.center_y = x + self.view_left, y + self.view_bottom

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.play_sound(self.shot)
