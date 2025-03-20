import pygame, random, time

pygame.init()

WIDTH , HEIGHT = 600 , 400
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
BLOCK_SIZE = 20

screen=pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("snake_game")
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
clock = pygame.time.Clock()

def generate_food(snake_body):
    valid_position = False
    while not valid_position:
        # Ensure food does not fall on the wall by choosing coordinates with a margin.
        food_x = random.randint(1, (WIDTH - BLOCK_SIZE*2) // BLOCK_SIZE) * BLOCK_SIZE
        food_y = random.randint(1, (HEIGHT - BLOCK_SIZE*2) // BLOCK_SIZE) * BLOCK_SIZE
        # Shift the food so it is not flush with the wall.
        food_x += BLOCK_SIZE
        food_y += BLOCK_SIZE
        # Check that the generated position is not on the snake's body.
        if [food_x, food_y] not in snake_body:
            valid_position = True
    return food_x, food_y

snake_head = [100, 40]
snake_body = [
    [100, 40],
    [80, 40],
    [60, 40],
    
]

direction = "DOWN"
change_to = direction

food_x, food_y = generate_food(snake_body)
score = 0
level = 1



running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"

    direction = change_to

    # Update Snake's Head Position Based on the Direction
    if direction == "RIGHT":
        snake_head[0] += BLOCK_SIZE
    elif direction == "LEFT":
        snake_head[0] -= BLOCK_SIZE
    elif direction == "UP":
        snake_head[1] -= BLOCK_SIZE
    elif direction == "DOWN":
        snake_head[1] += BLOCK_SIZE

    # Insert the new head position into the snake body list.
    snake_body.insert(0, list(snake_head))


    # Check if Snake has Eaten the Food
    if snake_head[0] == food_x and snake_head[1] == food_y:
        score += 1  # Increase score by 1
        # Increase level for every 3 foods eaten.
        if score % 3 == 0:
            level += 1
        # Generate a new food position ensuring it does not conflict with the snake or walls.
        food_x, food_y = generate_food(snake_body)
    else:
        # Remove the tail segment if food not eaten (this moves the snake forward).
        snake_body.pop()

    # Border Collision: Check if the snake hits the wall.
    if (snake_head[0] < 0 or snake_head[0] >= WIDTH or
        snake_head[1] < 0 or snake_head[1] >= HEIGHT):
        running = False

    # Self Collision: Check if the snake collides with its own body.
    for segment in snake_body[1:]:
        if snake_head[0] == segment[0] and snake_head[1] == segment[1]:
            running = False

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, pygame.Rect(food_x, food_y, BLOCK_SIZE, BLOCK_SIZE))

    for segment in snake_body:
        pygame.draw.rect(screen, BLUE, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    scores = font_small.render(str(score), True, BLACK)
    level_c = font_small.render(str(level), True, BLACK)
    screen.blit(scores, (10,10))
    screen.blit(level_c, (550,10))

    pygame.display.flip()
    clock.tick(4 + (level - 1) * 1.1)

screen.fill(RED)
screen.blit(font.render("Game Over", True, BLACK), (120,150))
screen.blit(font_small.render(f"Score: {score}", True, BLACK), (250,230))
pygame.display.update()
time.sleep(3)
pygame.quit()