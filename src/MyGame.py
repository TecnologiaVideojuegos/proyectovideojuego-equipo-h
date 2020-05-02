""" The darkness within """

import arcade
import math
from random import randrange
from src.pcNpc.Player import Player
from src.pcNpc.Enemy import Enemy
from src.menu.Button import Button
from src.mapGeneration.Map import Map
from src.mapGeneration.Room import Room
from src.Physics import Physics


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Game config
        super().__init__(800, 600, "Game name")
        self.set_fullscreen()
        self.screen_width, self.screen_height = self.get_size()
        self.set_update_rate(1 / 60)
        self.state = 0  # 0 - Main menu , 1 - Game , 2 - High Scores , 3 - Game over ...

        # Viewport
        self.view_bottom = 0
        self.view_left = 0
        self.viewport_margin_lr = self.screen_width // 2
        self.viewport_margin_ud = self.screen_height // 2

        # Physics
        self.physics = None

        # Every Sprite, SpriteList or SpriteList container is declared here
        # In game sprites
        self.map = Room(0, 0)
        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        # Menu Sprites
        self.button_list_0 = []
        self.button_list_2 = []
        self.button_list_3 = []

    def setup(self):
        """Sets up the game to be run"""

        # Create the enemies
        for i in range(2):
            enemy = Enemy(randrange(self.width), randrange(self.height))
            self.enemy_list.append(enemy)

        # Setup the map
        self.map.setup_room()
        self.physics = Physics(self.player, self.enemy_list, self.bullet_list, self.map.wall_list)

        # Setup the buttons
        theme = arcade.gui.Theme()
        theme.set_font(24, arcade.color.WHITE)
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        theme.add_button_textures(normal, hover, clicked, locked)
        # Setup main menu buttons (state 0)
        button = Button(self.screen_width // 2, self.screen_height // 2,
                        self.screen_width // 10, self.screen_height // 10,
                        "Nueva partida", theme)
        self.button_list_0.append(button)

    def on_draw(self):
        arcade.start_render()

        if self.state == 0:
            arcade.set_background_color(arcade.color.BLACK)
            for button in self.button_list_0:
                assert (isinstance(button, arcade.gui.TextButton))
                button.draw()

        elif self.state == 1:
            # Map
            self.map.draw()

            # Player
            self.player.draw()

            # Enemy
            self.enemy_list.draw()

            # Bullet
            self.bullet_list.draw()
        elif self.state == 2:
            pass
        else:
            pass

    def on_update(self, delta_time: float):
        """
        Here goes the game logic

        :param delta_time: The time that passed since the last frame was updated
        """
        if self.state == 0:
            if self.button_list_0[0].pressed:
                self.state = 1
                self.set_mouse_visible(False)

        elif self.state == 1:
            # Update enemy speed
            for enemy in self.enemy_list:
                assert (isinstance(enemy, Enemy))
                enemy.go_to(self.player.center_x, self.player.center_y, delta_time)

            # Update player speed and orientation
            self.player.upd_orientation()
            self.player.speed_up(delta_time)

            # Update bullseye position
            self.player.bullseye_pos(self.view_bottom, self.view_left)

            # Move everything and resolve collisions
            hit_list = self.physics.update()

            # Adjusting viewport
            self.fix_viewport()
        elif self.state == 2:
            pass
        else:
            pass

    def fix_viewport(self):
        changed = False

        # Scroll left
        if self.view_left <= 0:
            left_boundary = 0
        else:
            left_boundary = self.view_left + self.viewport_margin_lr
        if self.player.center_x < left_boundary:
            self.view_left -= left_boundary - self.player.center_x
            changed = True

        # Scroll right
        if self.view_left + self.screen_width >= 7040:
            right_boundary = 7040
        else:
            right_boundary = self.view_left + self.screen_width - self.viewport_margin_lr
        if self.player.center_x > right_boundary:
            self.view_left += self.player.center_x - right_boundary
            changed = True

        # Scroll up
        if self.view_bottom + self.screen_height >= 7040:
            top_boundary = 7040
        else:
            top_boundary = self.view_bottom + self.screen_height - self.viewport_margin_ud
        if self.player.center_y > top_boundary:
            self.view_bottom += self.player.center_y - top_boundary
            changed = True

        # Scroll down
        if self.view_bottom <= 0:
            bottom_boundary = 0
        else:
            bottom_boundary = self.view_bottom + self.viewport_margin_ud
        if self.player.center_y < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.center_y
            changed = True

        if changed:
            # self.on_mouse_motion(self.player.mouse_position[0], self.player.mouse_position[1], 0, 0)
            arcade.set_viewport(self.view_left, self.screen_width + self.view_left,
                                self.view_bottom, self.screen_height + self.view_bottom)

    def on_key_press(self, symbol: int, modifiers: int):
        if self.state == 0:
            pass
        elif self.state == 1:
            if symbol == arcade.key.W:
                self.player.mov_ud = "up"
            elif symbol == arcade.key.A:
                self.player.mov_lr = "left"
            elif symbol == arcade.key.S:
                self.player.mov_ud = "down"
            elif symbol == arcade.key.D:
                self.player.mov_lr = "right"
        elif self.state == 2:
            pass
        elif self.state == 3:
            pass

    def on_key_release(self, symbol: int, modifiers: int):
        if self.state == 0:
            pass
        elif self.state == 1:
            if symbol == arcade.key.W and self.player.mov_ud == "up":  # and self.player.mov_ud == "up"
                self.player.mov_ud = ""
            elif symbol == arcade.key.A and self.player.mov_lr == "left":  # and self.player.mov_lr == "left"
                self.player.mov_lr = ""
            elif symbol == arcade.key.S and self.player.mov_ud == "down":  # and self.player.mov_ud == "down"
                self.player.mov_ud = ""
            elif symbol == arcade.key.D and self.player.mov_lr == "right":  # and self.player.mov_lr == "right"
                self.player.mov_lr = ""
        elif self.state == 2:
            pass
        elif self.state == 3:
            pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.player.mouse_position = [x, y]

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.state == 0:
            for button in self.button_list_0:
                assert (isinstance(button, arcade.gui.TextButton))
                button.check_mouse_press(x, y)
        elif self.state == 1:
            if button == arcade.MOUSE_BUTTON_LEFT and self.player.weapon == "shotgun":
                arcade.play_sound(self.player.shotgun_sound)
        elif self.state == 2:
            pass
        elif self.state == 3:
            pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.state == 0:
            for button in self.button_list_0:
                assert (isinstance(button, arcade.gui.TextButton))
                button.check_mouse_release(x, y)
        elif self.state == 1:
            pass
        elif self.state == 2:
            pass
        elif self.state == 3:
            pass
