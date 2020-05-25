from arcade import *
from src.pcNpc.LivingBeing import LivingBeing
from src.pcNpc.Bullet import Bullet
from src.pcNpc.Player import Player
from src.pcNpc.Enemy import Enemy


class Physics:
    def __init__(self, player: Player, enemies: SpriteList, bullets: SpriteList, walls: SpriteList):
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

        # or if bullets is a list
        elif isinstance(enemies, list):
            for bullet in enemies:
                self.bullets.append(bullet)

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

        # or if bullets is a list
        elif isinstance(bullets, list):
            for bullet in bullets:
                self.bullets.append(bullet)

        # or if bullets is none of them
        else:
            raise Exception("bullets is neither a Sprite nor a SpriteList")

    def update(self, delta_time):
        """
        Moves everything, resolves and handles collisions.

        Although this procedure rotates all enemies towards the player, it doesn't handle the player rotation.

        :returns: SpriteList with all enemies killed by bullets. Empty list if no sprites.
        """

        complete_hit_list = []

        # Rotate
        for enemy in self.enemies:
            assert(isinstance(enemy, LivingBeing))
            enemy.upd_orientation(self.player.center_x, self.player.center_y)

        # Player
        # --- Move in the x direction
        self.player.center_x += self.player.change_x * delta_time

        # Check for wall hit
        hit_list_x = check_for_collision_with_list(self.player, self.walls)

        # If we hit a wall, move so the edges are at the same point
        if len(hit_list_x) > 0:
            self.player.center_x -= self.player.change_x * delta_time

        # --- Move in the y direction
        self.player.center_y += self.player.change_y * delta_time

        # Check for wall hit
        hit_list_y = check_for_collision_with_list(self.player, self.walls)

        # If we hit a wall, move so the edges are at the same point
        if len(hit_list_y) > 0:
            self.player.center_y -= self.player.change_y * delta_time

        # Enemies
        for enemy in self.enemies:
            # --- Move in the x direction
            enemy.center_x += enemy.change_x * delta_time

            # Check for wall or enemy hit
            hit_list_x = check_for_collision_with_list(enemy, self.walls)
            hit_list_x += check_for_collision_with_list(enemy, self.enemies)

            # If we hit a wall or enemy, move away
            if len(hit_list_x) > 0:
                enemy.center_x -= enemy.change_x * delta_time

            # --- Move in the y direction
            enemy.center_y += enemy.change_y * delta_time

            # Check for wall or enemy hit
            hit_list_y = check_for_collision_with_list(enemy, self.walls)
            hit_list_y += check_for_collision_with_list(enemy, self.enemies)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list_y) > 0:
                enemy.center_y -= enemy.change_y * delta_time

        # Bullets
        for bullet in self.bullets:
            assert(isinstance(bullet, Bullet))
            # --- Move in the x direction
            bullet.center_x += bullet.change_x * delta_time

            # --- Move in the y direction
            bullet.center_y += bullet.change_y * delta_time

            # Ensure the bullet doesn't move further than it's maximum travel distance
            bullet.travel_distance -= bullet.speed * delta_time
            if bullet.travel_distance <= 0:
                bullet.remove_from_sprite_lists()

            # Check enemies hit
            hit_list = check_for_collision_with_list(bullet, self.enemies)
            for enemy_ in hit_list:
                assert(isinstance(enemy_, LivingBeing))
                enemy_.damage(bullet.damage)
                if enemy_ not in complete_hit_list and not enemy_.alive:
                    enemy_.remove_from_sprite_lists()
                    complete_hit_list.append(enemy_)

            # Check for wall hit
            hit_list = check_for_collision_with_list(bullet, self.walls)

            # If we hit a wall, delete the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

        # Check damage on player
        enemy_attacks = check_for_collision_with_list(self.player, self.enemies)
        if len(enemy_attacks) > 0:
            self.player.damage(1)
            for enemy__ in enemy_attacks:
                if isinstance(enemy__, Enemy):
                    enemy__.center_x -= enemy__.change_x * delta_time
                    enemy__.center_y -= enemy__.change_y * delta_time

        return complete_hit_list
