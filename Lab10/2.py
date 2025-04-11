import pygame
import sys
import random
import time
import psycopg2

# ----------------------------
# 1. DATABASE CONNECTION SETUP
# ----------------------------

def create_connection():
    """
    Establish and return a connection to the PostgreSQL database.
    Adjust connection parameters as needed.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="snakescore",
            user="inkara",
            password=""
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        sys.exit(1)

def create_tables(conn):
    """
    Create 'users' and 'user_score' tables if they do not already exist.
    """
    cur = conn.cursor()
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        current_level INT DEFAULT 1
    );
    """
    create_user_score_table_query = """
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users(id),
        score INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cur.execute(create_users_table_query)
    cur.execute(create_user_score_table_query)
    conn.commit()
    cur.close()

def get_or_create_user(conn, username):
    """
    Checks if a user with the given 'username' exists in 'users' table.
    If not, creates a new user.
    Returns (user_id, current_level).
    """
    cur = conn.cursor()
    # Check if user exists
    cur.execute("SELECT id, current_level FROM users WHERE username = %s", (username,))
    row = cur.fetchone()

    if row:
        user_id, current_level = row
    else:
        # Create new user
        cur.execute(
            "INSERT INTO users (username) VALUES (%s) RETURNING id, current_level",
            (username,)
        )
        user_id, current_level = cur.fetchone()
        conn.commit()

    cur.close()
    return user_id, current_level

def update_user_level(conn, user_id, new_level):
    """
    Updates the current_level of a user in the 'users' table.
    """
    cur = conn.cursor()
    cur.execute("UPDATE users SET current_level = %s WHERE id = %s", (new_level, user_id))
    conn.commit()
    cur.close()

def save_score(conn, user_id, score):
    """
    Inserts a record into 'user_score' table with the current score.
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO user_score (user_id, score) VALUES (%s, %s)",
        (user_id, score)
    )
    conn.commit()
    cur.close()

# ----------------------------
# 2. GAME CONSTANTS & VARIABLES
# ----------------------------

# Create Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Game Window Dimensions and Settings
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
BLOCK_SIZE = 20  # Each block (snake segment/food) is 20x20

# Duration (in seconds) after which the food disappears if not eaten.
FOOD_DURATION = 10

# Font
pygame.init()
font = pygame.font.SysFont(None, 35)

# ----------------------------
# 3. HELPER FUNCTIONS
# ----------------------------

