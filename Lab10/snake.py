import psycopg2
import pygame
import random
import time
import sys
from pygame import mixer

# НАСТРОЙКИ ИГРЫ
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BACKGROUND = (40, 40, 40)

# Размеры
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
FONT_SIZE = 24
TITLE_SIZE = 48

# Скорости для разных уровней
LEVEL_SPEEDS = {1: 8, 2: 12, 3: 16, 4: 20, 5: 25, 6:35}

# SQL ЗАПРОСЫ
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    current_level INTEGER DEFAULT 1,
    highest_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_SCORES_TABLE = """
CREATE TABLE IF NOT EXISTS user_scores (
    score_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    score INTEGER NOT NULL,
    level INTEGER NOT NULL,
    snake_data TEXT NOT NULL,
    food_data TEXT NOT NULL,
    direction VARCHAR(10) NOT NULL,
    walls_data TEXT,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_USER = """
INSERT INTO users (username) VALUES (%s) 
RETURNING user_id, current_level, highest_score
"""

GET_USER = """
SELECT user_id, current_level, highest_score FROM users WHERE username = %s
"""

UPDATE_LEVEL = """
UPDATE users SET current_level = %s, highest_score = %s WHERE user_id = %s
"""

INSERT_GAME_STATE = """
INSERT INTO user_scores 
(user_id, score, level, snake_data, food_data, direction, walls_data)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

GET_LAST_GAME = """
SELECT score, level, snake_data, food_data, direction, walls_data 
FROM user_scores 
WHERE user_id = %s 
ORDER BY saved_at DESC 
LIMIT 1
"""

#  ИГРОВЫЕ ФУНКЦИИ 
def init_game():
    """Инициализация pygame и окна игры"""
    pygame.init()
    mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка Pro - Сохранение прогресса")
    return screen

def load_sounds():
    """Загрузка звуковых эффектов"""
    sounds = {
        'eat': mixer.Sound('eat.wav'),
        'level_up': mixer.Sound('level_up.wav'),
        'game_over': mixer.Sound('game_over.wav')
    }
    # Установка громкости
    for sound in sounds.values():
        sound.set_volume(0.5)
    return sounds

