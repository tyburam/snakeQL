from sprites.drawable_object import DrawableObject
from sprites.point import Point

SNAKE_MOVES_LEFT = 0
SNAKE_MOVES_UP = 1
SNAKE_MOVES_RIGHT = 2
SNAKE_MOVES_DOWN = 3


def collides(x1, y1, x2, y2):
    return (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1)


class Snake(DrawableObject):
    def __init__(self, img, length=3):
        super().__init__(img)
        self.x = [0 for _ in range(length)]
        self.y = [5 for _ in range(length)]
        self.length = 3
        self.direction = SNAKE_MOVES_RIGHT
        self.step = 32

        self.x[0] = 4
        self.x[1] = 3
        self.x[2] = 2

    def __modify_position__(self, x, y):
        if self.direction == SNAKE_MOVES_LEFT:
            return x - 1, y
        if self.direction == SNAKE_MOVES_UP:
            return x, y - 1
        if self.direction == SNAKE_MOVES_RIGHT:
            return x + 1, y
        if self.direction == SNAKE_MOVES_DOWN:
            return x, y + 1

    def move(self, direction):
        self.direction = direction

        # everything besides head moves to the head position
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        self.x[0], self.y[0] = self.__modify_position__(self.x[0], self.y[0])

    def grow(self):
        self.length = self.length + 1
        self.x.append(-1)
        self.y.append(-1)

    def tail(self):
        return Point(self.x[-1], self.y[-1])

    def hist_its_tail(self):
        coll_x, coll_y = self.__modify_position__(self.x[0], self.y[0])

        for i in range(2, self.length):
            if (self.x[0] == self.x[i] and self.y[0] == self.y[i]) \
                    or (coll_x == self.x[i] and coll_y == self.y[i]):
                return True
        return False

    def hits_apple(self, x, y):
        for i in range(self.length):
            if collides(x, y, self.x[i], self.y[i]):
                self.grow()
                return True
        return False

    def get_segments_distance(self):
        dist = []
        for i in range(1, self.length):
            dist.append((self.x[0] - self.x[i], self.y[0] - self.y[i]))
        return dist

    def draw(self, surface):
        for i in range(0, self.length):
            surface.blit(self.img, (self.x[i] * self.step, self.y[i] * self.step))
