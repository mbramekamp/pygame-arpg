import pygame

class HUD:

    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

    
    def draw_hud(self):
        # Draw health bar
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10

        health_percentage, xp_percentage, mana_percentage = self.player.calculate_percentages()
        
        self.draw_bar(bar_x, bar_y, bar_width, bar_height, health_percentage, (255, 0, 0))
        self.draw_bar(bar_x, bar_y + 30, bar_width, bar_height, mana_percentage, (0, 0, 255))
        self.draw_bar(bar_x, bar_y + 60, bar_width, bar_height, xp_percentage, (0, 255, 0))

    def draw_bar(self, x, y, width, height, percentage, color):
        pygame.draw.rect(self.screen, (20, 20, 20), (x, y, width, height))
        pygame.draw.rect(self.screen, color, (x, y, width * percentage, height))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, width, height), 2)