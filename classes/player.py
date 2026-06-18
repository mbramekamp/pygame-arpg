import pygame

from classes.skills.active_skill import ActiveSkill
from classes.skills.passive_skill import PassiveSkill


class Player(pygame.sprite.Sprite):
    health: int
    max_health: int
    armour: int
    speed: float
    xp: int
    required_xp: int
    mana: int
    max_mana: int
    level: int

    x: float
    y: float

    size: tuple
    passive_skill_list: list[PassiveSkill]
    active_skill_list: list[ActiveSkill]

    def __init__(self, x, y, front_image, side_image, back_image):
        super().__init__()
        self.health = 100
        self.max_health = self.health
        self.armour = 0
        self.speed = 10
        self.xp = 0
        self.mana = 100
        self.max_mana = self.mana
        self.level = 1
        self.required_xp = int(25 * self.level**1.7)

        self.x = x
        self.y = y

        self.size = (100, 100)

        self.passive_skill_list = []
        self.active_skill_list = []

        self.front_image = pygame.image.load(front_image)
        self.front_image = pygame.transform.scale(self.front_image, self.size)

        self.side_image = pygame.image.load(side_image)
        self.side_image = pygame.transform.scale(self.side_image, self.size)

        self.back_image = pygame.image.load(back_image)
        self.back_image = pygame.transform.scale(self.back_image, self.size)

        self.image: pygame.Surface = pygame.image.load(front_image)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(x, y))

    def update(
        self,
        projectile_sprite_list,
        xp_sprite_list,
        game_time,
        camera,
        world_size,
        tile_map,
    ):

        # Player values in update
        player_world_position = camera.apply(self)

        prev_x = self.rect.centerx
        prev_y = self.rect.centery

        tile_x = self.rect.centerx // 32
        tile_y = self.rect.centery // 32

        # mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_direction_x = mouse_x - player_world_position.centerx
        mouse_direction_y = mouse_y - player_world_position.centery

        mouse_vector = pygame.math.Vector2(mouse_direction_x, mouse_direction_y)
        mouse_vector = mouse_vector.normalize()

        # MOVEMENT
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.image = self.back_image
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.image = self.front_image
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.image = pygame.transform.flip(self.side_image, True, False)
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  #
            self.image = self.side_image
            dx += 1

        directional_vector = pygame.math.Vector2(dx, dy)

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

        self.rect.centerx = max(
            0, min(self.rect.centerx, world_size - self.size[0] / 2)
        )
        self.rect.centery = max(
            0, min(self.rect.centery, world_size - self.size[0] / 2)
        )

        # ABILITY CASTING
        self.ability_casting(mouse_vector, projectile_sprite_list, game_time, camera)

        # XP PICKUP
        self.pick_up_xp(xp_sprite_list)

        # CHECK LEVEL UP
        self.check_level_up()

        # print(f"tile_x: {tile_x}, tile_y: {tile_y}, tile: {tile_map[tile_y][tile_x]}")

        self.regen_property("health", "max_health", 3, 20, game_time)
        self.regen_property("mana", "max_mana", 2, 25, game_time)

    def ability_casting(self, mouse_vector, projectile_sprite_list, game_time, camera):

        keys = pygame.key.get_pressed()

        if not self.active_skill_list:
            pass
        else:
            if len(self.active_skill_list) >= 1:
                if self.active_skill_list[0].can_cast(game_time):
                    if keys[pygame.K_1]:
                        if self.mana >= self.active_skill_list[0].cost:
                            projectile = self.active_skill_list[0].cast(
                                x=self.rect.centerx,
                                y=self.rect.centery,
                                direction=mouse_vector,
                            )
                            projectile_sprite_list.add(projectile)
                            self.active_skill_list[0].last_cast_time = (
                                pygame.time.get_ticks() // 1000
                            )
                            self.mana -= self.active_skill_list[0].cost

            if len(self.active_skill_list) >= 2:
                if self.active_skill_list[1].can_cast(game_time):
                    if keys[pygame.K_2]:
                        if self.mana > self.active_skill_list[1].cost:
                            projectile = self.active_skill_list[1].cast(
                                x=self.rect.centerx,
                                y=self.rect.centery,
                                direction=mouse_vector,
                            )
                            projectile_sprite_list.add(projectile)
                            self.active_skill_list[1].last_cast_time = (
                                pygame.time.get_ticks() // 1000
                            )
                            self.mana -= self.active_skill_list[1].cost

            if len(self.active_skill_list) >= 3:
                if self.active_skill_list[2].can_cast(game_time):
                    if keys[pygame.K_3]:
                        if self.mana > self.active_skill_list[2].cost:
                            projectile = self.active_skill_list[2].cast(
                                x=self.rect.centerx,
                                y=self.rect.centery,
                                direction=mouse_vector,
                            )
                            projectile_sprite_list.add(projectile)
                            self.active_skill_list[2].last_cast_time = (
                                pygame.time.get_ticks() // 1000
                            )
                            self.mana -= self.active_skill_list[2].cost

            if len(self.active_skill_list) >= 4:
                if self.active_skill_list[3].can_cast(game_time):
                    if keys[pygame.K_4]:
                        if self.mana > self.active_skill_list[3].cost:
                            projectile = self.active_skill_list[3].cast(
                                x=self.rect.centerx,
                                y=self.rect.centery,
                                direction=mouse_vector,
                            )
                            projectile_sprite_list.add(projectile)
                            self.active_skill_list[3].last_cast_time = (
                                pygame.time.get_ticks() // 1000
                            )
                            self.mana -= self.active_skill_list[3].cost

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

    def take_damage(self, amount):
        self.health -= amount
        print(f"Player Health: {self.health}")
        if self.health <= 0:
            pygame.quit()

    def calculate_percentages(self):
        health_percentage = self.health / self.max_health
        xp_percentage = self.xp / int(25 * self.level**1.7)
        mana_percentage = self.mana / self.max_mana
        print(f"mana %: {mana_percentage}, mana: {self.mana}")
        return health_percentage, xp_percentage, mana_percentage

    def regen_property(self, attribute, max_attribute, amount, frequency, game_time):
        if game_time % frequency == 0 and getattr(self, attribute) < getattr(
            self, max_attribute
        ):
            value = min(getattr(self, attribute) + amount, getattr(self, max_attribute))
            setattr(self, attribute, value)
