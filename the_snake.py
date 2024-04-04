from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов в игре 'Змейка'."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заготовка метода"""
        pass

# Класс для объектов яблока


class Apple(GameObject):
    """Класс описывающий отрисовку и положение яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Задаём случайным образом положение яблока"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Рисуем яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# Класс для объекта змеи


class Snake(GameObject):
    """Класс описывающий змею, её движение и событие съедания яблока"""

    def __init__(self):
        super().__init__()
        self.length = 1  # Начальная длина змеи
        # Начальное положение змеи в центре окна
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        # Начальное направление змеи - направо
        self.direction = RIGHT
        self.next_direction = None
        # Цвет змеи - зеленый.
        self.body_color = SNAKE_COLOR

    def get_head_position(self):
        """ПЕредаём положение головы змеи"""
        return self.positions[0]

    def move(self):
        """Движение змейки"""
        # Текущая голова змеи
        cur = self.get_head_position()
        # Текущее направление
        x, y = self.direction
        # Вычисляем новую позицию головы змеи
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH),
               (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        # Если голова встречается с телом, начать заново
        if len(self.positions) > 2 and new in self.positions[2:]:
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
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовываем змею на поле"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT

# Установка окна игры и инициализация игровых объектов


def main():
    """Создание объектов змеи и яблока. Событие съедания яблока"""
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.update_direction()
        snake.move()
        handle_keys(snake)
        # Змея съела яблоко и увеличилась, яблоко рандомно появилось на поле
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        # Рисуем змею и яблоко
        snake.draw()
        apple.draw()
        # Обновление экрана
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()

# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT
#                                and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT
#                                 and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
