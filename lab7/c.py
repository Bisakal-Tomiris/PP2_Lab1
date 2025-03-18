import pygame
import sys

# Инициализация Pygame
pygame.init()

# Задаём размеры окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Движение красного мяча")

# Начальные координаты мяча (центр окна)
x = screen_width // 2
y = screen_height // 2
radius = 25       # Радиус мяча (отсюда размер 50 x 50)
speed = 20        # Шаг перемещения при нажатии клавиши

clock = pygame.time.Clock()

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Обработка нажатия клавиш
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Проверяем, что мяч не выйдет за верхнюю границу
                if y - radius - speed >= 0:
                    y -= speed
            elif event.key == pygame.K_DOWN:
                # Проверяем нижнюю границу
                if y + radius + speed <= screen_height:
                    y += speed
            elif event.key == pygame.K_LEFT:
                # Проверяем левую границу
                if x - radius - speed >= 0:
                    x -= speed
            elif event.key == pygame.K_RIGHT:
                # Проверяем правую границу
                if x + radius + speed <= screen_width:
                    x += speed

    # Заполнение экрана белым цветом
    screen.fill((255, 255, 255))
    
    # Отрисовка красного мяча
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
    
    # Обновление дисплея
    pygame.display.flip()
    
    # Ограничение FPS до 60
    clock.tick(60)
