""" Lab 7 - User Control """

import arcade
import math
from Classes.PC_NPCs import Player
from Classes.Maps import Room
from Classes.PC_NPCs import *

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
        self.set_update_rate(1 / 60)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "Sprites/Player/Skins/Shotgun.png", 1)
        self.bullseye = arcade.Sprite("Sprites/Player/Bullseye.png", 0.75)
        self.laser = [0, 0]
        self.speed = 500
        #Enemigo
        self.enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprites/Enemies/Zombie.png", 1)
        self.speed_enemies = 125
        self.mov_ud = ""
        self.mov_lr = ""
        self.set_mouse_visible(False)
        self.shot = None
        self.physics = None
        self.map = Room(0, 0)

    def setup(self):
        self.shot = arcade.Sound("Sounds/Shotgun.wav")
        self.map.setup_room(True, True, True, True)
        self.physics = arcade.PhysicsEngineSimple(self.player, self.map.wall_list)

    def on_draw(self):
        arcade.start_render()
        self.map.draw()
        arcade.draw_line(self.player.center_x, self.player.center_y, self.player.center_x + self.laser[0],
                         self.player.center_y + self.laser[1], arcade.color.PUCE_RED, line_width=2)
        self.player.draw()
        self.bullseye.draw()
        #Enemigo
        self.enemy.draw()

    def update_bullseye(self):
        self.laser = [self.bullseye.center_x - self.player.center_x, self.bullseye.center_y - self.player.center_y]
        laser_len = math.sqrt(self.laser[0] ** 2 + self.laser[1] ** 2)
        self.laser[0] /= laser_len
        self.laser[1] /= laser_len
        self.laser[0] *= math.sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2)
        self.laser[1] *= math.sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2)

    def on_update(self, delta_time: float):
        self.player.speed_up(self.mov_ud, self.mov_lr, self.speed * delta_time)
        self.physics.update()
        self.update_bullseye()
        self.player.upd_orientation(self.bullseye.center_x, self.bullseye.center_y)
        #Enemigo
        self.enemy.upd_orientation(self.player.center_x, self.player.center_y)
        self.enemy.move_enemy(self.speed_enemies * delta_time, self.player)
        self.enemy.upd_position(SCREEN_WIDTH, SCREEN_HEIGHT)

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
        self.bullseye.center_x, self.bullseye.center_y = x, y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.play_sound(self.shot)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
