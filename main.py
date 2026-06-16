import pygame

from classes.camera import Camera
from classes.enemy import Enemy
from classes.map_generator import MapGenerator
from classes.player import Player

pygame.init()

# SCREEN SIZES
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1600


# WORLD SIZES
HEIGHT = 1000
WIDTH = 1000
TILE_SIZE = 32
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

player = Player(x=WIDTH / 2, y=HEIGHT / 2, image="images\\Player.png")

# debug
# enemy = Enemy(image="images\\enemy.png", x=800, y=700)
# enemy_sprite_list.add(enemy)

camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
world_generator = MapGenerator()
noise_map = world_generator.generate_map()
tile_map = world_generator.create_tile_map(noise_map)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    GAME_TIME = pygame.time.get_ticks() // 1000

    screen.fill("black")
    draw_map(screen, tile_map, camera)

    # UPDATE
    projectile_sprite_list.update()
    player.update(xp_sprite_list, projectile_sprite_list, GAME_TIME)
    enemy_sprite_list.update(player)
    camera.update(player)

    # RENDER
    for xp in xp_sprite_list:
        screen.blit(xp.image, camera.apply(xp))

    screen.blit(player.image, camera.apply(player))
    for enemy in enemy_sprite_list:
        screen.blit(enemy.image, camera.apply(enemy))

    for proj in projectile_sprite_list:
        screen.blit(proj.image, camera.apply(proj))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
