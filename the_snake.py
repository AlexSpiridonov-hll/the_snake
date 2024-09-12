from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_BOARD = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
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
    """Класс GameObject содержит общие аттрибуты игровых объектов"""

    def __init__(self):
        self.body_color = None
        self.position = CENTER_BOARD

    def draw(self):
        """Это абстрактный метод"""
        pass

    def draw_cell(self):
        """Метод отрисовывает ячейку"""
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс Apple, унаследованный от GameObject.
    Описывает яблоко и действия с ним.
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(self.position)

    def randomize_position(self, old_position, snake_position=CENTER_BOARD):
        """Устанавливает случайное положение яблока на игровом поле."""
        while self.position in snake_position or self.position == old_position:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return self.position

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        super().draw_cell()


class Snake(GameObject):
    """Класс Snake унаследованный от GameObject.
    Описывает змейку и её поведение.
    """

    def __init__(self,):
        super().__init__()
        self.reset()

    def update_direction(self, direction):
        """Метод обновления направления после нажатия на кнопку"""
        self.direction = direction

    def move(self):
        """Обновляет позицию змейки на игровом поле"""
        head_x, head_y = self.get_head_position()
        move_x, move_y = self.direction
        new_head = ((head_x + (move_x * GRID_SIZE)) % SCREEN_WIDTH,
                    (head_y + (move_y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает игровое поле и начинает игру заново"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.body_color = SNAKE_COLOR
        self.positions = [CENTER_BOARD]
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш"""
    pygame_keys = {
        (pygame.K_UP, LEFT): UP,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_RIGHT, UP): RIGHT,
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_LEFT, DOWN): LEFT,
        (pygame.K_RIGHT, DOWN): RIGHT
    }
    global SPEED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.key, game_object.direction) in pygame_keys:
                game_object.update_direction(
                    pygame_keys[(event.key, game_object.direction)]
                )
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_MINUS:
                SPEED = max(SPEED - 1, 1)
            elif event.key == pygame.K_EQUALS:
                SPEED += 1


def main():
    """Основной цикл игры"""
    pygame.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        apple.draw()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(apple.position, snake.positions)
            apple.draw()
        elif snake.positions[0] in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(apple.position, snake.positions)
        pygame.display.update()


if __name__ == '__main__':
    main()
