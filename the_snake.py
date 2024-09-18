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



class GameObject:
    """Базовый класс для игровых объектов."""
    def __init__(self, x, y, width, height, color):
        """Инициализирует объект с заданными параметрами."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        """Отрисовывает объект на экране."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Apple(GameObject):
    """Класс яблока."""
    def __init__(self, width, height, color):
        """Инициализирует яблоко с заданными размерами и цветом."""
        super().__init__(0, 0, width, height, color)
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайную позицию для яблока."""
        self.x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE

class Snake(GameObject):
    """Класс змейки."""
    def __init__(self, x, y, width, height, color):
        """Инициализирует змейку с заданными параметрами."""
        super().__init__(x, y, width, height, color)
        self.body = [(x, y)]  # Начальное положение змейки
        self.direction = RIGHT
        self.last = None # Переменная для хранения позиции предыдущего сегмента

    def draw(self, screen):
        """Отрисовывает змейку на экране."""
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.body[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Отрисовка тела змейки
        for segment in self.body[1:]:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], self.width, self.height))

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Перемещает змейку на одну клетку в заданном направлении."""
        head_x, head_y = self.body[0]
        new_head_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        self.last = self.body[-1] # Запоминаем позицию предыдущего сегмента
        self.body.insert(0, (new_head_x, new_head_y))
        self.body.pop()  # Удаляем последний элемент

    def change_direction(self, new_direction):
        """Изменяет направление движения змейки."""
        if new_direction != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction

    def check_collision(self):
        """Проверяет, столкнулась ли змейка сама с собой."""
        head_x, head_y = self.body[0]
        for segment in self.body[1:]:
            if head_x == segment[0] and head_y == segment[1]:
                return True
        return False

    def reset(self):
        """Сбрасывает змейку в исходное положение."""
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.last = None

def handle_keys():
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return LEFT
            elif event.key == pygame.K_RIGHT:
                return RIGHT
            elif event.key == pygame.K_UP:
                return UP
            elif event.key == pygame.K_DOWN:
                return DOWN
    return None


def main():
        """Основная функция игры."""
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Змейка')
        clock = pygame.time.Clock()

        # Создание змейки и яблока
        snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, GRID_SIZE, GRID_SIZE, SNAKE_COLOR)
        apple = Apple(GRID_SIZE, GRID_SIZE, APPLE_COLOR)

        # Основной игровой цикл
        running = True
        while running:
            # Обработка событий
            new_direction = handle_keys()
            if new_direction:
                snake.change_direction(new_direction)

            # Движение змейки
            snake.move()

            # Проверка столкновений
            if snake.check_collision():
                snake.reset()

            # Проверка поедания яблока
            if snake.body[0] == (apple.x, apple.y):
                snake.body.append(snake.body[-1])
                apple.randomize_position()

            # Отрисовка объектов
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.draw(screen)
            snake.draw(screen)

            # Обновление экрана
            pygame.display.update()

            # Регулировка скорости игры
            clock.tick(SPEED)

        # Завершение Pygame
        pygame.quit()
if __name__ == '__main__':
    main()