def generate_food(snake_body, walls):
    """Генерация еды в случайном месте"""
    while True:
        food_x = random.randint(1, (WIDTH - BLOCK_SIZE*2) // BLOCK_SIZE) * BLOCK_SIZE
        food_y = random.randint(1, (HEIGHT - BLOCK_SIZE*2) // BLOCK_SIZE) * BLOCK_SIZE
        food_x += BLOCK_SIZE
        food_y += BLOCK_SIZE
        
        # Проверяем, чтобы еда не появилась на змейке или стене
        if [food_x, food_y] not in snake_body and [food_x, food_y] not in walls:
            return food_x, food_y

def generate_walls(level):
    """Генерация стен для разных уровней"""
    walls = []
    
    if level == 1:
        # Простые границы
        for x in range(0, WIDTH, BLOCK_SIZE):
            walls.append([x, 0])
            walls.append([x, HEIGHT - BLOCK_SIZE])
        for y in range(0, HEIGHT, BLOCK_SIZE):
            walls.append([0, y])
            walls.append([WIDTH - BLOCK_SIZE, y])
    
    elif level == 2:
        # Крест посередине
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        for i in range(-9, 10):
            walls.append([center_x + i*BLOCK_SIZE, center_y])
            walls.append([center_x, center_y + i*BLOCK_SIZE])
    
    elif level == 3:
        # Квадраты по углам
        for i in range(5):
            for j in range(5):
                walls.append([BLOCK_SIZE*(1+i), BLOCK_SIZE*(1+j)])
                walls.append([WIDTH-BLOCK_SIZE*(2+i), BLOCK_SIZE*(1+j)])
                walls.append([BLOCK_SIZE*(1+i), HEIGHT-BLOCK_SIZE*(2+j)])
                walls.append([WIDTH-BLOCK_SIZE*(2+i), HEIGHT-BLOCK_SIZE*(2+j)])
    
    elif level >= 4:
        # Лабиринт
        for x in range(BLOCK_SIZE*5, WIDTH-BLOCK_SIZE*5, BLOCK_SIZE):
            walls.append([x, HEIGHT//3])
            walls.append([x, 2*HEIGHT//3])
    if level == 5:
        # Простые границы (ИЗЗА СКОРОСТИ МЕГА СЛОЖНО)
        for x in range(0, WIDTH, BLOCK_SIZE):
            walls.append([x, 0])
            walls.append([x, HEIGHT - BLOCK_SIZE])
        for y in range(0, HEIGHT, BLOCK_SIZE):
            walls.append([0, y])
            walls.append([WIDTH - BLOCK_SIZE, y])
    return walls

def draw_objects(screen, snake_body, food, walls, score, level, highest_score):
    """Отрисовка всех игровых объектов"""
    # Фон
    screen.fill(BACKGROUND)
    
    # Отрисовка стен
    for wall in walls:
        pygame.draw.rect(screen, PURPLE, 
                        pygame.Rect(wall[0], wall[1], BLOCK_SIZE, BLOCK_SIZE))
    
    # Отрисовка змейки (градиент от головы к хвосту)
    for i, segment in enumerate(snake_body):
        # Цвет меняется от синего (голова) к зеленому (хвост)
        color = (
            int(0 + (0 - 0) * i / len(snake_body)),
            int(0 + (255 - 0) * i / len(snake_body)),
            int(255 + (0 - 255) * i / len(snake_body))
        )
        pygame.draw.rect(screen, color, 
                        pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
    
    # Отрисовка еды (анимированная)
    pulse = int((pygame.time.get_ticks() % 1000) / 1000 * 5 + 5)
    pygame.draw.circle(screen, RED, 
                      (food[0] + BLOCK_SIZE//2, food[1] + BLOCK_SIZE//2), 
                      pulse)
    
    # Отображение информации
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    title_font = pygame.font.SysFont("Arial", TITLE_SIZE, bold=True)
    
    # Заголовок
    title = title_font.render("Змейка Pro", True, YELLOW)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))
    
    # Статистика
    score_text = font.render(f"Счет: {score}", True, WHITE)
    level_text = font.render(f"Уровень: {level}", True, WHITE)
    highest_text = font.render(f"Рекорд: {highest_score}", True, WHITE)
    
    screen.blit(score_text, (20, 70))
    screen.blit(level_text, (20, 100))
    screen.blit(highest_text, (20, 130))
    
    # Подсказки
    hints = font.render("P - Пауза/Сохранение | ESC - Выход", True, WHITE)
    screen.blit(hints, (WIDTH//2 - hints.get_width()//2, HEIGHT - 30))

def game_over_screen(screen, score, highest_score):
    """Экран завершения игры"""
    # Затемнение
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Текст
    font_large = pygame.font.SysFont("Arial", 72, bold=True)
    font_medium = pygame.font.SysFont("Arial", 36)
    font_small = pygame.font.SysFont("Arial", 24)
    
    game_over_text = font_large.render("Игра Окончена!", True, RED)
    score_text = font_medium.render(f"Ваш счет: {score}", True, WHITE)
    
    if score > highest_score:
        record_text = font_medium.render("Новый рекорд!", True, YELLOW)
    else:
        record_text = font_medium.render(f"Рекорд: {highest_score}", True, WHITE)
    
    continue_text = font_small.render("Нажмите любую клавишу для выхода", True, WHITE)
    
    # Позиционирование
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(record_text, (WIDTH//2 - record_text.get_width()//2, HEIGHT//2 + 50))
    screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 120))
    
    pygame.display.update()

def pause_screen(screen):
    """Экран паузы"""
    # Затемнение
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Текст
    font_large = pygame.font.SysFont("Arial", 72, bold=True)
    font_small = pygame.font.SysFont("Arial", 24)
    
    pause_text = font_large.render("ПАУЗА", True, WHITE)
    hint_text = font_small.render("P - Продолжить | ESC - Выход", True, WHITE)
    save_text = font_small.render("Игра сохранена автоматически", True, GREEN)
    
    # Позиционирование
    screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, HEIGHT//2 + 20))
    screen.blit(save_text, (WIDTH//2 - save_text.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.update()

#  РАБОТА С БАЗОЙ ДАННЫХ 
def create_connection():
    """Создание подключения к PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='snake_game_db',
            user='inkara',
            password='',
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        sys.exit(1)

def setup_database(conn):
    """Создание таблиц в базе данных"""
    try:
        cur = conn.cursor()
        cur.execute(CREATE_USERS_TABLE)
        cur.execute(CREATE_SCORES_TABLE)
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка создания таблиц: {e}")
        conn.close()
        sys.exit(1)

def handle_user(conn, username):
    """Обработка пользователя (поиск или создание нового)"""
    try:
        cur = conn.cursor()
        cur.execute(GET_USER, (username,))
        user = cur.fetchone()
        
        if user:
            print(f"\nДобро пожаловать назад, {username}!")
            print(f"Текущий уровень: {user[1]}")
            print(f"Ваш рекорд: {user[2]}")
            return user[0], user[1], user[2]  # user_id, current_level, highest_score
        else:
            cur.execute(INSERT_USER, (username,))
            user_id, level, highest = cur.fetchone()
            conn.commit()
            print(f"\nНовый пользователь создан: {username}")
            print("Начинаем с 1 уровня.")
            return user_id, level, highest
    except psycopg2.Error as e:
        print(f"Ошибка работы с пользователем: {e}")
        conn.close()
        sys.exit(1)

def save_game(conn, user_id, score, level, snake_body, food, direction, walls):
    """Сохранение текущего состояния игры"""
    try:
        snake_str = ",".join([f"{x},{y}" for x, y in snake_body])
        food_str = f"{food[0]},{food[1]}"
        walls_str = ",".join([f"{x},{y}" for x, y in walls]) if walls else ""
        
        cur = conn.cursor()
        cur.execute(INSERT_GAME_STATE, 
                   (user_id, score, level, snake_str, food_str, direction, walls_str))
        conn.commit()
        cur.close()
        return True
    except psycopg2.Error as e:
        print(f"Ошибка сохранения игры: {e}")
        return False

def load_game(conn, user_id):
    """Загрузка последнего сохраненного состояния игры"""
    try:
        cur = conn.cursor()
        cur.execute(GET_LAST_GAME, (user_id,))
        state = cur.fetchone()
        cur.close()
        
        if state:
            score, level, snake_str, food_str, direction, walls_str = state
            snake_body = [[int(x), int(y)] for coord in snake_str.split(",") for x, y in [coord.split(",")]]
            food = [int(x) for x in food_str.split(",")]
            walls = [[int(x), int(y)] for coord in walls_str.split(",") for x, y in [coord.split(",")]] if walls_str else []
            return score, level, snake_body, food, direction, walls
        return None
    except psycopg2.Error as e:
        print(f"Ошибка загрузки игры: {e}")
        return None

def update_user_progress(conn, user_id, level, score):
    """Обновление прогресса пользователя"""
    try:
        cur = conn.cursor()
        cur.execute(UPDATE_LEVEL, (level, score, user_id))
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print(f"Ошибка обновления прогресса: {e}")

#  ОСНОВНАЯ ИГРА 
def main():
    """Главная функция игры"""
    # Инициализация
    conn = create_connection()
    setup_database(conn)
    
    # Ввод имени пользователя
    print("\n" + "="*50)
    print(" " * 15 + "ЗМЕЙКА PRO")
    print("="*50)
    username = input("\nВведите ваше имя: ").strip()
    user_id, current_level, highest_score = handle_user(conn, username)
    
    # Инициализация игры
    screen = init_game()
    try:
        sounds = load_sounds()
    except:
        sounds = None
        print("Звуковые эффекты не загружены")
    
    clock = pygame.time.Clock()
    
    # Загрузка сохраненной игры или начало новой
    saved_state = load_game(conn, user_id)
    if saved_state and input("\nЗагрузить сохраненную игру? (y/n): ").lower() == 'y':
        score, level, snake_body, food, direction, walls = saved_state
        snake_head = snake_body[0]
        print(f"\nЗагружена игра: Уровень {level}, Счет {score}")
    else:
        # Начальные параметры
        snake_head = [WIDTH//2 - 10*BLOCK_SIZE, HEIGHT//2 - 10*BLOCK_SIZE]
        snake_body = [list(snake_head), 
                     [snake_head[0]-BLOCK_SIZE, snake_head[1]], 
                     [snake_head[0]-2*BLOCK_SIZE, snake_head[1]]]
        direction = "RIGHT"
        score = 0
        level = current_level
        walls = generate_walls(level)
        food = generate_food(snake_body, walls)
        print("\nНовая игра начата!")
    
    # Основной игровой цикл
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        # Сохраняем игру при паузе
                        if save_game(conn, user_id, score, level, snake_body, food, direction, walls):
                            print("\nИгра сохранена!")
                        pause_screen(screen)
                    else:
                        print("\nИгра продолжается!")
                elif not paused:
                    # Управление змейкой
                    if event.key == pygame.K_LEFT and direction != "RIGHT":
                        direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and direction != "LEFT":
                        direction = "RIGHT"
                    elif event.key == pygame.K_UP and direction != "DOWN":
                        direction = "UP"
                    elif event.key == pygame.K_DOWN and direction != "UP":
                        direction = "DOWN"
        
        if paused:
            clock.tick(5)
            continue
        
        # Движение змейки
        if direction == "RIGHT":
            snake_head[0] += BLOCK_SIZE
        elif direction == "LEFT":
            snake_head[0] -= BLOCK_SIZE
        elif direction == "UP":
            snake_head[1] -= BLOCK_SIZE
        elif direction == "DOWN":
            snake_head[1] += BLOCK_SIZE
        
        snake_body.insert(0, list(snake_head))
        
        # Проверка на съедение еды
        if snake_head[0] == food[0] and snake_head[1] == food[1]:
            if sounds:
                sounds['eat'].play()
            score += 1
            if score > highest_score:
                highest_score = score
            
            # Повышение уровня каждые 5 очков
            if score % 5 == 0:  
                level += 1
                if sounds:
                    sounds['level_up'].play()
                walls = generate_walls(level)
                update_user_progress(conn, user_id, level, highest_score)
                print(f"\nУровень повышен до {level}!")
            
            food = generate_food(snake_body, walls)
        else:
            snake_body.pop()
        
        # Проверка столкновений
        if (snake_head[0] < 0 or snake_head[0] >= WIDTH or
            snake_head[1] < 0 or snake_head[1] >= HEIGHT or
            any(snake_head == segment for segment in snake_body[1:]) or
            snake_head in walls):
            
            if sounds:
                time.sleep(0.1)
                sounds['game_over'].play()
            update_user_progress(conn, user_id, level, highest_score)
            game_over_screen(screen, score, highest_score)
            # Ждем нажатия любой клавиши
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        waiting = False
                        running = False
            break
        
        # Отрисовка
        draw_objects(screen, snake_body, food, walls, score, level, highest_score)
        pygame.display.update()
        clock.tick(LEVEL_SPEEDS.get(level, 10))
    
    # Завершение игры
    pygame.quit()
    conn.close()
    print("\n" + "="*50)
    print(f"Игра завершена! Ваш счет: {score}")
    print(f"Ваш рекорд: {highest_score}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()