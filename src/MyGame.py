""" The darkness within """

import arcade
from random import randrange
from src.pcNpc.Player import Player
from src.pcNpc.Enemy import Enemy
from src.menu.Button import Button
from src.mapGeneration.Room import Room
from src.Physics import Physics, check_for_collision


class MyGame(arcade.Window):
    """Our Custom Window Class"""

    def __init__(self):
        """ Initializer """

        # Game config
        super().__init__(800, 600, "Game name")
        self.set_fullscreen()
        self.screen_width, self.screen_height = self.get_size()
        self.set_update_rate(1 / 60)
        self.state = 0  # 0 - Main menu , 1 - Game , 2 - Game over

        # Viewport
        self.view_bottom = 0
        self.view_left = 0
        self.viewport_margin_lr = self.screen_width // 2
        self.viewport_margin_ud = self.screen_height // 2

        # Physics
        self.physics = None

        # Music
        self.song = arcade.Sound("./resources/music/punish_them.wav")
        self.song_length = 0

        # Every Sprite, SpriteList or SpriteList container is declared here
        # In game sprites
        self.map = Room(0, 0)
        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.enemy_list = arcade.SpriteList()
        self.dead_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Menu Sprites
        self.button_list_0 = []
        self.button_list_1 = []
        self.buttonName = ["New Game", "Quit"]

        # Points and rounds
        self.points = 0
        self.round = 1
        self.newRound = True
        self.numEnemys = 3
        self.numOrangeEnemys = 1
        self.rest = self.numEnemys
        self.mode = 1
        self.deadEnemys = 0

        # Pause
        self.pause_list = []
        self.pause = False

        # Wallpapper
        self.endBackground = None

    def setup(self):
        """Sets up the game to be run"""

        # Setup the map
        arcade.Sound.play(self.song, 0.05)
        self.map.setup_room()
        self.physics = Physics(self.player, self.enemy_list, self.bullet_list, self.map.wall_list)

        # Wallpaper
        self.endBackground = arcade.load_texture("./resources/wallpaper/gameOver.png")

        # Setup the buttons
        # Setup main menu buttons (state 0)
        for i in range(2):
            button = Button(self.screen_width // 2, (self.screen_height // 2) - i * 125,
                            self.screen_width // 8, self.screen_height // 8,
                            self.buttonName[i])
            self.button_list_0.append(button)

        # Setup main end game button (state 2)
        button = Button(3 * self.screen_width // 4, (self.screen_height // 3) - i * 125,
                        self.screen_width // 8, self.screen_height // 8,
                        self.buttonName[1])
        self.button_list_1.append(button)

    def reset_viewport(self):
        if self.view_left != 0 and self.view_bottom != 0:
            self.view_left = 0
            self.view_bottom = 0
            arcade.set_viewport(self.view_left, self.screen_width + self.view_left,
                                self.view_bottom, self.screen_height + self.view_bottom)

    def adjust_viewport(self):
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

    def on_draw(self):
        arcade.start_render()

        if self.state == 0:
            arcade.set_background_color(arcade.color.WHITE)
            for button in self.button_list_0:
                button.draw()

        elif self.state == 1:
            # Map
            self.map.draw()

            # Create the enemies
            if self.newRound:
                for i in range(self.numEnemys):
                    enemy = Enemy(randrange(96, 6944), randrange(96, 6944), 0)
                    self.enemy_list.append(enemy)

                self.newRound = False
                self.rest = self.numEnemys
                self.numEnemys += 2

                if self.mode >= 2:
                    for i in range(self.numOrangeEnemys):
                        enemy = Enemy(randrange(96, 6944), randrange(96, 6944), 1)
                        self.enemy_list.append(enemy)

                    self.rest += self.numOrangeEnemys
                    self.numOrangeEnemys += 1

            # Enemies
            self.dead_list.draw()
            self.enemy_list.draw()

            # Player
            self.player.draw()

            # Bullets
            self.bullet_list.draw()

            left, right, bottom, top = arcade.get_viewport()

            if self.pause:
                # Pause button
                if len(self.pause_list) == 0:
                    if bottom + 800 > 7040:
                        bottom = 6340
                    pause_button = Button(100 + left, 800 + bottom, self.screen_width // 8, self.screen_height // 8,
                                          "Exit game")
                    self.pause_list.append(pause_button)

                for button in self.pause_list:
                    if isinstance(button, Button):
                        button.draw()

            else:
                arcade.draw_text("Score: " + str(self.points), 50 + left, 800 + bottom, arcade.color.WHITE, 40)
                arcade.draw_text("Round: " + str(self.round), 500 + left, 800 + bottom, arcade.color.WHITE, 40)
                arcade.draw_text("Remaining: " + str(self.rest), 800 + left, 800 + bottom, arcade.color.WHITE, 40)

        elif self.state == 2:
            left, right, bottom, top = arcade.get_viewport()
            arcade.draw_lrwh_rectangle_textured(0, 0, self.screen_width, self.screen_height, self.endBackground)

            for button in self.button_list_1:
                button.draw()

            arcade.draw_text("Defeated enemies: " + str(self.deadEnemys), 50 + left, 300 + bottom, arcade.color.WHITE, 40)
            arcade.draw_text("Rounds: " + str(self.round - 1), 50 + left, 240 + bottom, arcade.color.WHITE, 40)
            arcade.draw_text("Score: " + str(self.points), 50 + left, 180 + bottom, arcade.color.WHITE, 40)

        else:
            pass

    def on_update(self, delta_time: float):
        """
        Here goes the game logic

        :param delta_time: The time that passed since the last frame was updated
        """
        if self.state == 0:
            self.reset_viewport()
            if self.button_list_0[0].pressed:
                self.state = 1
            elif self.button_list_0[1].pressed:
                arcade.close_window()

        elif self.state == 1:

            if not self.pause:
                self.set_mouse_visible(False)

                # Rounds
                if len(self.enemy_list) == 0:
                    self.newRound = True
                    self.round += 1

                    if (self.round == 5):
                        self.mode = 2

                # Generate bullets
                if self.player.shooting:
                    # If the player is trying to shoot resolve the action
                    new_bullet_list = self.player.shoot(delta_time, reloading=False)
                    self.physics.append_bullet(new_bullet_list)
                else:
                    # If the player ain't shooting reload the weapon
                    self.player.shoot(delta_time, reloading=True)

                # Update enemy speed
                for enemy in self.enemy_list:
                    assert (isinstance(enemy, Enemy))
                    enemy.go_to(self.player.center_x, self.player.center_y)

                # Update player speed and orientation
                self.player.upd_orientation()
                self.player.speed_up()

                # Update bullseye position
                self.player.bullseye_pos(self.view_left, self.view_bottom)

                # Move everything and resolve collisions
                hit_list = self.physics.update(delta_time)

                for enemy in hit_list:
                    if isinstance(enemy, Enemy):
                        if enemy.type == 0:
                            enemy.texture = arcade.load_texture("./resources/sprites/enemies/blueCorpse.png")
                        elif enemy.type == 1:
                            enemy.texture = arcade.load_texture("./resources/sprites/enemies/orangeCorpse.png")

                        enemy.angle = randrange(360)
                        self.points = self.points + 100 * self.round
                        enemy.remove_from_sprite_lists()
                        self.dead_list.append(enemy)
                        self.rest -= 1
                        self.deadEnemys += 1

                # Adjusting viewport
                self.adjust_viewport()

                # End game
                # Check damage on player
                for enemy in self.enemy_list:
                    enemy_attacks = check_for_collision(self.player, enemy)
                    if enemy_attacks:
                        self.state = 2

            else:
                self.set_mouse_visible(True)
                try:
                    if self.pause_list[0].pressed:
                        arcade.close_window()
                except:
                    pass

        elif self.state == 2:
            self.reset_viewport()
            self.set_mouse_visible(True)
            if self.button_list_1[0].pressed:
                arcade.close_window()

        else:
            pass

    def on_key_press(self, symbol: int, modifiers: int):
        if self.state == 0:
            pass
        elif self.state == 1:
            if symbol == arcade.key.KEY_1:
                self.player.texture = arcade.load_texture(self.player.textures[0])

            if symbol == arcade.key.KEY_2:
                self.player.texture = arcade.load_texture(self.player.textures[1])

            if symbol == arcade.key.ESCAPE:
                if self.pause:
                    self.pause_list.clear()
                    self.pause = False
                else:
                    self.pause = True

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
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.player.shooting = True

            for button2 in self.pause_list:
                if isinstance(button2, Button):
                    left, right, bottom, top = arcade.get_viewport()
                    button2.check_mouse_press(x + left, y + bottom)

        elif self.state == 2:
            for button in self.button_list_1:
                assert (isinstance(button, arcade.gui.TextButton))
                button.check_mouse_press(x, y)
        elif self.state == 3:
            pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.state == 0:
            for button in self.button_list_0:
                assert (isinstance(button, arcade.gui.TextButton))
                button.check_mouse_release(x, y)
        elif self.state == 1:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.player.shooting = False

            for button2 in self.pause_list:
                if isinstance(button2, Button):
                    left, right, bottom, top = arcade.get_viewport()
                    button2.check_mouse_release(x + left, y + bottom)

        elif self.state == 2:
            for button in self.button_list_1:
                assert (isinstance(button, arcade.gui.TextButton))
                button.check_mouse_release(x, y)
        elif self.state == 3:
            pass
