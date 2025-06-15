#!/usr/bin/env python3
"""
Cyber Ninja Assault - Action Game
Escape from red boxes while collecting stars
"""
import pygame
import random
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_COLOR = (0, 255, 200)
ENEMY_COLOR = (255, 80, 80)
STAR_COLOR = (255, 255, 0)
FONT_COLOR = (0, 255, 200)
UI_COLOR = (180, 180, 180)
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)
PLAYER_SIZE = 50
ENEMY_SIZE = 50
STAR_SIZE = 30
SPEED = 5
ENEMY_SPEED_BASE = 2
FPS = 60
MAX_ENEMIES = 5
STAR_COUNT = 3

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

class Star:
    def __init__(self):
        self.x = random.randint(STAR_SIZE, WIDTH - STAR_SIZE)
        self.y = random.randint(STAR_SIZE, HEIGHT - STAR_SIZE)
        self.size = STAR_SIZE
        self.collected = False
        self.points = 50
        self.angle = 0
    
    def draw(self, surface):
        if not self.collected:
            # Draw a 5-pointed star
            self.angle += 0.5
            points = []
            for i in range(10):
                radius = self.size/2 if i % 2 == 0 else self.size/4
                angle = math.pi/5 * i + math.radians(self.angle)
                points.append((
                    self.x + radius * math.sin(angle),
                    self.y - radius * math.cos(angle)
                ))
            pygame.draw.polygon(surface, STAR_COLOR, points)

def run():
    player = pygame.Rect(WIDTH//2, HEIGHT//2, PLAYER_SIZE, PLAYER_SIZE)
    enemies = [pygame.Rect(random.randint(0, WIDTH-ENEMY_SIZE), 
                          random.randint(0, HEIGHT-ENEMY_SIZE), 
                          ENEMY_SIZE, ENEMY_SIZE) for _ in range(3)]
    
    stars = [Star() for _ in range(STAR_COUNT)]
    collected_stars = 0
    total_stars = 0
    
    score = 0
    game_over = False
    level = 1
    enemy_speed = ENEMY_SPEED_BASE

    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if game_over and event.key == pygame.K_r:
                    return run()
                elif game_over and event.key == pygame.K_q:
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

            # Enemy movement
            for enemy in enemies:
                # Enemy follows player
                if enemy.x < player.x:
                    enemy.x += enemy_speed
                elif enemy.x > player.x:
                    enemy.x -= enemy_speed
                if enemy.y < player.y:
                    enemy.y += enemy_speed
                elif enemy.y > player.y:
                    enemy.y -= enemy_speed

                # Collision detection with player
                if player.colliderect(enemy):
                    game_over = True

            # Check for star collection
            for star in stars:
                if not star.collected:
                    star_rect = pygame.Rect(star.x - star.size/2, star.y - star.size/2, star.size, star.size)
                    if player.colliderect(star_rect):
                        star.collected = True
                        score += star.points
                        collected_stars += 1
                        total_stars += 1
            
            # If all stars are collected, add more stars and enemies
            if all(star.collected for star in stars):
                level += 1
                stars = [Star() for _ in range(STAR_COUNT)]
                if len(enemies) < MAX_ENEMIES:
                    enemies.append(pygame.Rect(random.randint(0, WIDTH-ENEMY_SIZE), 
                                             random.randint(0, HEIGHT-ENEMY_SIZE), 
                                             ENEMY_SIZE, ENEMY_SIZE))
                # Increase enemy speed slightly with each level
                enemy_speed = min(enemy_speed + 0.2, SPEED - 0.5)  # Cap enemy speed below player speed

            score += 1

        # Drawing
        screen.blit(bg_image, (0, 0))
        draw_text("Cyber Ninja Assault", FONT, FONT_COLOR, screen, WIDTH//2, 40, center=True)
        draw_text(f"Score: {score}", SMALL_FONT, UI_COLOR, screen, 10, 10)
        draw_text(f"Stars: {collected_stars} (Total: {total_stars})", SMALL_FONT, UI_COLOR, screen, 10, 40)
        draw_text(f"Level: {level}", SMALL_FONT, UI_COLOR, screen, WIDTH - 100, 10)

        # Draw stars
        for star in stars:
            star.draw(screen)

        # Draw player as a ninja character
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        # Draw ninja headband
        pygame.draw.line(screen, (0, 0, 255), 
                        (player.x - PLAYER_SIZE//2, player.y - PLAYER_SIZE//4),
                        (player.x + PLAYER_SIZE//2, player.y - PLAYER_SIZE//4), 5)
        
        # Draw enemies as red boxes with angry faces
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, enemy)
            # Draw angry eyes
            eye_size = ENEMY_SIZE // 8
            pygame.draw.rect(screen, (0, 0, 0), 
                           (enemy.x - ENEMY_SIZE//4, enemy.y - ENEMY_SIZE//4, eye_size, eye_size))
            pygame.draw.rect(screen, (0, 0, 0), 
                           (enemy.x + ENEMY_SIZE//8, enemy.y - ENEMY_SIZE//4, eye_size, eye_size))
            # Draw angry mouth
            pygame.draw.line(screen, (0, 0, 0), 
                           (enemy.x - ENEMY_SIZE//4, enemy.y + ENEMY_SIZE//4),
                           (enemy.x + ENEMY_SIZE//4, enemy.y + ENEMY_SIZE//4), 3)

        if game_over:
            draw_text("Game Over", FONT, (255, 0, 0), screen, WIDTH//2, HEIGHT//2 - 50, center=True)
            draw_text(f"Final Score: {score}", FONT, (255, 255, 255), screen, WIDTH//2, HEIGHT//2, center=True)
            draw_text("Press R to Restart or Q to Quit", SMALL_FONT, UI_COLOR, screen, WIDTH//2, HEIGHT//2 + 50, center=True)

        draw_text("Use arrow keys or WASD to move. ESC to return to launcher.", SMALL_FONT, UI_COLOR, screen, WIDTH//2, HEIGHT - 30, center=True)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    run()
