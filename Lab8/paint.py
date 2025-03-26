import pygame
import sys

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
drawing = True
last_pos = (0, 0)
shape_mode = "pen"  # "pen", "rectangle", "circle", "eraser"
brush_size = 5

# Функция для рисования линии
def draw_line(start_pos, end_pos, color, size):
    pygame.draw.line(screen, color, start_pos, end_pos, size)

# Функция для рисования прямоугольника
def draw_rectangle(start_pos, end_pos, color, size):
    pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), size)

# Функция для рисования круга
def draw_circle(start_pos, end_pos, color, size):
    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
    pygame.draw.circle(screen, color, start_pos, radius, size)

# Функция для рисования ластика
def erase(start_pos, end_pos, size):
    pygame.draw.rect(screen, WHITE, (start_pos[0], start_pos[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))

# Главный цикл
screen.fill(WHITE) 
while True:
    # Очистка экрана
     # Очистка экрана белым цветом перед каждым циклом рисования

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Обработка нажатия клавиш для выбора инструмента
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_color = BLACK  # Черный цвет
            elif event.key == pygame.K_2:
                current_color = RED  # Красный цвет
            elif event.key == pygame.K_3:
                current_color = GREEN  # Зеленый цвет
            elif event.key == pygame.K_4:
                current_color = BLUE  # Синий цвет
            elif event.key == pygame.K_5:
                current_color = YELLOW  # Желтый цвет

            # Выбор инструмента
            if event.key == pygame.K_p:  # Ручка
                shape_mode = "pen"
            elif event.key == pygame.K_r:  # Прямоугольник
                shape_mode = "rectangle"
            elif event.key == pygame.K_c:  # Круг
                shape_mode = "circle"
            elif event.key == pygame.K_e:  # Ластик
                shape_mode = "eraser"
         
        # Обработка нажатий на мышь
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = event.pos
        
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos
                if shape_mode == "pen":
                    draw_line(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "rectangle":
                    draw_rectangle(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "circle":
                    draw_circle(last_pos, current_pos, current_color, brush_size)
                elif shape_mode == "eraser":
                    erase(last_pos, current_pos, brush_size)
                last_pos = current_pos

    # Отображение текущего цвета и инструмента
    font = pygame.font.SysFont("Arial", 20)
    tool_text = font.render(f"Tool: {shape_mode.capitalize()}", True, BLACK)
    color_text = font.render(f"Color: {current_color}", True, BLACK)
    screen.blit(tool_text, (10, HEIGHT - 40))
    screen.blit(color_text, (10, HEIGHT - 20))

    # Обновление экрана
    pygame.display.update()
