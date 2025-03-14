import pygame
import os
pygame.init()


WIDTH , HEIGHT = 500 , 500 
screen=pygame.display.set_mode((WIDTH , HEIGHT ))
pygame.display.set_caption("music_player")

playlist = [file for file in os.listdir() if file.endswith(".mp3")]
current_track = 0

print(playlist)

pygame.mixer.music.load(playlist[current_track])
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

font = pygame.font.Font(None, 24)

def draw():
    screen.fill((255,192,203))
    track_name=font.render(f"now playing -> {playlist[current_track]}", False, (255, 255, 255))
    screen.blit(track_name,(20,10))
    pygame.display.flip()

running = True
while running:
    draw()
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.mixer.music.unpause()
            elif event.key == pygame.K_SPACE:
                pygame.mixer.music.pause()
            elif event.key == pygame.K_LEFT:
                current_track = (current_track - 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
            elif event.key == pygame.K_RIGHT:
                current_track = (current_track + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()

            print(playlist[current_track])


            
