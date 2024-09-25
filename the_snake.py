import pygame
from random import randint

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

# Позиция по умолчанию (центр экрана)
DEFAULT_CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

pygame.init()

class GameObject:
    """Класс, описывающий обекты игры"""

    def __init__(self, body_color=None) -> None:
        self.position = DEFAULT_CENTER_POSITION
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объектов,
        который переопределится в наследуемых классах
        """

    def draw_cell(self, coordinat, body_color=None, border_color=None):
        """Метод для отрисовки одной ячейки"""
        if not body_color:
            body_color = self.body_color
        if not border_color:
            border_color = BORDER_COLOR

        rect = pygame.Rect(coordinat, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, border_color, rect, 1)

class Apple(GameObject):
    """Класс, описывающий яблоко в игре"""

    def __init__(self, ignored=None, body_color=None) -> None:
        super().__init__(body_color)
        if ignored is None:
            ignored = []
        self.ignored = ignored
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайную позицию для яблока."""
        while True:
            self.x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            self.y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (self.x, self.y)
            if self.position not in self.ignored:
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_cell(self.position, self.body_color)

class Snake(GameObject):
    """Класс змейки."""
    def __init__(self, body_color=None):
        """Инициализирует змейку с заданными параметрами."""
        super().__init__(body_color)
        self.length = 1
        self.positions = [DEFAULT_CENTER_POSITION]  # Начальное положение змейки
        self.direction = RIGHT
        self.next_direction = None
        self.last = None  # Переменная для хранения позиции предыдущего сегмента

    def draw(self):
        """Отрисовывает змейку на экране."""
        # Отрисовка головы змейки
        self.draw_cell(self.positions[0], self.body_color, BORDER_COLOR)

        # Отрисовка тела змейки
        for segment in self.positions[1:]:
            self.draw_cell(segment, self.body_color)

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def move(self):
        """Перемещает змейку на одну клетку в заданном направлении."""
        head_x, head_y = self.positions[0]
        new_head_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        self.last = self.positions[-1]  # Запоминаем позицию предыдущего сегмента
        self.positions.insert(0, (new_head_x, new_head_y))

        # Удаляем последний элемент, если длина змейки не увеличилась
        if len(self.positions) > self.length:
            self.positions.pop()

        self.position = self.positions[0]

    def change_direction(self, new_direction):
        """Изменяет направление движения змейки."""
        self.next_direction = new_direction

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def check_collision(self):
        """Проверяет, столкнулась ли змейка сама с собой."""
        head_x, head_y = self.positions[0]
        for segment in self.positions[1:]:
            if head_x == segment[0] and head_y == segment[1]:
                return True
        return False

    def reset(self):
        """Сбрасывает змейку в исходное положение."""
        self.positions = [DEFAULT_CENTER_POSITION]
        self.direction = RIGHT
        self.last = None
        self.length = 1
        self.position = self.positions[0]

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)
            elif event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
    
    # Обновляем направление змейки
    snake.update_direction()
    return True


def main():
    """Метод, описывающий главную логику игры"""
    pygame.init()
    snake = Snake(body_color=SNAKE_COLOR)
    apple = Apple(snake.positions, body_color=APPLE_COLOR)
    apple.draw()

    while True:
        clock.tick(SPEED)
        # Вызов handle_keys для обработки нажатий клавиш
        if not handle_keys(snake):
            break
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.positions = [apple.position] + snake.positions
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()