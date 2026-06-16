import pygame


class Projectile(pygame.sprite.Sprite):
    x: int
    y: int
    size: tuple
    direction: pygame.math.Vector2
    speed: float
    damage: int
    sound: str
    screen: pygame.Surface

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

    def update(self):

        normalized_direction = self.direction.normalize()

        self.rect.centerx = self.rect.centerx + (normalized_direction.x * self.speed)
        self.rect.centery = self.rect.centery + (normalized_direction.y * self.speed)

        if (
            self.rect.centerx < 0
            or self.rect.centerx > self.screen.width
            or self.rect.centery < 0
            or self.rect.centery > self.screen.height
        ):
            self.kill()
