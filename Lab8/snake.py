import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

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


# Функция для отрисовки еды
def food_spawn():
    x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    return x, y


# Главная функция игры
def gameLoop():
    game_over = False
    game_close = False

    # Начальные параметры
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # Генерация начальной еды
    foodx, foody = food_spawn()

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

        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # Проверка на выход за пределы экрана
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # Обновляем позицию змеи
        x1 += x1_change
        y1 += y1_change
        SCREEN.fill(BLUE)
        pygame.draw.rect(SCREEN, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(BLOCK_SIZE, snake_list)
        Your_score(score)
        Your_level(level)

        pygame.display.update()

        # Проверка на поедание еды
        if x1 == foodx and y1 == foody:
            foodx, foody = food_spawn()
            length_of_snake += 1
            score += 10

            # Увеличение уровня и скорости
            if score % 30 == 0:
                level += 1
                SNAKE_SPEED += 2

        # Контроль скорости игры
        CLOCK.tick(SNAKE_SPEED)

    pygame.quit()


# Запуск игры
gameLoop()
