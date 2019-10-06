import numpy as np

from sprites.drawable_object import DrawableObject


class Apple(DrawableObject):
    def __init__(self, img, x, y):
        super().__init__(img)
        self.x = x
        self.y = y
        self.size = 32

    def move(self):
        self.x = np.random.randint(0, 10)
        self.y = np.random.randint(0, 10)

    def draw(self, surface):
        surface.blit(self.img, (self.x * self.size, self.y * self.size))
