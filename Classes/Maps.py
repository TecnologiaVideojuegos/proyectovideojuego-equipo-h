import arcade
from random import randrange


class Room:
    def __init__(self, x, y):
        """Creates a collection of sprites positioned respect to the point (x, y) in the bottom left of the room"""
        self.room_x = x
        self.room_y = y
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

    def setup_room(self, up: bool, right: bool, left: bool, down: bool):
        """Changes the room procedurally so that it has an entrance wherever the parameters say"""
        # Filling the floor with tiles
        for x in range(self.room_x + 32, self.room_x + 1376, 64):
            for y in range(self.room_y + 32, self.room_y + 1376, 64):
                tile = arcade.Sprite("Sprites/GroundTiles/SteelGround1.png", 1)
                tile.center_x = x
                tile.center_y = y
                self.floor_list.append(tile)

        # Filling in the basic walls
        if down:
            for x in range(self.room_x + 32, self.room_x + 608, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 32
                self.wall_list.append(wall)

            for x in range(self.room_x + 736, self.room_x + 1312, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 32
                self.wall_list.append(wall)
        else:
            for x in range(self.room_x + 32, self.room_x + 1312, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 32
                self.wall_list.append(wall)

        if up:
            for x in range(self.room_x + 32, self.room_x + 608, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 1312
                self.wall_list.append(wall)

            for x in range(self.room_x + 736, self.room_x + 1312, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 1312
                self.wall_list.append(wall)
        else:
            for x in range(self.room_x + 32, self.room_x + 1312, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 1376
                self.wall_list.append(wall)

        if left:
            for y in range(self.room_y + 32, self.room_y + 608, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = self.room_x + 32
                wall.center_y = y
                self.wall_list.append(wall)

            for y in range(self.room_y + 736, self.room_y + 1312, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = self.room_x + 32
                wall.center_y = y
                self.wall_list.append(wall)
        else:
            for y in range(self.room_y + 32, self.room_y + 1312, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = self.room_x + 32
                wall.center_y = y
                self.wall_list.append(wall)

        if right:
            for y in range(self.room_y + 32, self.room_y + 608, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = self.room_x + 1312
                wall.center_y = y
                self.wall_list.append(wall)

            for y in range(self.room_y + 736, self.room_y + 1376, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = self.room_x + 1312
                wall.center_y = y
                self.wall_list.append(wall)
        else:
            for y in range(self.room_y + 32, self.room_y + 1312, 64):
                wall = arcade.Sprite("Sprites/GroundTiles/SteelGround.png", 1)
                wall.center_x = self.room_x + 1312
                wall.center_y = y
                self.wall_list.append(wall)

    def draw(self):
        self.floor_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()


class Map:
    def __init__(self):
        """This is just a class to handle all 25 rooms at the same time"""
        self.main_path = []
        self.rooms = []
        for x in range(0, 5632, 1408):
            for y in range(0, 5632, 1408):
                self.rooms.append(Room(x, y))

    def __update_main_path(self):
        """Clears the main path and creates a new one"""
        # Clearing main path
        self.main_path.clear()

        # Adding first two rooms to the path
        self.main_path.append((randrange(5), 0))
        if self.main_path[0][0] == 0:
            if randrange(2):  # up
                self.main_path.append((0, 1))
            else:  # right
                self.main_path.append((1, 0))
        elif self.main_path[0][0] == 4:
            if randrange(2):  # up
                self.main_path.append((4, 1))
            else:  # left
                self.main_path.append((3, 0))
        else:
            r = randrange(3)
            if r == 0:  # up
                self.main_path.append((self.main_path[0][0], 1))
            elif r == 1:  # left
                self.main_path.append((self.main_path[0][0] - 1, 0))
            else:  # right
                self.main_path.append((self.main_path[0][0] + 1, 0))

        # Creating the rest of the main path
        while self.main_path[-1][1] != 5:
            # Check what happened with last two rooms in the main path
            a = self.main_path[-1]  # Room we're in
            b = self.main_path[-2]  # Room we were in
            c = (a[0] - b[0], a[1] - b[1])  # Last movement we did
            if c[1] == 1:  # We've just moved upwards
                if a[0] == 0:
                    if randrange(2):  # up
                        self.main_path.append((0, a[1] + 1))
                    else:  # right
                        self.main_path.append((1, a[1]))
                elif a[0] == 4:
                    if randrange(2):  # up
                        self.main_path.append((4, a[1] + 1))
                    else:  # left
                        self.main_path.append((3, a[1]))
                else:
                    r = randrange(3)
                    if r == 0:  # up
                        self.main_path.append((a[0], a[1] + 1))
                    elif r == 1:  # left
                        self.main_path.append((a[0] - 1, a[1]))
                    else:  # right
                        self.main_path.append((a[0] + 1, a[1]))
            elif c[0] == 1:  # We've just moved rightwards
                if a[0] == 4:
                    self.main_path.append((4, a[1] + 1))
                else:
                    if randrange(2):  # up
                        self.main_path.append((a[0], a[1] + 1))
                    else:  # right
                        self.main_path.append((a[0] + 1, a[1]))
            else:  # We've just moved leftwards
                if a[0] == 0:
                    self.main_path.append((4, a[1] + 1))
                else:
                    if randrange(2):  # up
                        self.main_path.append((a[0], a[1] + 1))
                    else:  # left
                        self.main_path.append((a[0] - 1, a[1]))
        self.main_path.pop()

    def new_map(self):
        """Creates a new set of rooms, following a new main path"""
        self.__update_main_path()
        # Setting up the rooms
        for x in range(5):
            for y in range(5):
                ri = x+5*y  # Room index
                if y == 0:
                    if x == 0:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), randrange(2), False, False)
                    if x == 4:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), False, randrange(2), False)
                    else:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), randrange(2), randrange(2), False)
                elif y < 4:
                    if x == 0:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), randrange(2), False, randrange(2))
                    if x == 4:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), False, randrange(2), randrange(2))
                    else:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), randrange(2), randrange(2), randrange(2))
                else:
                    if x == 0:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(False, randrange(2), False, randrange(2))
                    if x == 4:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(False, False, randrange(2), randrange(2))
                    else:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(False, randrange(2), randrange(2), randrange(2))
