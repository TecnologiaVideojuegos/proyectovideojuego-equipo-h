from arcade import *
from src.pcNpc.LivingBeing import LivingBeing
from src.pcNpc.Player import Player
from src.pcNpc.Enemy import Enemy


class Physics:
    def __init__(self, player: Sprite, enemies: SpriteList, bullets: SpriteList, walls: SpriteList):
        """
        Create a physics engine with a shooting player and some enemies.

        :param player: The player sprite.
        :param enemies: The enemies sprites.
        :param bullets: The bullet sprites for the player to kill the enemies.
        :param walls: The sprites neither the player nor the enemies nor the bullets can move through.
        """
        self.player = player
        self.enemies = enemies
        self.bullets = bullets
        self.walls = walls

    def append_enemy(self, enemies):
        """
        Add enemies to the list of enemies considered by the physics.

        :param enemies: It can be either a Sprite or a SpriteList to give the user more flexibility.
        :raises: Only if the type of enemies is wrong.
        """

        # if enemies is a Sprite
        if isinstance(enemies, Sprite):
            self.enemies.append(enemies)

        # or if enemies is a SpriteList
        elif isinstance(enemies, SpriteList):
            for enemy in enemies:
                self.enemies.append(enemy)

        # or if enemies is none of them
        else:
            raise Exception("enemies is neither a Sprite nor a SpriteList")

    def append_bullet(self, bullets):
        """
        Add bullets to the list of bullets considered by the physics.

        :param bullets: It can be either a Sprite or a SpriteList to give the user more flexibility.
        :raises: Only if the type of bullets is wrong.
        """

        # if bullets is a Sprite
        if isinstance(bullets, Sprite):
            self.bullets.append(bullets)

        # or if bullets is a SpriteList
        elif isinstance(bullets, SpriteList):
            for bullet in bullets:
                self.bullets.append(bullet)

        # or if bullets is none of them
        else:
            raise Exception("bullets is neither a Sprite nor a SpriteList")

    def update(self):
        """
        Move everything and resolve collisions.

        This procedure rotates all enemies towards the player. It doesn't handle the player rotation

        :returns: SpriteList with all enemies contacted by bullets. Empty list if no sprites. The first Sprite will be
            the player in case it is contacted by an enemy.
        """

        complete_hit_list = []

        # Rotate
        for enemy in self.enemies:
            assert(isinstance(enemy, LivingBeing))
            enemy.upd_orientation(self.player.center_x, self.player.center_y)

        # Player
        # --- Move in the x direction
        self.player.center_x += self.player.change_x

        # Check for wall hit
        hit_list_x = check_for_collision_with_list(self.player, self.walls)

        # If we hit a wall, move so the edges are at the same point
        if len(hit_list_x) > 0:
            self.player.center_x -= 2*self.player.change_x

        # --- Move in the y direction
        self.player.center_y += self.player.change_y

        # Check for wall hit
        hit_list_y = check_for_collision_with_list(self.player, self.walls)

        # If we hit a wall, move so the edges are at the same point
        if len(hit_list_y) > 0:
            self.player.center_y -= 2*self.player.change_y

        # Enemies
        for enemy in self.enemies:
            # --- Move in the x direction
            enemy.center_x += enemy.change_x

            # Check for wall or enemy hit
            hit_list_x = check_for_collision_with_list(enemy, self.walls)
            hit_list_x += check_for_collision_with_list(enemy, self.enemies)

            # If we hit a wall or enemy, move away
            if len(hit_list_x) > 0:
                enemy.center_x -= enemy.change_x

            # --- Move in the y direction
            enemy.center_y += enemy.change_y

            # Check for wall or enemy hit
            hit_list_y = check_for_collision_with_list(enemy, self.walls)
            hit_list_y += check_for_collision_with_list(enemy, self.enemies)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list_y) > 0:
                enemy.center_y -= enemy.change_y

        # Bullets
        for bullet in self.bullets:
            # --- Move in the x direction
            bullet.center_x += bullet.change_x

            # --- Move in the y direction
            bullet.center_y += bullet.change_y

            # Check enemies hit
            hit_list = check_for_collision_with_list(bullet, self.enemies)
            for sprite in complete_hit_list:
                sprite.remove_from_sprite_lists()
                if sprite not in complete_hit_list:
                    complete_hit_list.append(sprite)

            # Check for wall hit
            hit_list = check_for_collision_with_list(bullet, self.walls)

            # If we hit a wall, delete the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

        # Check damage on player
        if len(check_for_collision_with_list(self.player, self.enemies)) > 0:
            complete_hit_list.append(self.player)

        return complete_hit_list
