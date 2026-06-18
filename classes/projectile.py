import pygame


class Projectile(pygame.sprite.Sprite):
    x: float
    y: float
    size: tuple
    direction: pygame.math.Vector2
    speed: float
    damage: int
    sound: str

    def __init__(self, x, y, direction, speed, damage, image, sound, size):
        super().__init__()

        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.sound = sound
        self.size = size

        self.original_image = pygame.image.load(image)

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, screen, world_size, enemy_sprite_list, xp_sprite_list):
        print(f"Projectile update: x={self.x}, y={self.y}, direction={self.direction}")

        normalized_direction = self.direction.normalize()
        self.x += normalized_direction.x * self.speed
        self.y += normalized_direction.y * self.speed

        self.image = pygame.transform.rotate(
            self.original_image, self.direction.angle - 90
        )
        self.image = pygame.transform.scale(self.image, self.size)

        self.rect.center = (self.x, self.y)

        print(f"Player world pos: {self.rect.centerx}, {self.rect.centery}")

        if (
            self.rect.centerx < 0
            or self.rect.centerx > world_size
            or self.rect.centery < 0
            or self.rect.centery > world_size
        ):
            self.kill()

        self.collide(enemy_sprite_list, xp_sprite_list)

    def collide(self, enemy_sprite_list, xp_sprite_list):
        enemy_collisions = pygame.sprite.spritecollide(self, enemy_sprite_list, False)

        for enemy in enemy_collisions:
            enemy.take_damage(self.damage, xp_sprite_list)
            self.kill()
        
