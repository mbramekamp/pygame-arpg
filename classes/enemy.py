import pygame

from classes.xp import XP


class Enemy(pygame.sprite.Sprite):
    damage: int
    health: int
    speed: float
    size: tuple
    attack_speed: int
    last_attack: int
    x: int
    y: int

    def __init__(self, image, x, y):
        super().__init__()

        self.damage = 5
        self.health = 25
        self.speed = 3.4
        self.size = (50, 50)
        self.attack_speed = 300
        self.last_attack = 0
        self.x = x
        self.y = y

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player):
        positional_vector = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        spawnpoint_vector = pygame.math.Vector2(self.x, self.y)
        player_vector = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
        # aggro behavior
        if positional_vector.distance_to(player_vector) < 500:
            directional_vector = player_vector - positional_vector
            if directional_vector.length() < 50:
                self.deal_damage(player)
            else:
                directional_vector = directional_vector.normalize() * (self.speed + 2)

                self.rect.centerx += directional_vector.x
                self.rect.centery += directional_vector.y
        # passive behavior
        elif positional_vector.distance_to(spawnpoint_vector) > 5:
            directional_vector = positional_vector - spawnpoint_vector
            if directional_vector.length() != 0:
                directional_vector = directional_vector.normalize() * self.speed

                self.rect.centerx += directional_vector.x
                self.rect.centery += directional_vector.y

    # dealing damage
    #

    def take_damage(self, amount, xp_sprite_list):
        self.health -= amount

        if self.health <= 0:
            xp = XP("test.png", self.rect.centerx, self.rect.centery)
            xp_sprite_list.add(xp)
            self.kill()

    def deal_damage(self, player):
        if pygame.time.get_ticks() - self.last_attack > self.attack_speed:
            player.take_damage(self.damage)
            self.last_attack = pygame.time.get_ticks()
