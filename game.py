from settings import *
from board import Board


class Game():
    def __init__(self):
        pygame.init()
        self.display_window = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True

        # make groups
        self.all_group = pygame.sprite.Group()

        # make board
        self.board = Board(self, self.all_group)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.display_window.fill("grey")
            self.all_group.update()

            # draw
            self.all_group.draw(self.display_window)
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
