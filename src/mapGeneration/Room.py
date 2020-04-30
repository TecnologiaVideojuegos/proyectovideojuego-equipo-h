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
                tile = arcade.Sprite("./resources/sprites/groundTiles/steelGround1.png", 1)
                tile.center_x = x
                tile.center_y = y
                self.floor_list.append(tile)

        # Filling in the basic walls
        if down:
            for x in range(self.room_x + 32, self.room_x + 608, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 32
                self.wall_list.append(wall)

            for x in range(self.room_x + 736, self.room_x + 1312, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 32
                self.wall_list.append(wall)
        else:
            for x in range(self.room_x + 32, self.room_x + 1312, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 32
                self.wall_list.append(wall)

        if up:
            for x in range(self.room_x + 32, self.room_x + 608, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 1312
                self.wall_list.append(wall)

            for x in range(self.room_x + 736, self.room_x + 1312, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 1312
                self.wall_list.append(wall)
        else:
            for x in range(self.room_x + 32, self.room_x + 1312, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = x
                wall.center_y = self.room_y + 1376
                self.wall_list.append(wall)

        if left:
            for y in range(self.room_y + 32, self.room_y + 608, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = self.room_x + 32
                wall.center_y = y
                self.wall_list.append(wall)

            for y in range(self.room_y + 736, self.room_y + 1312, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = self.room_x + 32
                wall.center_y = y
                self.wall_list.append(wall)
        else:
            for y in range(self.room_y + 32, self.room_y + 1312, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = self.room_x + 32
                wall.center_y = y
                self.wall_list.append(wall)

        if right:
            for y in range(self.room_y + 32, self.room_y + 608, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = self.room_x + 1312
                wall.center_y = y
                self.wall_list.append(wall)

            for y in range(self.room_y + 736, self.room_y + 1376, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = self.room_x + 1312
                wall.center_y = y
                self.wall_list.append(wall)
        else:
            for y in range(self.room_y + 32, self.room_y + 1312, 64):
                wall = arcade.Sprite("./resources/sprites/groundTiles/cyberGroundTile1.png", 1)
                wall.center_x = self.room_x + 1312
                wall.center_y = y
                self.wall_list.append(wall)

    def draw(self):
        self.floor_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
