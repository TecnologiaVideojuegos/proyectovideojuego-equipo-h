import arcade
import math


class Bullet(arcade.Sprite):
    """Class to handle operations with bullets"""

    def __init__(self, position_x, position_y, speed: int, travel_distance: int, damage: int, radians: float):
        """
        Creates a simple bullet.

        :param position_x: The initial x position of the bullet.
        :param position_y: The initial y position of the bullet.
        :param speed: The speed at which the bullet moves.
        :param travel_distance: The total distance the bullet can travel.
        :param damage: The amount of damage this bullet deals.
        :param radians: The initial rotation of the bullet in radians.
        """

        super().__init__("./resources/sprites/player/bullet.png", 1, center_x=position_x, center_y=position_y)
        self.speed = speed
        self.travel_distance = travel_distance
        self.damage = damage
        self.radians = radians
        self.change_x = math.cos(radians) * self.speed
        self.change_y = math.sin(radians) * self.speed
