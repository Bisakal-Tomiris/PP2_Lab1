import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# Загрузка фоновой музыки
pygame.mixer.music.load("background.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Установка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Размеры окна
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# Загрузка фонового изображения
background = pygame.image.load("AnimatedStreet.png")

# Глобальные переменные игры
SPEED = 5
SCORE = 0
COINS = 0
COIN_THRESHOLD = 10  # Увеличиваем скорость каждые 10 монет

# Таймер для постепенного увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Звук при столкновении
crash_sound = pygame.mixer.Sound('crash.wav')

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Враг
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

# Монета с весом (ценностью)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 3])  # Coin value
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 100))

    def move(self):
        # Обновляем вес и позицию монеты
        self.weight = random.choice([1, 2, 3])
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 100))

# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.top > 0 and pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)

# Обработка столкновения с врагом
def handle_crash():
    pygame.mixer.Sound.play(crash_sound)
    time.sleep(0.5)
    DISPLAYSURF.fill(RED)
    DISPLAYSURF.blit(game_over, (30, 250))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

background_y = 0

running = True
while running:
    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == INC_SPEED:
            SPEED += 0.1  # Постепенно увеличиваем скорость

    # Проверка на столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        handle_crash()

    # Анимация движения фона
    background_y = (background_y + SPEED) % background.get_height()
    DISPLAYSURF.blit(background, (0, background_y))
    DISPLAYSURF.blit(background, (0, background_y - background.get_height()))

    # Отображение счета и монет
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (250, 10))

    # Движение игрока и врага
    P1.move()
    E1.move()

    # Отрисовка всех объектов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Проверка на сбор монеты
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += C1.weight  # Добавляем "вес" монеты к счетчику
        if COINS % COIN_THRESHOLD == 0:
            SPEED += 1  # Увеличиваем скорость при достижении порога
        C1.move()  # Перемещаем монету в случайное место

    pygame.display.update()
    FramePerSec.tick(FPS)
   
