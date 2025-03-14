import pygame
  
pygame.init()

WIDTH ,HEIGHT = 500 , 500
screen=pygame.display.set_mode((WIDTH ,HEIGHT))
pygame.display.set_caption("red_ball")

ball_radius=25
ball_color=(255,0,0)
ball_step=20
ball_x=WIDTH//2
ball_y=HEIGHT//2

running=True
while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and ball_y - ball_radius - ball_step>0:
                ball_y -= ball_step
            elif event.key == pygame.K_DOWN and ball_y + ball_radius + ball_step<HEIGHT:
                ball_y += ball_step
            elif event.key == pygame.K_LEFT and ball_x - ball_radius - ball_step>0:
                ball_x -= ball_step
            elif event.key == pygame.K_RIGHT and ball_x + ball_radius + ball_step<WIDTH:
                ball_x += ball_step
                
    pygame.draw.circle(screen ,ball_color,(ball_x,ball_y),ball_radius)
    pygame.display.flip()