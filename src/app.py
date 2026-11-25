"""Графический интерфейс tkinter."""
import tkinter as tk
from src.model import Snake


class App:
    """Окно и цикл анимации без блокирующих ожиданий."""

    def __init__(self):
        """Создать окно, поле и привязки клавиш."""
        self.root = tk.Tk()
        self.root.title('Змейка')
        self.root.resizable(False, False)
        self.label = tk.Label(self.root, font=('Arial', 14))
        self.label.pack(pady=8)
        self.canvas = tk.Canvas(self.root, width=480, height=480,
                                bg='#152238', highlightthickness=0)
        self.canvas.pack()
        tk.Label(self.root, text='Стрелки — движение | Space — пауза | '
                 'R — заново | Esc — выход').pack(pady=8)
        self.root.bind('<KeyPress>', self.key)
        self.game = Snake()
        self.paused = False
        self.draw()
        self.root.after(140, self.tick)

    def key(self, event):
        """Обработать управление игрой."""
        directions = {'Up': (0, -1), 'Down': (0, 1),
                      'Left': (-1, 0), 'Right': (1, 0)}
        if event.keysym in directions and not self.paused:
            self.game.turn(directions[event.keysym])
        elif event.keysym == 'space':
            self.paused = not self.paused
        elif event.keysym.lower() == 'r':
            self.game = Snake()
            self.paused = False
        elif event.keysym == 'Escape':
            self.root.destroy()
            return
        self.draw()

    def draw(self):
        """Отрисовать змейку, еду, счёт и состояние."""
        self.canvas.delete('all')
        for i, cell in enumerate(self.game.body):
            self.cell(cell, '#8ee39b' if i == 0 else '#38ad70')
        if self.game.food is not None:
            self.cell(self.game.food, '#f87868')
        state = 'Пауза' if self.paused else ''
        if self.game.over:
            state = ('Победа!' if self.game.food is None
                     else 'Игра окончена!') + ' R — заново'
        self.label.config(text=f'Счёт: {self.game.score}   {state}')

    def cell(self, position, color):
        """Нарисовать одну клетку."""
        x, y = position
        self.canvas.create_rectangle(
            x * 24 + 1, y * 24 + 1, (x + 1) * 24 - 1,
            (y + 1) * 24 - 1, fill=color, outline='')

    def tick(self):
        """Выполнить ход и запланировать следующий кадр."""
        if not self.paused:
            self.game.step()
        self.draw()
        self.root.after(max(65, 140 - self.game.score * 3), self.tick)

    def run(self):
        """Запустить цикл событий окна."""
        self.root.mainloop()
