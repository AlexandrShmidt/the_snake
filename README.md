Змейка (Snake Game)
Простая реализация классической игры "Змейка" на Python с использованием библиотеки Pygame.

Описание игры:

Это моя первая игра на Python, написанная с применением объектно-ориентированного программирования. Игра представляет собой классическую "Змейку", похожую на версию из старых телефонов Nokia.

Управление:

Стрелки на клавиатуре - изменение направления движения змейки

Крестик в правом верхнем углу - выход из игры

Правила игры:

Змейка появляется в центре экрана

Управляя змейкой, нужно собирать яблоки (красные квадраты)

При съедании яблока змейка увеличивается на один сегмент

Игра заканчивается, если змейка врезается в саму себя

Игровое поле имеет замкнутые границы - змейка может выходить за край и появляться с противоположной стороны

Особенности реализации:

Игра написана с использованием ООП

Основные классы:

GameObject - базовый класс для игровых объектов

Apple - класс для яблок

Snake - класс для змейки

Размер игрового поля фиксированный (640x480 пикселей)

Размер ячейки сетки - 20 пикселей

Скорость игры регулируется константой SPEED

Требования
Python 3.x

Pygame

Запуск игры
Просто запустите файл с игрой: python snake_game.py

Это моя первая игра, поэтому некоторые функции (например, полноэкранный режим) пока не реализованы. Игра создана в учебных целях.

Приятной игры!
