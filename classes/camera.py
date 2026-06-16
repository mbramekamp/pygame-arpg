import pygame


class Camera:
    offset_x: int
    offset_y: int
    width: int
    height: int

    def __init__(self, WIDTH, HEIGHT):
        self.offset_x = 0
        self.offset_y = 0
        self.width = WIDTH / 2
        self.height = HEIGHT / 2

    def update(self, player):
        self.offset_x = player.rect.centerx - self.width
        self.offset_y = player.rect.centery - self.height

    def apply(self, sprite):
        x = sprite.rect.centerx - self.offset_x
        y = sprite.rect.centery - self.offset_y

        rect = pygame.Rect((x, y), sprite.rect.size)
        print(sprite.rect.centerx, self.offset_x, x)

        return rect

    def apply_rect(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)
