from src.pcNpc.LivingBeing import LivingBeing


class DEnemy(LivingBeing):
    def __init__(self, position_x: int, position_y: int):
        super().__init__(position_x, position_y, "./resources/sprites/enemies/blueCorpse.png", 1)

    def draw_debug(self):
        self.draw()
        self.draw_hit_box()
