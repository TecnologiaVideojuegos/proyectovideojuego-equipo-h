import arcade


class Physics:
    def __init__(self, player: arcade.Sprite, enemies: arcade.SpriteList, bullets: arcade.SpriteList, walls: arcade.SpriteList):
        self.player = player
        self.enemy_list = enemies
        self.bullet_list = bullets
        self.wall_list = walls

    def append_enemy(self):
        pass
