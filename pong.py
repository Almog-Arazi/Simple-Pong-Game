import pygame
import requests
from io import BytesIO
import random


pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pong')
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 48)

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 100
PLAYER_VELOCITY = 10
BALL_RADIUS = 10
BALL_VELOCITY_X = 5
BALL_VELOCITY_Y = 5
SCORE_PLAYER = 0
SCORE_CPU = 0
player = pygame.Rect(50, WINDOW_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
cpu = pygame.Rect(WINDOW_WIDTH - 50 - PLAYER_WIDTH, WINDOW_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
ball = pygame.Rect(WINDOW_WIDTH // 2 - BALL_RADIUS, WINDOW_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)


music_data = "music.ogg"
pygame.mixer.music.load(music_data)
pygame.mixer.music.play(-1)

bg_image = pygame.image.load("background.jpeg").convert()
bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

ball_image = pygame.image.load("ball2.png").convert_alpha()
ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))

sound_hit = pygame.mixer.Sound("hit.ogg")
sound_hit.set_volume(0.9)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move_ip(0, -PLAYER_VELOCITY)
    if keys[pygame.K_s]:
        player.move_ip(0, PLAYER_VELOCITY)

    cpu_speed = random.randint(1, PLAYER_VELOCITY)
    if ball.centery > cpu.top:
        cpu.move_ip(0, cpu_speed)
    elif ball.centery < cpu.bottom:
        cpu.move_ip(0, -cpu_speed)

    ball.move_ip(BALL_VELOCITY_X, BALL_VELOCITY_Y)

    if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
        BALL_VELOCITY_Y = -BALL_VELOCITY_Y
    if ball.left <= 0:
        SCORE_CPU += 1
        ball.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        BALL_VELOCITY_X = -BALL_VELOCITY_X
        sound_hit.play()
    if ball.right >= WINDOW_WIDTH:
        SCORE_PLAYER += 1
        ball.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        BALL_VELOCITY_X = -BALL_VELOCITY_X
        sound_hit.play()

    if ball.colliderect(player) or ball.colliderect(cpu):
        BALL_VELOCITY_X = -BALL_VELOCITY_X
        sound_hit.play()

    GAME_WINDOW.blit(bg_image, (0, 0))
    pygame.draw.rect(GAME_WINDOW, pygame.Color('white'), player)
    pygame.draw.rect(GAME_WINDOW, pygame.Color('white'), cpu)
    GAME_WINDOW.blit(ball_image, ball)
    score_text = FONT.render(f'Player: {SCORE_PLAYER} CPU: {SCORE_CPU}', True, pygame.Color('white'))
    GAME_WINDOW.blit(score_text, ((WINDOW_WIDTH - score_text.get_width()) // 2, 20))

    # Check if ball collides with player or cpu paddle and play hit sound effect
    if ball.colliderect(player) or ball.colliderect(cpu):
        pygame.mixer.Sound.play(sound_hit)

    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()














