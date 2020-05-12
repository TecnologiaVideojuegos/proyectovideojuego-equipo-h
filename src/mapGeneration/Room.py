import arcade
from random import randrange


class Room:
    def __init__(self, x, y):
        """Creates a collection of sprites positioned respect to the point (x, y) in the bottom left of the room"""
        self.room_x = x
        self.room_y = y
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()

    @staticmethod
    def random_wall():
        rnd_wall = randrange(2)
        rnd_rotation = randrange(4)
        wall = None
        if rnd_wall == 0:
            wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
        elif rnd_wall == 1:
            wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile2.png", 1)
        wall.angle = rnd_rotation * 90
        return wall

    @staticmethod
    def random_floor():
        rnd_tile = randrange(2)
        rnd_rotation = randrange(4)
        tile = None
        if rnd_tile == 0:
            tile = arcade.Sprite("./resources/sprites/groundTiles/steelGround1.png", 1)
        elif rnd_tile == 1:
            tile = arcade.Sprite("./resources/sprites/groundTiles/steelGround2.png", 1)
        tile.angle = rnd_rotation * 90
        return tile

    def setup_room(self):
        """
        Sets up the ground tiles and the basic walls of a room to be used by the game

        :return:
        """
        # Fill the floor
        for x in range(self.room_x + 96, self.room_x + 7040 - 32, 64):
            for y in range(self.room_y + 96, self.room_y + 7040 - 32, 64):
                tile = self.random_floor()
                tile.center_x = x
                tile.center_y = y
                self.floor_list.append(tile)

        # Fill bottom walls
        for x in range(self.room_x + 32, self.room_x + 7040 + 32, 64):
            wall = self.random_wall()
            wall.center_x = x
            wall.center_y = self.room_y + 32
            self.wall_list.append(wall)

        # Fill left walls
        for y in range(self.room_x + 32, self.room_x + 7040 + 32, 64):
            wall = self.random_wall()
            wall.center_x = self.room_x + 32
            wall.center_y = y
            self.wall_list.append(wall)

        # Fill top walls
        for x in range(self.room_x + 32, self.room_x + 7040 + 32, 64):
            wall = self.random_wall()
            wall.center_x = x
            wall.center_y = self.room_y + 7040 - 32
            self.wall_list.append(wall)

        # Fill right walls
        for y in range(self.room_x + 32, self.room_x + 7040 + 32, 64):
            wall = self.random_wall()
            wall.center_x = self.room_y + 7040 - 32
            wall.center_y = y
            self.wall_list.append(wall)

        for x in range(self.room_x + 96, self.room_x + 7040 - 32, 64):
            for y in range(self.room_y + 96, self.room_y + 7040 - 32, 64):
                rnd = randrange(100)
                if rnd < 7:
                    if not (704 < x < 832 and 319 < y < 513):
                        wall = self.random_wall()
                        wall.center_x = x
                        wall.center_y = y
                        self.wall_list.append(wall)

    def draw(self):
        self.floor_list.draw()
        self.wall_list.draw()
