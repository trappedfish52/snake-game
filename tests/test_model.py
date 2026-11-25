"""Тестирование правил без графического окна."""
import unittest
from src.model import Snake


class SnakeTests(unittest.TestCase):
    """Проверки роста, границ и управления."""

    def test_food(self):
        """Еда увеличивает длину и счёт."""
        game = Snake()
        game.food = (11, 10)
        game.step()
        self.assertEqual((game.score, len(game.body)), (1, 2))
        self.assertNotIn(game.food, game.body)

    def test_wall(self):
        """Стена завершает игру."""
        game = Snake()
        game.body = [(19, 10)]
        game.step()
        self.assertTrue(game.over)

    def test_reverse(self):
        """Нельзя развернуться назад между кадрами."""
        game = Snake()
        game.turn((0, -1))
        game.turn((-1, 0))
        game.step()
        self.assertEqual(game.body[0], (10, 9))

    def test_self_collision(self):
        """Столкновение с телом завершает игру."""
        game = Snake()
        game.body = [(2, 2), (3, 2), (3, 3), (2, 3)]
        game.step()
        self.assertTrue(game.over)
