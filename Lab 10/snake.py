import pygame
import random
import psycopg2

# Настройки Pygame
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS_BASE = 4
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Подключение к базе данных
def get_connection():
    return psycopg2.connect(dbname='snake', user='postgres', password='tomi2007', host='localhost', port=5432)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(100) PRIMARY KEY
    );
    CREATE TABLE IF NOT EXISTS scores (
        username VARCHAR(100) REFERENCES users(username),
        score INTEGER,
        level INTEGER
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_user_level(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(level) FROM scores WHERE username = %s;", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row[0] else 1

def save_score(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING;", (username,))
    cur.execute("INSERT INTO scores (username, score, level) VALUES (%s, %s, %s);", (username, score, level))
    conn.commit()
    cur.close()
    conn.close()

# Игровые переменные
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont(None, 24)

# Ввод имени игрока через графический интерфейс
def get_username():
    input_active = True
    user_input = ''
    while input_active:
        screen.fill(BLACK)
        text_surface = font.render("Enter your username:", True, WHITE)
        screen.blit(text_surface, (WIDTH // 4, HEIGHT // 4))
        
        input_surface = font.render(user_input, True, WHITE)
        screen.blit(input_surface, (WIDTH // 4, HEIGHT // 4 + 40))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        
        pygame.display.flip()
    
    return user_input

# Генерация еды с таймером
def generate_food():
    """Создает случайную еду с разным весом и таймером удаления."""
    x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
    y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
    weight = random.randint(1, 5)  # Вес еды (1-5 очков)
    food.append((x, y, weight))
    food_timer[(x, y)] = pygame.time.get_ticks() + random.randint(3000, 6000)  # Таймер 3-7 сек.

# Инициализация игры
username = get_username()
init_db()
level = get_user_level(username)
speed = FPS_BASE + level
score = 0
paused = False

snake = [(WIDTH // 2, HEIGHT // 2)]
direction = RIGHT
food = []
food_timer = {}

generate_food()

running = True
clock = pygame.time.Clock()

# Главный игровой цикл
while running:
    if not paused:
        screen.fill(BLACK)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score(username, score, level)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != DOWN:
                direction = UP
            elif event.key == pygame.K_DOWN and direction != UP:
                direction = DOWN
            elif event.key == pygame.K_LEFT and direction != RIGHT:
                direction = LEFT
            elif event.key == pygame.K_RIGHT and direction != LEFT:
                direction = RIGHT
            elif event.key == pygame.K_p:
                paused = not paused
                if paused:
                    save_score(username, score, level)

    if not paused:
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0] * CELL_SIZE, head_y + direction[1] * CELL_SIZE)

        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT or new_head in snake:
            save_score(username, score, level)
            running = False

        snake.insert(0, new_head)

        # Проверка съеденной еды
        ate_food = None
        for f in food:
            if new_head[:2] == f[:2]:
                ate_food = f
                break

        if ate_food:
            score += ate_food[2]
            food.remove(ate_food)
            del food_timer[(ate_food[0], ate_food[1])]
            generate_food()  # Создаём новую еду
            if score // 10 + 1 > level:
                level += 1
                speed = FPS_BASE + level
        else:
            snake.pop()

        # Проверка таймеров еды
        current_time = pygame.time.get_ticks()
        food = [f for f in food if food_timer.get((f[0], f[1]), current_time) > current_time]
        food_timer = {pos: t for pos, t in food_timer.items() if t > current_time}

        # Отрисовка змейки
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

        # Отрисовка еды
        for f in food:
            pygame.draw.rect(screen, RED, (f[0], f[1], CELL_SIZE, CELL_SIZE))
            weight_text = font.render(str(f[2]), True, BLUE)
            screen.blit(weight_text, (f[0] + 5, f[1] + 2))

        # Отображение информации
        info_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        screen.blit(info_text, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

pygame.quit()