import pygame
import math 
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 1300,1024
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey_Clock")

clock_face = pygame.image.load("c:/Users/ASUS/Downloads/mickey_clock.png")
clock_face = pygame.transform.scale(clock_face, (WIDTH, HEIGHT))
minute_hand = pygame.image.load("c:/Users/ASUS/Downloads/right.png")
second_hand = pygame.image.load("c:/Users/ASUS/Downloads/left.png")

clock_center = (WIDTH // 2, HEIGHT // 2)

running=True
while running:
    screen.fill((255, 255, 255))  
    screen.blit(clock_face, (0, 0))  

    now = datetime.now()
    seconds = now.second
    minutes = now.minute

    second_angle = -seconds * 6  
    minute_angle = -minutes * 6  

    rotated_minute = pygame.transform.rotate(minute_hand, minute_angle)
    rotated_second = pygame.transform.rotate(second_hand, second_angle)

    min_rect = rotated_minute.get_rect(center=clock_center)
    sec_rect = rotated_second.get_rect(center=clock_center)
    
    screen.blit(rotated_minute, min_rect.topleft)
    screen.blit(rotated_second, sec_rect.topleft)
    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    pygame.display.flip()

pygame.quit()