def draw_text(surface, text, color, x, y):
    """Utility function to render and draw text on the screen."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def generate_food(snake_body):
    """
    Generate a random food position ensuring:
    1. The food is not placed on the outer wall.
    2. The food does not appear on any part of the snake's body.
    
    Additionally, assign a random weight (1, 2, or 3), determine its size based on weight,
    and record the spawn time.
    """
    valid_position = False
    while not valid_position:
        # Ensure food does not appear directly on the wall
        food_x = random.randint(1, (SCREEN_WIDTH - BLOCK_SIZE * 2) // BLOCK_SIZE) * BLOCK_SIZE
        food_y = random.randint(1, (SCREEN_HEIGHT - BLOCK_SIZE * 2) // BLOCK_SIZE) * BLOCK_SIZE
        food_x += BLOCK_SIZE
        food_y += BLOCK_SIZE

        if [food_x, food_y] not in snake_body:
            valid_position = True

    weight = random.choice([1, 2, 3])
    if weight == 1:
        food_size = BLOCK_SIZE
    elif weight == 2:
        food_size = int(BLOCK_SIZE * 1.5)
    else:
        food_size = BLOCK_SIZE * 2

    spawn_time = time.time()
    return food_x, food_y, weight, spawn_time, food_size

def pause_game(screen, clock, conn, user_id, score):
    """
    Pauses the game until the user presses 'P' again.
    Also saves the current score to the database.
    """
    # Save current score
    save_score(conn, user_id, score)

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Press P again to resume
                if event.key == pygame.K_p:
                    paused = False

        screen.fill(BLACK)
        draw_text(screen, "Game Paused. Press 'P' to Resume.", WHITE, SCREEN_WIDTH/6, SCREEN_HEIGHT/3)
        pygame.display.update()
        clock.tick(5)  # Slow update rate while paused

# ----------------------------
# 4. MAIN SOLVE FUNCTION
# ----------------------------

def solve():
    # 4.1 Connect to DB and create tables
    conn = create_connection()
    create_tables(conn)

    # 4.2 Prompt for username
    username = input("Enter your username: ")

    # 4.3 Get or create user
    user_id, level = get_or_create_user(conn, username)

    # Console message for user level
    print(f"Welcome, {username}! Your current level is {level}.")

    # 4.4 Initialize Pygame Window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # 4.5 Initialize Snake Variables
    snake_head = [100, 40]
    snake_body = [
        [100, 40],
        [80, 40],
        [60, 40]
    ]
    direction = "RIGHT"
    change_to = direction
    score = 0

    # Food
    food_x, food_y, food_weight, food_spawn_time, food_size = generate_food(snake_body)

    # Base speed: increase with level
    base_speed = 3

    game_over = False

    # ----------------------------
    # 5. MAIN GAME LOOP
    # ----------------------------
    while not game_over:
        # 5.1 EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_p:
                    # Pause the game
                    pause_game(screen, clock, conn, user_id, score)

        # 5.2 UPDATE DIRECTION
        direction = change_to

        # 5.3 MOVE SNAKE HEAD
        if direction == "RIGHT":
            snake_head[0] += BLOCK_SIZE
        elif direction == "LEFT":
            snake_head[0] -= BLOCK_SIZE
        elif direction == "UP":
            snake_head[1] -= BLOCK_SIZE
        elif direction == "DOWN":
            snake_head[1] += BLOCK_SIZE

        # Insert new head
        snake_body.insert(0, list(snake_head))

        # 5.4 CHECK FOOD TIMEOUT
        if time.time() - food_spawn_time > FOOD_DURATION:
            # Regenerate if food expired
            food_x, food_y, food_weight, food_spawn_time, food_size = generate_food(snake_body)

        # 5.5 CHECK IF SNAKE EATS FOOD
        if snake_head[0] == food_x and snake_head[1] == food_y:
            score += food_weight
            # Increase level for every 3 foods eaten
            if score % 3 == 0:
                level += 1
                # Update user level in DB
                update_user_level(conn, user_id, level)
            food_x, food_y, food_weight, food_spawn_time, food_size = generate_food(snake_body)
        else:
            # Remove tail if no food eaten
            snake_body.pop()

        # 5.6 COLLISION DETECTION (BORDER)
        if (snake_head[0] < 0 or snake_head[0] >= SCREEN_WIDTH or
            snake_head[1] < 0 or snake_head[1] >= SCREEN_HEIGHT):
            game_over = True

        # 5.7 COLLISION DETECTION (SELF)
        for segment in snake_body[1:]:
            if snake_head[0] == segment[0] and snake_head[1] == segment[1]:
                game_over = True

        # 5.8 RENDER
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, RED, (food_x, food_y, food_size, food_size))
        # Draw snake
        for segment in snake_body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        # Display score & level
        draw_text(screen, f"Score: {score}", WHITE, 10, 10)
        draw_text(screen, f"Level: {level}", WHITE, SCREEN_WIDTH - 150, 10)

        pygame.display.update()

        # 5.9 CONTROL SPEED
        # Speed is base_speed + something that depends on level
        clock.tick(base_speed + (level - 1) * 2)

    # ----------------------------
    # 6. GAME OVER SCREEN
    # ----------------------------
    # Once game is over, let's save the final score one more time
    save_score(conn, user_id, score)

    screen.fill(BLUE)
    draw_text(screen, "Game Over! Score: " + str(score), WHITE, SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Direct run of game
if __name__ == "__main__":
    solve()