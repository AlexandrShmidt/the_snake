"""

Сокращаем название библиотеки pygame для удобства.
Импортируем её.
Импортируем функцию randint из модуля random.

"""

import pygame as pg
from random import randint


""""

Здравствуйте! Меня зовут Александр.
Представляю вам свой первый проект на языке программирования Python.
Я написал для вас игру, классическая 'The snake'.
Не такая конечно, как мы любили на Nokia.
Но что то очень похожее.
Играть очень просто.
Запускаете этот файл.
Змейка появляется в середине экрана размером в одну клетку.
С помощью стрелочек на клавиатуре вы направляете змейку.
Когда она сьедает яблоко - растёт на одну клетку.
Если врежется сама в себя игра закончена.
Что бы выйти из игры нажмите на крестик в правом верхнем углу.
Открыть змейку на весь экран к сожалению нельзя.
Я ещё только учусь программировнию.
Не судите строго.
Спасибо, что поиграли в мою игру.

"""

"""

Здесь расскажу немного о самом коде.
Игра написана с применением ООП.
Есть основной класс, GameObject.
Он отвечает за параметры цвета и отрисовки обьектов.
У GameObject два наследника.
Apple and Snake.
Apple наследует от GameObject только цвет.Переопределяет отрисовку.
Snake инициализирует змейку с новыми праметрами.
Переопределяет отрисовку.
Инициализирует напрвление движения змейки.
Проверяет на столкновения  с яблоком.
Добавляет змейке длину.
Ещё здесть есть метод handle_keys.
Он отвечает за обработку нажатия клавиш.
Метод def main описывает всю игру.
Вызывает отрисовку поля, яблока, змейки
и запускает цикл игры.ы
Ниже под каждым классом и методом подписано, что он делает,
что бы вам было понятнее.
Спасибо за внимание!

"""

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Позиция по умолчанию (центр экрана)
DEFAULT_CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

pg.init()


class GameObject:
    # Класс, описывающий обекты игры

    def __init__(self, body_color=None) -> None:
        """

        self.position = DEFAULT_CENTER_POSITION.
        Эта строка задаёт начальную позицию обьекта.
        self.position это атрибут обьекта,
        который хранит его координаты на игровом поле.
        = это оператор присваивания. Он устанавливает значение атрибуту.
        DEFAULT_CENTER_POSITION это переменная,
        которая хранит координаты центра игрового поля.

        """
        self.position = DEFAULT_CENTER_POSITION
        self.body_color = body_color

    def draw(self):

        """

        Метод отрисовки объектов.
        Он переопределится в наследуемых классах.

        """

    def draw_cell(self, coordinat, body_color=None, border_color=None):
        # Метод для отрисовки одной ячейки
        if not body_color:
            body_color = self.body_color
        if not border_color:
            border_color = BORDER_COLOR

        rect = pg.Rect(coordinat, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    # Класс, описывающий яблоко в игре

    def __init__(self, ignored=None, body_color=None) -> None:
        super().__init__(body_color)
        if ignored is None:
            ignored = []
        self.randomize_position(ignored)

    def randomize_position(self, ignored):
        """

        Генерирует случайную позицию для яблока.
        Учитывает занятые клетки(ignored)

        """
        while True:
            horizontal = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            vertical = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (horizontal, vertical)
            # Условие ниже гарантирует, что яблоко не появится.
            # На занятых клетках.
            if self.position not in ignored:
                break

    def draw(self):
        # Отрисовывает яблоко на экране.
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    # Класс змейки.

    def __init__(self, body_color=None):
        # Инициализирует змейку с заданными параметрами.
        super().__init__(body_color)
        self.length = 1
        self.positions = [DEFAULT_CENTER_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position(), self.body_color, BORDER_COLOR)
        # Отрисовка тела змейки
        for segment in self.positions[1:]:
            self.draw_cell(segment, self.body_color)
        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def move(self):
        # Перемещает змейку на одну клетку в заданном направлении.
        head_x, head_y = self.get_head_position()
        # Распаковка направления.
        delta_x, delta_y = self.direction
        new_head_x = (head_x + delta_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT
        self.last = self.positions[-1]  # Позиция предыдущей ячейки змеи.
        self.positions.insert(0, (new_head_x, new_head_y))
        # Удаляем последний элемент, если длина змейки не увеличилась.
        if len(self.positions) > self.length:
            self.positions.pop()
        else:
            # Зануляем self.last, если длина змейки не увеличилась.
            self.last = None

    def change_direction(self, new_direction):
        # Изменяет направление движения змейки.
        self.next_direction = new_direction

    def update_direction(self):
        # Обновляет направление движения змейки.
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        # Сбрасывает змейку в исходное положение.
        self.positions = [DEFAULT_CENTER_POSITION]
        self.last = None
        self.length = 1
        # Используем get_head_position
        self.position = self.get_head_position()
        # Устанавливаем случайное направление змейки.
        self.direction = [UP, DOWN, LEFT, RIGHT][randint(0, 3)]

    def get_head_position(self):
        # Возвращает позицию головы змейки.
        return self.positions[0]

    def eat_apple(self, apple):
        """

        Увеличивает длину змейки.
        Обновляет её позицию после поедания яблока.

        self.positions = [apple.position] + self.positions
        Эта строчка кода добавляет apple.position,
        (координаты яблока) в начало списка self.positions (позиций змеи).
        apple.position: Это кортеж (x, y),
        представляющий координаты яблока на поле.
        self.positions: Это список кортежей,
        хранящий координаты всех сегментов змеи.
        В этом контексте оператор + означает конкатенацию списков.
        Он создает новый список, объединяющий два исходных списка.
        [apple.position]: Здесь создается новый список,
        содержащий только один элемент - apple.position.
        Это делается для того,
        чтобы мы могли использовать оператор + для конкатенации списков.
        Почему именно так я сделал?
        Простая логика: Это простой и прямой способ
        обновить self.positions после поедания яблока.
        Мы просто вставляем позицию яблока в начало списка,
        что делает яблоко “головой” змеи.
        Эффективность: Конкатенация списков -
        относительно эффективная операция,
        поэтому это хорошее решение.
        С точки зрения производительности.

        """
        self.length += 1
        self.positions = [apple.position] + self.positions


def handle_keys(snake):
    # Обрабатывает нажатия клавиш.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                snake.change_direction(RIGHT)
            elif event.key == pg.K_UP:
                snake.change_direction(UP)
            elif event.key == pg.K_DOWN:
                snake.change_direction(DOWN)
    # Обновляем направление змейки
    return True


def main():

    """
    snake.positions - это список координат,
    которые уже заняты змеей.
    Эти координаты передаются в Apple.__init__ как ignored,
    чтобы яблоко не появилось на змее.

    """

    # Метод, описывающий главную логику игры.
    pg.init()
    snake = Snake(body_color=SNAKE_COLOR)
    apple = Apple(snake.positions, body_color=APPLE_COLOR)
    apple.draw()
    # Заливаем фон при старте
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        # Вызов handle_keys для обработки нажатий клавиш
        if not handle_keys(snake):
            break
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            # Передаём ignored в randomize_position
            # Перемещаем яблоко после сброса змейки
            apple.randomize_position(snake.positions)
            # Заливаем фон при сбросе
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.get_head_position() == apple.position:
            snake.eat_apple(apple)
            # Передаём ignored в randomize_position
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
