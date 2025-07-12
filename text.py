from settings import *


class Text(pygame.sprite.Sprite):
    def __init__(self, font, text, color, pos, groups):
        super().__init__(groups)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_frect(center=pos)
