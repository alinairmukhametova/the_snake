"""Игра Змейка на принципах ООП."""

import pygame
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=None):
        """
        Инициализация объекта.

        Args:
            position (tuple): Начальная позиция объекта.
        """
        self.position = position if position else (0, 0)
        self.body_color = None

    def draw(self):
        """Метод отрисовки (переопределяется в наследниках)."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Создаёт яблоко и задаёт ему случайную позицию."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Создает змейку в центре экрана."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            opposite = {
                UP: DOWN,
                DOWN: UP,
                LEFT: RIGHT,
                RIGHT: LEFT,
            }
            if self.next_direction != opposite.get(self.direction):
                self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        if len(self.positions) > 1:
            self.last = self.positions[-1]
        else:
            self.last = None

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку и стирает след."""
        for pos in self.positions[:-1]:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.positions:
            head_rect = pygame.Rect(
                self.positions[0], (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """
    Обрабатывает события клавиш.

    Args:
        game_object (Snake): объект управления.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and \
                    game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
