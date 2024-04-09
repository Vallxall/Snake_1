from random import randint

import pygame as pg
# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BOARD_BACKGROUND_COLOR = (220, 220, 220)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 15
DIRECTION_MAP = {
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
}

# Переменная для хранения рекордной длины
highscore_length = 0

# Настройка скорости обновления
current_speed = SPEED
clock = pg.time.Clock()

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов в игре 'Змейка'."""

    def __init__(self, position=(0, 0), body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заготовка метода"""

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку на поле."""
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывающий отрисовку и положение яблока"""

    def __init__(self, snake_positions):
        super().__init__(snake_positions)
        self.body_color = APPLE_COLOR
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Задаём случайным образом положение яблока не занятое змеёй"""
        self.position = None
        while self.position is None or self.position in snake_positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Рисуем яблоко"""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс описывающий змею, её движение и событие съедания яблока"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.last = None
        self.length = 1

    def get_head_position(self):
        """Передаём положение головы змеи"""
        return self.positions[0]

    def move(self):
        """Движение змейки"""
        # Текущая голова змеи
        head_snake = self.get_head_position()
        # Текущее направление
        x, y = self.direction
        # Вычисляем новую позицию головы змеи
        new = (((head_snake[0] + (x * GRID_SIZE)) % SCREEN_WIDTH),
               (head_snake[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        # Если голова встречается с телом, начать заново
        if len(self.positions) > 2 and new in self.positions:
            self.reset()
        else:
            # Вставляем новую позицию головы на первое место в список
            self.positions.insert(0, new)
            # Удаляем последний элемент, если длина списка больше длины змеии
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def reset(self):
        """Сброс змеи к начальной позиции"""
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.length = 1
        self.last = None

    def update_direction(self, new_direction=None):
        """Метод обновления направления после нажатия на кнопку"""
        if new_direction:
            self.direction = new_direction

    def draw(self):
        """рисуем змею"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        for pos in self.positions:
            self.draw_cell(pos, self.body_color)
        if self.last:
            self.draw_cell(self.last, SNAKE_COLOR)


def handle_keys(snake):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            # Обработка нажатия ESC для завершения игры
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            new_direction = DIRECTION_MAP.get((snake.direction, event.key))
            if new_direction:
                snake.update_direction(new_direction)

# Установка окна игры и инициализация игровых объектов


def main():
    """Создание объектов змеи и яблока. Событие съедания яблока"""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(current_speed)
        snake.update_direction()
        handle_keys(snake)
        snake.move()

        # Змея съела яблоко и увеличилась, яблоко рандомно появилось на поле
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        # Рисуем змею и яблоко
        snake.draw()
        apple.draw()

        # Обновляем заголовок окна с текущей скоростью змеи
        pg.display.set_caption(f'Змейка – Скорость: {current_speed}')

        # Обновление экрана
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
