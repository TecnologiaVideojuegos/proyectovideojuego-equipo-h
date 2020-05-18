import math
from src.pcNpc.LivingBeing import LivingBeing


class Enemy(LivingBeing):
    def __init__(self, position_x: int, position_y: int, image: str = "./resources/sprites/enemies/blueZombie.png", health: int = 1):
        super().__init__(position_x, position_y, image, 1)
        self.health = health
        self.image = image

    def go_to(self, x, y):
        dx = self.center_x - x
        dy = self.center_y - y
        d = math.sqrt(dx ** 2 + dy ** 2)
        if d == 0:
            d = 0.0001
        self.change_x = -self.speed / d * dx
        self.change_y = -self.speed / d * dy

    def draw_debug(self):
        self.draw()
        self.draw_hit_box()