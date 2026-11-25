"""Правила змейки без графики."""
import random


class Snake:
    """Поле 20 на 20, еда и движение змейки."""

    def __init__(self):
        """Начать новую игру."""
        self.body = [(10, 10)]
        self.direction = (1, 0)
        self.pending = (1, 0)
        self.score = 0
        self.over = False
        self.food = self.new_food()

    def new_food(self):
        """Разместить еду в свободной клетке."""
        free = [(x, y) for x in range(20) for y in range(20)
                if (x, y) not in self.body]
        return random.choice(free) if free else None

    def turn(self, direction):
        """Запретить разворот назад относительно текущего движения."""
        if direction != (-self.direction[0], -self.direction[1]):
            self.pending = direction

    def step(self):
        """Передвинуть змейку, проверить еду и столкновения."""
        if self.over:
            return
        self.direction = self.pending
        x, y = self.body[0]
        dx, dy = self.direction
        head = (x + dx, y + dy)
        eating = head == self.food
        # Без роста хвост освобождает клетку в этот же ход.
        occupied = self.body if eating else self.body[:-1]
        if (not 0 <= head[0] < 20 or not 0 <= head[1] < 20
                or head in occupied):
            self.over = True
            return
        self.body.insert(0, head)
        if eating:
            self.score += 1
            self.food = self.new_food()
            self.over = self.food is None
        else:
            self.body.pop()
