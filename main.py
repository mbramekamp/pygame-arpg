import pygame

from classes.camera import Camera
from classes.enemy import Enemy
from classes.hud import HUD
from classes.map_generator import MapGenerator
from classes.player import Player
from classes.skills.fireball_skill import FireballSkill

pygame.init()
# nach pygame.init()
font = pygame.font.SysFont("Arial", 50)
# SCREEN SIZES
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1600


# WORLD SIZES
HEIGHT = 100
WIDTH = 100
TILE_SIZE = 32
WORLD_SIZE = HEIGHT * TILE_SIZE
COLORS = {"floor": (194, 178, 128), "wall": (30, 30, 30)}


# MAP FUNCTIONS


def draw_map(screen, tile_map, camera):
    for y in range(len(tile_map)):
        for x in range(len(tile_map[0])):
            tile = tile_map[y][x]
            color = COLORS[tile]

            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            rect = camera.apply_rect(rect)

            pygame.draw.rect(screen, color, rect)


# SPRITE LISTS

xp_sprite_list = pygame.sprite.Group()
enemy_sprite_list = pygame.sprite.Group()
projectile_sprite_list = pygame.sprite.Group()
xp_sprite_list = pygame.sprite.Group()

player = Player(
    x=WORLD_SIZE / 2,
    y=WORLD_SIZE / 2,
    front_image="images\\Player.png",
    side_image="images\\PlayerSide.png",
    back_image="images\\PlayerBack.png",
)

# debug
enemy = Enemy(image="images\\enemy.png", x=WORLD_SIZE / 3, y=WORLD_SIZE / 3)
enemy_sprite_list.add(enemy)
fireball = FireballSkill(
    name="Fireball",
    cooldown=3,
    cost=25,
    damage=50,
    speed=12,
    sound="",
    images="images\\FireBall.png",
    size=(75, 75),
)

player.active_skill_list.append(fireball)
camera = Camera(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
world_generator = MapGenerator()
noise_map = world_generator.generate_map()
tile_map = world_generator.create_tile_map(noise_map)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

hud = HUD(screen, player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    GAME_TIME = pygame.time.get_ticks() // 1000

    screen.fill("black")
    draw_map(screen, tile_map, camera)

    # UPDATE
    projectile_sprite_list.update(screen, WORLD_SIZE, enemy_sprite_list, xp_sprite_list)
    # print(f"After update, list size: {len(projectile_sprite_list)}")
    player.update(
        projectile_sprite_list, xp_sprite_list, GAME_TIME, camera, WORLD_SIZE, tile_map
    )
    enemy_sprite_list.update(player, camera, tile_map, WORLD_SIZE)
    camera.update(player, WORLD_SIZE)

    # RENDER
    for xp in xp_sprite_list:
        screen.blit(xp.image, camera.apply(xp))

    screen.blit(player.image, camera.apply(player))
    for enemy in enemy_sprite_list:
        screen.blit(enemy.image, camera.apply(enemy))

    for proj in projectile_sprite_list:
        screen.blit(proj.image, camera.apply(proj))

    pos_text = font.render(
        f"World: {int(player.rect.centerx)}, {int(player.rect.centery)}",
        True,
        (255, 255, 255),
    )

    screen.blit(pos_text, (10, 10))
    hud.draw_hud()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
