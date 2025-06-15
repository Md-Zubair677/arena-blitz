#!/usr/bin/env python3
"""
Arena Blitz Game Launcher
Main entry point for the game launcher application.
"""
import os
import sys
import pygame

pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
TITLE = "Arena Blitz Game Launcher"
BG_COLOR = (25, 35, 60)  # Deeper blue for a more premium look
TEXT_COLOR = (220, 220, 255)  # Slightly blue-tinted text
BUTTON_COLOR = (45, 85, 135)  # Vibrant blue buttons
BUTTON_HOVER_COLOR = (65, 125, 185)  # Lighter blue on hover
BUTTON_TEXT_COLOR = (240, 240, 255)  # Bright text on buttons
ACCENT_COLOR = (255, 165, 0)  # Orange accent color

class GameLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 26, bold=True)
        self.title_font = pygame.font.SysFont('Arial', 42, bold=True)
        self.running = True

        self.games = [
            {"name": "Cyber Ninja Assault", "module": "cyber_ninja_assault"},

            {"name": "Shadow Ops", "module": "shadow_ops"}
        ]

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.check_button_click(event.pos)

    def update(self):
        pass

    def render(self):
        # Create gradient background
        for y in range(SCREEN_HEIGHT):
            # Calculate gradient color (darker at top, lighter at bottom)
            gradient_factor = y / SCREEN_HEIGHT
            r = int(BG_COLOR[0] * (1 + gradient_factor * 0.3))
            g = int(BG_COLOR[1] * (1 + gradient_factor * 0.3))
            b = int(BG_COLOR[2] * (1 + gradient_factor * 0.3))
            r = min(r, 255)
            g = min(g, 255)
            b = min(b, 255)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw title with shadow effect
        shadow_text = self.title_font.render(TITLE, True, (20, 20, 30))
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, 53))
        self.screen.blit(shadow_text, shadow_rect)
        
        title_text = self.title_font.render(TITLE, True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)

        button_height = 70
        button_width = 350
        button_spacing = 30
        start_y = 180

        for i, game in enumerate(self.games):
            button_y = start_y + i * (button_height + button_spacing)
            button_rect = pygame.Rect(
                (SCREEN_WIDTH - button_width) // 2,
                button_y,
                button_width,
                button_height
            )
            mouse_pos = pygame.mouse.get_pos()
            hover = button_rect.collidepoint(mouse_pos)
            color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
            
            # Draw button with gradient and glow effect
            for offset in range(5, 0, -1):
                if hover:
                    glow_rect = button_rect.inflate(offset*2, offset*2)
                    glow_color = (ACCENT_COLOR[0], ACCENT_COLOR[1], ACCENT_COLOR[2], 100 - offset*20)
                    pygame.draw.rect(self.screen, glow_color, glow_rect, border_radius=10)
            
            # Draw main button
            pygame.draw.rect(self.screen, color, button_rect, border_radius=8)
            
            # Add highlight to top of button
            highlight_rect = pygame.Rect(button_rect.left + 2, button_rect.top + 2, 
                                        button_rect.width - 4, 10)
            pygame.draw.rect(self.screen, (color[0] + 30, color[1] + 30, color[2] + 30), 
                            highlight_rect, border_radius=8)
            
            button_text = self.font.render(game["name"], True, BUTTON_TEXT_COLOR)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)

        pygame.display.flip()

    def check_button_click(self, pos):
        button_height = 70
        button_width = 350
        button_spacing = 30
        start_y = 180

        for i, game in enumerate(self.games):
            button_y = start_y + i * (button_height + button_spacing)
            button_rect = pygame.Rect(
                (SCREEN_WIDTH - button_width) // 2,
                button_y,
                button_width,
                button_height
            )
            if button_rect.collidepoint(pos):
                self.launch_game(game["module"])

    def launch_game(self, module_name):
        print(f"[LAUNCHER] Launching {module_name}...")
        try:
            game_module = __import__(f"games.{module_name}.main", fromlist=["main"])
            if hasattr(game_module, "run"):
                game_module.run()
            elif hasattr(game_module, "main"):
                game_module.main()
            else:
                print(f"[ERROR] No run() or main() found in {module_name}")
        except ImportError as e:
            print(f"[IMPORT ERROR] {e}")
        except Exception as e:
            print(f"[ERROR] Failed to launch {module_name}: {e}")

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()
