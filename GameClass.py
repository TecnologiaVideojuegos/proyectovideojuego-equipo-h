""" Lab 7 - User Control """

import arcade
import math
from Classes.PC_NPCs import *

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

VIEWPORT_MARGIN_DI = 400
VIEWPORT_MARGIN_AA = 300






class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
        self.set_update_rate(1 / 60)

        self.background = arcade.load_texture("FondoPrueba.png")

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "Sprites/Player/Skins/Shotgun.png", 0.5)
        # Enemigo
        self.enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprites/Enemies/Zombie.png", 1)
        self.bullseye = arcade.Sprite("Sprites/Player/Bullseye.png", 0.5)
        self.laser = [0, 0]
        self.speed = 250
        self.speed_enemies = 125
        self.mov_ud = ""
        self.mov_lr = ""
        self.set_mouse_visible(False)
        self.shot = None




    def setup(self):
        self.shot = arcade.Sound("Sounds/Shotgun.wav")

        # Used in scrolling
        self.view_bottom = 0
        self.view_left = 0       ####################

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        arcade.draw_line(self.player.center_x, self.player.center_y, self.player.center_x + self.laser[0],
                         self.player.center_y + self.laser[1], arcade.color.PUCE_RED, line_width=2)
        self.player.draw()
        self.bullseye.draw()
        # Enemigo
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
        self.player.upd_position(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.update_bullseye()
        self.player.upd_orientation(self.bullseye.center_x, self.bullseye.center_y)
        # Enemigo
        self.enemy.upd_orientation(self.player.center_x, self.player.center_y)
        self.enemy.move_enemy(self.speed_enemies * delta_time, self.player)
        self.enemy.upd_position(SCREEN_WIDTH, SCREEN_HEIGHT)



                            ############################## Hacia abajo

        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN_DI
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN_DI
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN_AA
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN_AA
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)




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
