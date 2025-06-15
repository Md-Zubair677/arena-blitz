#!/usr/bin/env python3
"""
Cyber Ninja Assault - Action Game
"""
import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_COLOR = (0, 255, 200)
ENEMY_COLOR = (255, 80, 80)
FONT_COLOR = (0, 255, 200)
UI_COLOR = (180, 180, 180)
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)
PLAYER_SIZE = 50
ENEMY_SIZE = 50
SPEED = 5
FPS = 60

# Load background image
bg_image = pygame.image.load("games/cyber_ninja_assault/assets/images/bg.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Ninja Assault")
clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y, center=False):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)

def run():
    player = pygame.Rect(WIDTH//2, HEIGHT//2, PLAYER_SIZE, PLAYER_SIZE)
    enemy = pygame.Rect(random.randint(0, WIDTH-ENEMY_SIZE), random.randint(0, HEIGHT-ENEMY_SIZE), ENEMY_SIZE, ENEMY_SIZE)

    score = 0
    game_over = False

    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    return run()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # Movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x -= SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x += SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.y -= SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.y += SPEED

            # Keep inside screen
            player.clamp_ip(screen.get_rect())

            # Enemy follows player
            if enemy.x < player.x:
                enemy.x += 2
            elif enemy.x > player.x:
                enemy.x -= 2
            if enemy.y < player.y:
                enemy.y += 2
            elif enemy.y > player.y:
                enemy.y -= 2

            # Collision detection
            if player.colliderect(enemy):
                game_over = True

            score += 1

        # Drawing
        screen.blit(bg_image, (0, 0))
        draw_text("Cyber Ninja Assault", FONT, FONT_COLOR, screen, WIDTH//2, 40, center=True)
        draw_text(f"Score: {score}", SMALL_FONT, UI_COLOR, screen, 10, 10)

        pygame.draw.rect(screen, PLAYER_COLOR, player)
        pygame.draw.rect(screen, ENEMY_COLOR, enemy)

        if game_over:
            draw_text("Game Over", FONT, (255, 0, 0), screen, WIDTH//2, HEIGHT//2 - 50, center=True)
            draw_text("Press R to Restart or Q to Quit", SMALL_FONT, UI_COLOR, screen, WIDTH//2, HEIGHT//2 + 10, center=True)

        draw_text("Use arrow keys or WASD to move. ESC to quit.", SMALL_FONT, UI_COLOR, screen, WIDTH//2, HEIGHT - 30, center=True)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    run()
