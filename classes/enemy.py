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

    def update(self, player, camera, tile_map, world_size):



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

                self.move(directional_vector, tile_map)    

            
        # passive behavior
        elif positional_vector.distance_to(spawnpoint_vector) > 5:
            directional_vector = spawnpoint_vector - positional_vector
            if directional_vector.length() != 0:
                directional_vector = directional_vector.normalize() * self.speed

                self.move(directional_vector, tile_map)
    
        elif positional_vector.distance_to(spawnpoint_vector) > 5:
            print(f"Passive: distance to spawn: {positional_vector.distance_to(spawnpoint_vector)}")
  

        self.rect.centerx = max(0, min(self.rect.centerx, world_size - self.size[0] / 2))
        self.rect.centery = max(0, min(self.rect.centery, world_size - self.size[0] / 2))


        # print(f"Enemy pos: {self.rect.centerx}, {self.rect.centery}")
        # print(f"Spawn pos: {self.x}, {self.y}")
        # print(f"Player pos: {player.rect.centerx}, {player.rect.centery}")
        # print(f"Distance to player: {positional_vector.distance_to(player_vector)}")
        # print(f"Distance to spawn: {positional_vector.distance_to(spawnpoint_vector)}")

    # dealing damage
    #

    def take_damage(self, amount, xp_sprite_list):
        self.health -= amount

        if self.health <= 0:
            xp = XP("images\\XPOrb.png", self.rect.centerx, self.rect.centery)
            xp_sprite_list.add(xp)
            self.kill()

    def deal_damage(self, player):
        if pygame.time.get_ticks() - self.last_attack > self.attack_speed:
            print(f"Dealing {self.damage} damage, player health: {player.health}")
            player.take_damage(self.damage)
            self.last_attack = pygame.time.get_ticks()

    def move(self, directional_vector, tile_map):
        prev_x = self.rect.centerx
        prev_y = self.rect.centery

        if directional_vector.length() > 0:
            normalized_direction = directional_vector.normalize()

            # X separat
            self.rect.centerx += normalized_direction.x * self.speed
            tile_x = self.rect.centerx // 32
            tile_y = self.rect.centery // 32
            if tile_map[tile_y][tile_x] == "wall":
                self.rect.centerx = prev_x

            # Y separat
            self.rect.centery += normalized_direction.y * self.speed
            tile_x = self.rect.centerx // 32
            tile_y = self.rect.centery // 32
            if tile_map[tile_y][tile_x] == "wall":
                self.rect.centery = prev_y
    
       