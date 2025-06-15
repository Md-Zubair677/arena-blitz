import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (10, 10, 30)
GREEN = (0, 255, 180)
RED = (255, 60, 60)
WHITE = (255, 255, 255)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Ops")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 28)

# Load background image
bg_image = pygame.image.load("games/shadow_ops/assets/images/bg.png")
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player setup
player_size = (50, 50)
player = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, *player_size)
player_speed = 7

# Enemy setup
enemy_size = (50, 50)
enemies = []
enemy_spawn_rate = 30  # lower = faster spawns
base_enemy_speed = 4

# Score
score = 0


def draw_text(text, size, color, x, y, align="topleft"):
    font = pygame.font.SysFont('Arial', size)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    setattr(rect, align, (x, y))
    screen.blit(surface, rect)


def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - enemy_size[0])
    enemy = pygame.Rect(x, -enemy_size[1], *enemy_size)
    enemies.append(enemy)


def reset_game():
    global enemies, score, player
    enemies = []
    score = 0
    player.x = SCREEN_WIDTH // 2


def run():
    global score
    frame = 0
    running = True
    game_over = False

    while True:
        clock.tick(FPS)
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if game_over:
                    if event.key == pygame.K_r:
                        reset_game()
                        game_over = False
                        running = True
                        frame = 0
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x += player_speed
            player.x = max(0, min(player.x, SCREEN_WIDTH - player.width))

            frame += 1
            if frame % enemy_spawn_rate == 0:
                spawn_enemy()

            current_enemy_speed = base_enemy_speed + (score // 1000) * 0.5

            for enemy in enemies[:]:
                enemy.y += current_enemy_speed
                if enemy.top > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                elif enemy.colliderect(player):
                    game_over = True
                    running = False
                else:
                    pygame.draw.rect(screen, RED, enemy)

            pygame.draw.rect(screen, GREEN, player)

            score += 1
            draw_text(f"Score: {score}", 24, WHITE, 10, 10)

        else:
            draw_text("Game Over", 40, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, align="center")
            draw_text("Press R to Restart or Q to Quit", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, align="center")

        pygame.display.flip()


if __name__ == "__main__":
    run()
