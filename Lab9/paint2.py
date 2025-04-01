import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Начальные настройки
current_color = BLACK
drawing = False
last_pos = (0, 0)
shape_mode = "pen"
brush_size = 5

# Очистка экрана
screen.fill(WHITE)

# ——— Функции рисования фигур ———
def draw_line(start_pos, end_pos, color, size):
    pygame.draw.line(screen, color, start_pos, end_pos, size)

def draw_rectangle(start_pos, end_pos, color, size):
    pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), size)

def draw_circle(start_pos, end_pos, color, size):
    radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
    pygame.draw.circle(screen, color, start_pos, radius, size)

def draw_square(start_pos, end_pos, color, size):
    side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
    pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], side, side), size)

def draw_right_triangle(start_pos, end_pos, color, size):
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [(x1, y1), (x2, y2), (x1, y2)]
    pygame.draw.polygon(screen, color, points, size)

def draw_equilateral_triangle(start_pos, end_pos, color, size):
    x1, y1 = start_pos
    x2 = x1 + abs(end_pos[0] - x1)
    side = x2 - x1
    height = side * math.sqrt(3) / 2
    points = [
        (x1, y1),
        (x1 + side, y1),
        (x1 + side / 2, y1 - height)
    ]
    pygame.draw.polygon(screen, color, points, size)

def draw_rhombus(start_pos, end_pos, color, size):
    x1, y1 = start_pos
    x2, y2 = end_pos
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    dx = abs(x2 - x1) / 2
    dy = abs(y2 - y1) / 2
    points = [
        (mid_x, y1),
        (x2, mid_y),
        (mid_x, y2),
        (x1, mid_y)
    ]
    pygame.draw.polygon(screen, color, points, size)

def erase(start_pos, end_pos, size):
    pygame.draw.rect(screen, WHITE, (start_pos[0], start_pos[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))

# ——— Главный цикл ———
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Управление цветами
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_color = BLACK
                elif event.key == pygame.K_2:
                    current_color = RED
                elif event.key == pygame.K_3:
                    current_color = GREEN
                elif event.key == pygame.K_4:
                    current_color = BLUE
                elif event.key == pygame.K_5:
                    current_color = YELLOW

                # Выбор фигуры
                if event.key == pygame.K_p:
                    shape_mode = "pen"
                elif event.key == pygame.K_r:
                    shape_mode = "rectangle"
                elif event.key == pygame.K_c:
                    shape_mode = "circle"
                elif event.key == pygame.K_s:
                    shape_mode = "square"
                elif event.key == pygame.K_t:
                    shape_mode = "right_triangle"
                elif event.key == pygame.K_q:
                    shape_mode = "equilateral_triangle"
                elif event.key == pygame.K_d:
                    shape_mode = "rhombus"
                elif event.key == pygame.K_e:
                    shape_mode = "eraser"

            # Управление мышкой
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                last_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None

            elif event.type == pygame.MOUSEMOTION and drawing:
                current_pos = event.pos
                if shape_mode == "pen":
                    draw_line(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "rectangle":
                    draw_rectangle(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "circle":
                    draw_circle(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "square":
                    draw_square(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "right_triangle":
                    draw_right_triangle(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "equilateral_triangle":
                    draw_equilateral_triangle(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "rhombus":
                    draw_rhombus(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "eraser":
                    erase(last_pos, current_pos, brush_size)
                last_pos = current_pos

        # Подпись инструмента и цвета
        font = pygame.font.SysFont("Arial", 20)
        tool_text = font.render(f"Tool: {shape_mode.capitalize()}", True, BLACK)
        color_text = font.render(f"Color: {current_color}", True, BLACK)
        screen.blit(tool_text, (10, HEIGHT - 40))
        screen.blit(color_text, (10, HEIGHT - 20))

        pygame.display.update()

except Exception as e:
    print("Ошибка:", e)
    pygame.quit()
    sys.exit()
