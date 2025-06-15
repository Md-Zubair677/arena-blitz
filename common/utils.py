"""
Utility functions for the Arena Blitz game launcher and games.
"""
import os
import pygame
from .settings import FONTS_DIR, IMAGES_DIR, SOUNDS_DIR

def load_image(filename, scale=1.0, convert_alpha=True):
    """
    Load an image from the images directory.
    
    Args:
        filename (str): The filename of the image to load.
        scale (float): Scale factor to resize the image.
        convert_alpha (bool): Whether to convert the image with alpha channel.
        
    Returns:
        pygame.Surface: The loaded image.
    """
    path = os.path.join(IMAGES_DIR, filename)
    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
            
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder surface
        surf = pygame.Surface((50, 50))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        return surf

def load_game_image(game_name, filename, scale=1.0, convert_alpha=True):
    """
    Load an image from a specific game's images directory.
    
    Args:
        game_name (str): The name of the game folder.
        filename (str): The filename of the image to load.
        scale (float): Scale factor to resize the image.
        convert_alpha (bool): Whether to convert the image with alpha channel.
        
    Returns:
        pygame.Surface: The loaded image.
    """
    from .settings import BASE_DIR
    path = os.path.join(BASE_DIR, "games", game_name, "assets", "images", filename)
    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
            
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder surface
        surf = pygame.Surface((50, 50))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        return surf

def load_sound(filename):
    """
    Load a sound from the sounds directory.
    
    Args:
        filename (str): The filename of the sound to load.
        
    Returns:
        pygame.mixer.Sound: The loaded sound.
    """
    path = os.path.join(SOUNDS_DIR, filename)
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound {path}: {e}")
        return None

def load_font(filename, size):
    """
    Load a font from the fonts directory.
    
    Args:
        filename (str): The filename of the font to load.
        size (int): The size of the font.
        
    Returns:
        pygame.font.Font: The loaded font.
    """
    path = os.path.join(FONTS_DIR, filename)
    try:
        return pygame.font.Font(path, size)
    except pygame.error as e:
        print(f"Error loading font {path}: {e}")
        return pygame.font.SysFont('arial', size)

def draw_text(surface, text, font, color, x, y, align="topleft"):
    """
    Draw text on a surface with alignment options.
    
    Args:
        surface (pygame.Surface): The surface to draw on.
        text (str): The text to draw.
        font (pygame.font.Font): The font to use.
        color (tuple): The color of the text (RGB).
        x (int): The x coordinate.
        y (int): The y coordinate.
        align (str): The alignment of the text ('topleft', 'center', etc.).
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    setattr(text_rect, align, (x, y))
    surface.blit(text_surface, text_rect)

class Button:
    """A simple button class for pygame UIs."""
    
    def __init__(self, x, y, width, height, text, font, 
                 bg_color=(100, 100, 100), text_color=(255, 255, 255),
                 hover_color=(150, 150, 150), border_radius=5):
        """
        Initialize a button.
        
        Args:
            x (int): The x coordinate of the button.
            y (int): The y coordinate of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text on the button.
            font (pygame.font.Font): The font to use for the text.
            bg_color (tuple): The background color of the button (RGB).
            text_color (tuple): The color of the text (RGB).
            hover_color (tuple): The color of the button when hovered (RGB).
            border_radius (int): The radius of the button's corners.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.border_radius = border_radius
        self.is_hovered = False
        
    def draw(self, surface):
        """
        Draw the button on a surface.
        
        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        """
        Update the button's hover state.
        
        Args:
            mouse_pos (tuple): The position of the mouse (x, y).
            
        Returns:
            bool: Whether the button is being hovered.
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        """
        Check if the button is clicked.
        
        Args:
            mouse_pos (tuple): The position of the mouse (x, y).
            mouse_click (bool): Whether the mouse is clicked.
            
        Returns:
            bool: Whether the button is clicked.
        """
        return self.rect.collidepoint(mouse_pos) and mouse_click
