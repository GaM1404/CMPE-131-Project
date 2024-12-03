from .controller import Controller
import pygame

def main():
    game = Controller()
    game.game_loop()
    pygame.quit()

if __name__ == "__main__":
    main()
