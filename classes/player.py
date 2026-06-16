import pygame

from classes.skills.active_skill import ActiveSkill
from classes.skills.passive_skill import PassiveSkill


class Player(pygame.sprite.Sprite):
    health: int
    armour: int
    speed: float
    xp: int
    level: int

    x: float
    y: float

    size: tuple
    passive_skill_list: list[PassiveSkill]
    active_skill_list: list[ActiveSkill]

    def __init__(self, x, y, image):
        super().__init__()
        self.health = 100
        self.armour = 0
        self.speed = 10
        self.xp = 0
        self.level = 1

        self.x = x
        self.y = y

        self.size = (100, 100)

        self.passive_skill_list = []
        self.active_skill_list = []

        self.image: pygame.Surface = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, projectile_sprite_list, xp_sprite_list, game_time):

        # mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_direction_x = mouse_x - self.rect.centerx
        mouse_direction_y = mouse_y - self.rect.centery

        mouse_vector = pygame.math.Vector2(mouse_direction_x, mouse_direction_y)
        mouse_vector = mouse_vector.normalize()

        # MOVEMENT
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.image = pygame.transform.rotate(self.image, 90)
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.image = pygame.transform.rotate(self.image, 0)
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.image = pygame.transform.rotate(self.image, 270)
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.image = pygame.transform.rotate(self.image, 180)
            dx += 1

        directional_vector = pygame.math.Vector2(dx, dy)

        if directional_vector.length() > 0:
            normalized_direction = directional_vector.normalize()

            self.rect.centerx = self.rect.centerx + (
                normalized_direction.x * self.speed
            )
            self.rect.centery = self.rect.centery + (
                normalized_direction.y * self.speed
            )

        # ABILITY CASTING
        self.ability_casting(mouse_vector, projectile_sprite_list, game_time)

        # XP PICKUP
        self.pick_up_xp(xp_sprite_list)

        # CHECK LEVEL UP
        self.check_level_up()

    def ability_casting(self, mouse_vector, projectile_sprite_list, game_time):

        keys = pygame.key.get_pressed()

        if not self.active_skill_list:
            pass
        else:
            if len(self.active_skill_list) >= 1:
                if self.active_skill_list[0].can_cast(game_time):
                    if keys[pygame.K_1]:
                        projectile = self.active_skill_list[0].cast(
                            x=self.rect.centerx,
                            y=self.rect.centery,
                            direction=mouse_vector,
                        )
                        projectile_sprite_list.add(projectile)
            if len(self.active_skill_list) >= 2:
                if self.active_skill_list[1].can_cast(game_time):
                    if keys[pygame.K_2]:
                        projectile = self.active_skill_list[1].cast(
                            x=self.rect.centerx,
                            y=self.rect.centery,
                            direction=mouse_vector,
                        )
                        projectile_sprite_list.add(projectile)

            if len(self.active_skill_list) >= 3:
                if self.active_skill_list[2].can_cast(game_time):
                    if keys[pygame.K_3]:
                        projectile = self.active_skill_list[2].cast(
                            x=self.rect.centerx,
                            y=self.rect.centery,
                            direction=mouse_vector,
                        )
                        projectile_sprite_list.add(projectile)
            if len(self.active_skill_list) >= 4:
                if self.active_skill_list[3].can_cast(game_time):
                    if keys[pygame.K_4]:
                        projectile = self.active_skill_list[3].cast(
                            x=self.rect.centerx,
                            y=self.rect.centery,
                            direction=mouse_vector,
                        )
                        projectile_sprite_list.add(projectile)

    def pick_up_xp(self, xp_sprite_list):

        xp_collisions = pygame.sprite.spritecollide(self, xp_sprite_list, True)

        for xp in xp_collisions:
            self.xp += xp.value

    def check_level_up(self):
        required_xp = int(25 * self.level**1.7)

        while self.xp >= required_xp:
            self.xp -= required_xp
            self.level += 1
            required_xp = int(25 * self.level**1.7)
