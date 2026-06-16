import pygame


class XP(pygame.sprite.Sprite):
    value: int
    size: tuple

    def __init__(self, image, x, y):
        super().__init__()
        self.value = 5
        self.size = (5, 5)

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(x, y))
