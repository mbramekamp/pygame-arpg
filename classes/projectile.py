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

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, screen, world_size):
        print(f"Projectile update: x={self.x}, y={self.y}, direction={self.direction}")

        normalized_direction = self.direction.normalize()
        self.x += normalized_direction.x * self.speed
        self.y += normalized_direction.y * self.speed

        self.rect.center = (self.x, self.y)

        print(f"Player world pos: {self.rect.centerx}, {self.rect.centery}")

        if (
            self.rect.centerx < 0
            or self.rect.centerx > world_size
            or self.rect.centery < 0
            or self.rect.centery > world_size
        ):
            self.kill()
