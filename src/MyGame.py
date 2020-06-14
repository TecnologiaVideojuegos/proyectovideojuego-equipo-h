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
        super().__init__(800, 600, "Ravenous beings")
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
        self.volume = 0.05
        arcade.Sound.play(self.song, self.volume)

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
        self.startGame = []
        self.startGame.append("./resources/wallpaper/0.gif")
        self.startGame.append("./resources/wallpaper/1.gif")
        self.startGame.append("./resources/wallpaper/2.gif")
        self.startGame.append("./resources/wallpaper/3.gif")
        self.startGame.append("./resources/wallpaper/4.gif")
        self.startGame.append("./resources/wallpaper/5.gif")
        self.startGame.append("./resources/wallpaper/6.gif")
        self.startGame.append("./resources/wallpaper/7.gif")
        self.startGame.append("./resources/wallpaper/8.gif")
        self.image = 0
        self.velocity = 0
        self.startTitle = []
        self.startTitle.append("./resources/wallpaper/gameTitle/title00.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title01.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title02.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title03.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title04.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title05.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title06.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title07.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title08.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title09.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title10.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title11.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title12.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title13.png")
        self.startTitle.append("./resources/wallpaper/gameTitle/title14.png")
        self.title = 0
        self.velocityTitle = 0

        # Weapons
        self.texturesWeapon1 = []
        self.texturesWeapon2 = []
        self.texturesWeapon3 = []

        self.texturesWeapon1.append("./resources/sprites/weapons/PistolSquareSelected.png")
        self.texturesWeapon1.append("./resources/sprites/weapons/PistolSquareNonSelected.png")

        self.texturesWeapon2.append("./resources/sprites/weapons/MachinegunSquareSelected.png")
        self.texturesWeapon2.append("./resources/sprites/weapons/MachinegunSquareNonSelected.png")
        self.texturesWeapon2.append("./resources/sprites/weapons/MachinegunSquareLocked.png")

        self.texturesWeapon3.append("./resources/sprites/weapons/ShotgunSquareSelected.png")
        self.texturesWeapon3.append("./resources/sprites/weapons/ShotgunSquareNonSelected.png")
        self.texturesWeapon3.append("./resources/sprites/weapons/ShotgunSquareLocked.png")

        self.unlocksecond = False
        self.unlockthird = False
        self.first = 0
        self.second = 2
        self.third = 2

        # Points and rounds
        self.points = 0
        self.round = 0
        self.newRound = True
        self.numEnemys = 3
        self.numOrangeEnemys = 1
        self.rest = self.numEnemys
        self.mode = 1
        self.deadEnemys = 0

        # Pause
        self.pause_list = []
        self.pause = False

        # EE
        self.contador = 0

        # Wallpapper
        self.endCounter = 0
        self.endBackground = []
        self.endBackground.append("./resources/wallpaper/endGame/0.gif")
        self.endBackground.append("./resources/wallpaper/endGame/1.gif")
        self.endBackground.append("./resources/wallpaper/endGame/2.gif")
        self.endBackground.append("./resources/wallpaper/endGame/3.gif")
        self.endBackground.append("./resources/wallpaper/endGame/4.gif")
        self.endBackground.append("./resources/wallpaper/endGame/5.gif")
        self.endBackground.append("./resources/wallpaper/endGame/6.gif")
        self.endBackground.append("./resources/wallpaper/endGame/7.gif")
        self.endBackground.append("./resources/wallpaper/endGame/8.gif")
        self.endBackground.append("./resources/wallpaper/endGame/9.gif")
        self.endBackground.append("./resources/wallpaper/endGame/10.gif")
        self.endBackground.append("./resources/wallpaper/endGame/11.gif")
        self.endBackground.append("./resources/wallpaper/endGame/12.gif")
        self.endBackground.append("./resources/wallpaper/endGame/13.gif")
        self.endBackground.append("./resources/wallpaper/endGame/14.gif")

        self.endVelocity = 0

    def setup(self):
        """Sets up the game to be run"""

        # Setup the map
        self.map.setup_room()
        self.physics = Physics(self.player, self.enemy_list, self.bullet_list, self.map.wall_list)

        # Setup the buttons
        # Setup main menu buttons (state 0)
        for i in range(2):
            button = Button(self.screen_width // 8, (self.screen_height // 3) - (self.screen_height / 7) * i,
                            self.screen_width // 8, self.screen_height // 8,
                            self.buttonName[i])
            self.button_list_0.append(button)

        # Setup main end game button (state 2)
        button = Button(7 * self.screen_width // 8, (self.screen_height // 4) - i * 125,
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
            # Background
            arcade.set_background_color(arcade.color.BLACK)
            if self.image == 9:
                self.image = 0
            arcade.draw_lrwh_rectangle_textured(0, 0, self.screen_width, self.screen_height,
                                                arcade.load_texture(self.startGame[self.image]))
            self.velocity += 1
            if self.velocity == 13:
                self.image += 1
                self.velocity = 0

            # Title
            if self.title == 15:
                self.title = 0
            arcade.draw_lrwh_rectangle_textured((self.screen_width - 1284) / 2, 11 * self.screen_height // 16, 1284,
                                                192, arcade.load_texture(self.startTitle[self.title]))
            self.velocityTitle += 1
            if self.velocityTitle == 9:
                self.title += 1
                self.velocityTitle = 0

            # Button
            for button in self.button_list_0:
                button.draw()

        elif self.state == 1:
            # Map
            self.map.draw()

            # Enemies
            self.dead_list.draw()
            self.enemy_list.draw()

            # Player
            self.player.draw()

            # Bullets
            self.bullet_list.draw()

            left, right, bottom, top = arcade.get_viewport()

            # Weapons
            arcade.draw_lrwh_rectangle_textured(left + self.screen_width / 16, bottom + self.screen_height / 12, 60,
                                                60, arcade.load_texture(self.texturesWeapon1[self.first]))
            arcade.draw_lrwh_rectangle_textured(left + 2 * self.screen_width / 16, bottom + self.screen_height / 12, 60,
                                                60, arcade.load_texture(self.texturesWeapon2[self.second]))
            arcade.draw_lrwh_rectangle_textured(left + 3 * self.screen_width / 16, bottom + self.screen_height / 12, 60,
                                                60, arcade.load_texture(self.texturesWeapon3[self.third]))

            if self.round >= 5 and not self.unlocksecond:
                self.unlocksecond = True
                self.second = 1

            if self.round >= 10 and not self.unlockthird:
                self.unlockthird = True
                self.third = 1

            # Pause
            if self.pause:
                # Pause button
                if len(self.pause_list) == 0:
                    if bottom + 800 > 7040:
                        bottom = 6340
                    pause_button = Button(self.screen_width // 10 + left, 7 * self.screen_height // 8 + bottom, self.screen_width // 8, self.screen_height // 8,
                                          "Exit game")
                    self.pause_list.append(pause_button)

                for button in self.pause_list:
                    if isinstance(button, Button):
                        button.draw()

            else:
                arcade.draw_text("Score: " + str(self.points), left + self.screen_width / 12,
                                 top - self.screen_height / 14, arcade.color.WHITE, 40)
                arcade.draw_text("Round: " + str(self.round), left + self.screen_width / 3,
                                 top - self.screen_height / 14, arcade.color.WHITE, 40)
                arcade.draw_text("Remaining: " + str(self.rest), left + self.screen_width / 2,
                                 top - self.screen_height / 14, arcade.color.WHITE, 40)

        elif self.state == 2:
            left, right, bottom, top = arcade.get_viewport()

            if self.endCounter == 14:
                self.endCounter = 0

            arcade.draw_lrwh_rectangle_textured(0, 0, self.screen_width, self.screen_height,
                                                arcade.load_texture(self.endBackground[self.endCounter]))
            self.endVelocity += 1
            if self.endVelocity == 13:
                self.endCounter += 1
                self.endVelocity = 0

            for button in self.button_list_1:
                button.draw()

            arcade.draw_text("Defeated enemies: " + str(self.deadEnemys), self.screen_width // 10 + left, 13 * self.screen_height // 15 + bottom, arcade.color.WHITE,
                             40)
            arcade.draw_text("Rounds: " + str(self.round - 1), self.screen_width // 10 + left, 12 * self.screen_height // 15 + bottom, arcade.color.WHITE, 40)
            arcade.draw_text("Score: " + str(self.points), self.screen_width // 10 + left, 11 * self.screen_height // 15 + bottom, arcade.color.WHITE, 40)

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
            self.position = self.song.get_stream_position()
            if self.position == 0.0:
                arcade.Sound.play(self.song, self.volume)

            if not self.pause:
                self.set_mouse_visible(False)

                # Rounds
                if len(self.enemy_list) == 0:
                    self.newRound = True
                    self.round += 1

                    if (self.round == 5):
                        self.mode = 2

                # Summon new enemies
                if self.newRound:
                    for i in range(self.numEnemys):
                        run = True
                        enemy = Enemy(randrange(1, 109) * 64 + 32, randrange(1, 109) * 64 + 32, 0)
                        while run:
                            if self.player.center_x - self.width <= enemy.center_x <= self.player.center_x + self.width and self.player.center_y - self.height <= enemy.center_y <= self.player.center_y + self.height:
                                enemy = Enemy(randrange(1, 109) * 64 + 32, randrange(1, 109) * 64 + 32, 0)
                                continue
                            run = False
                            for wall in self.map.wall_list:
                                if enemy.center_x == wall.center_x and enemy.center_y == wall.center_y:
                                    enemy = Enemy(randrange(1, 109) * 64 + 32, randrange(1, 109) * 64 + 32, 0)
                                    run = True
                                    break
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

                # Generate bullets
                if self.player.shooting:
                    # If the player is trying to shoot resolve the action
                    new_bullet_list = self.player.shoot(delta_time, reloading=False)
                    self.physics.append_bullet(new_bullet_list)
                else:
                    # If the player isn't shooting reload the weapon
                    self.player.shoot(delta_time, reloading=True)

                # Update enemy speed
                for enemy in self.enemy_list:
                    assert (isinstance(enemy, Enemy))
                    enemy.go_to(self.player.center_x, self.player.center_y)

                # Update player speed and orientation
                self.player.update_animation()
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
                self.first = 0
                if self.unlocksecond:
                    self.second = 1
                if self.unlockthird:
                    self.third = 1

                self.player.texture = arcade.load_texture(self.player.textures[0])
                self.player.weapon = "Akimbo"
                self.player.change_animation()

            if symbol == arcade.key.KEY_2:
                if self.unlocksecond:
                    self.first = 1
                    self.second = 0

                    self.player.texture = arcade.load_texture(self.player.textures[1])
                    self.player.weapon = "Machinegun"
                    self.player.change_animation()

                if self.unlockthird:
                    self.third = 1

            if symbol == arcade.key.KEY_3:
                if self.unlockthird:
                    self.first = 1
                    self.second = 1
                    self.third = 0

                    self.player.texture = arcade.load_texture(self.player.textures[1])
                    self.player.weapon = "Shotgun"
                    self.player.change_animation()

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
            left, right, bottom, top = arcade.get_viewport()

            if button == arcade.MOUSE_BUTTON_LEFT:
                self.player.shooting = True

            for button2 in self.pause_list:
                if isinstance(button2, Button):
                    button2.check_mouse_press(x + left, y + bottom)

            # Easter egg
            if self.pause:
                if (self.player.check_mouse_press(x + left, y + bottom)):
                    self.contador += 1
                    if self.contador == 15:
                        self.song.stop()
                        self.song = arcade.Sound("./resources/music/song2.wav")
                        self.volume = 0.01
                        arcade.Sound.play(self.song, self.volume)

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
