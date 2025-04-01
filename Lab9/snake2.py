import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)

# Установки экрана
WIDTH = 600
HEIGHT = 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Шрифты
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)

# Размеры блока
BLOCK_SIZE = 10

# FPS контроллер
CLOCK = pygame.time.Clock()

# Начальная скорость
SNAKE_SPEED = 15

# Параметры для еды с таймером
FOOD_LIFETIME = 5  # сек

# Функция для отображения счета
def Your_score(score):
    value = SCORE_FONT.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(value, [0, 0])

# Функция для отображения уровня
def Your_level(level):
    value = SCORE_FONT.render(f"Level: {level}", True, BLACK)
    SCREEN.blit(value, [WIDTH - 120, 0])

# Функция для отрисовки змеи
def our_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(SCREEN, GREEN, [x[0], x[1], block, block])

# Функция для генерации еды со случайной ценностью
def food_spawn():
    x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    weight = random.choice([10, 20, 30])  # Случайная ценность еды
    return x, y, weight, time.time()  # Вернём и время создания еды

# Главная функция игры
def gameLoop():
    game_over = False
    game_close = False

    # Начальные координаты змеи
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # Генерация начальной еды
    foodx, foody, food_weight, food_time = food_spawn()

    score = 0
    level = 1

    global SNAKE_SPEED

    # Игровой цикл
    while not game_over:

        while game_close:
            SCREEN.fill(BLUE)
            message = FONT_STYLE.render("You Lost! Press Q-Quit or C-Play Again", True, RED)
            SCREEN.blit(message, [WIDTH / 6, HEIGHT / 3])
            Your_score(score)
            Your_level(level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Обработка управления
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # Проверка выхода за границы
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # Обновление позиции
        x1 += x1_change
        y1 += y1_change
        SCREEN.fill(BLUE)

        # Проверка таймера еды: если истёк — генерируем новую
        if time.time() - food_time >= FOOD_LIFETIME:
            foodx, foody, food_weight, food_time = food_spawn()

        # Отрисовка еды (разные цвета по весу)
        if food_weight == 10:
            color = YELLOW
        elif food_weight == 20:
            color = RED
        else:
            color = BLACK
        pygame.draw.rect(SCREEN, color, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # Обновление тела змеи
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Проверка на столкновение с собой
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Отрисовка змеи и счёта
        our_snake(BLOCK_SIZE, snake_list)
        Your_score(score)
        Your_level(level)

        pygame.display.update()

        # Проверка на поедание еды
        if x1 == foodx and y1 == foody:
            foodx, foody, food_weight, food_time = food_spawn()
            length_of_snake += 1
            score += food_weight  # Добавляем вес еды в счёт

            # Увеличение уровня и скорости
            if score % 60 == 0:
                level += 1
                SNAKE_SPEED += 2

        # Установка FPS
        CLOCK.tick(SNAKE_SPEED)

    pygame.quit()

# Запуск игры
gameLoop()
