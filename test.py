# images/explosion_sprites_sheet.png
import pygame
import os

pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = (600, 600)

screen = pygame.display.set_mode(WINDOW_SIZE)

sprite_sheet = pygame.image.load(os.path.join('images', 'explosion_sprites_sheet.png')).convert_alpha()
sprite_width, sprite_height = 300, 300

sprites = []
for row in range(2):
    sprite_row = []
    for col in range(6):
        sprite_rect = pygame.Rect(col*sprite_width, row*sprite_height, sprite_width, sprite_height)
        sprite = sprite_sheet.subsurface(sprite_rect)
        sprite_row.append(sprite)
    sprites.append(sprite_row)

frame = 0
max_frame = len(sprites[0]) * len(sprites[1])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))

    row = frame // len(sprites[0])
    col = frame % len(sprites[0])
    screen.blit(sprites[row][col], (0, 0))

    frame += 1
    if frame == max_frame:
        frame = 0

    pygame.display.flip()
    clock.tick(15)
