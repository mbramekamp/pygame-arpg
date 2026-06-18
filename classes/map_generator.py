from random import randint

from opensimplex.api import OpenSimplex


class MapGenerator:
    seed: int
    map_width: int
    map_height: int
    tile_size: int
    scale: float

    def __init__(self):
        self.seed = randint(0, 2**32)
        self.map_width = 100
        self.map_height = 100
        self.tile_size = 32
        self.scale = 0.06

    def generate_map(self):

        noise_gen = OpenSimplex(seed=self.seed)

        matrix = [[0.0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        for y in range(self.map_height):
            for x in range(self.map_width):
                noise_value = noise_gen.noise2(x * self.scale, y * self.scale)
                matrix[y][x] = noise_value

        return matrix

    def create_tile_map(self, noise_matrix):
        tile_map = [["" for _ in range(self.map_width)] for _ in range(self.map_height)]

        for y in range(self.map_height):
            for x in range(self.map_width):
                value = noise_matrix[y][x]

                if value < 0.3:
                    tile_map[y][x] = "floor"
                elif value > 0.3:
                    tile_map[y][x] = "wall"
                else:
                    tile_map[y][x] = "wall"
        return tile_map
