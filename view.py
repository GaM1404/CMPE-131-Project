import pygame

class View:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Blackjack Game")
        self.font = pygame.font.SysFont("Arial", 30)

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_card(self, card, x, y):
        card_image = pygame.image.load(f"assets/card_images/{card.rank}.png")
        self.screen.blit(card_image, (x, y))

    def draw_background(self):
        self.screen.fill((0, 128, 0))  # Green background like a card table

    def update(self):
        pygame.display.update()

    def display_message(self, message):
        self.screen.fill((0, 0, 0))
        self.draw_text(message, self.screen_width // 2 - 100, self.screen_height // 2)
        self.update()
        pygame.time.wait(2000)
