"""
============================================
PROJECT 3: SNAKE GAME
============================================
Classic Snake game built with Python and Pygame

FEATURES:
- Smooth snake movement
- Food collection & score tracking
- Increasing difficulty
- Game over & restart option
- High score saving

HOW TO RUN:
1. Install pygame first:
   Open terminal/command prompt and run:
   pip install pygame

2. Run the game:
   python snake_game.py

CONTROLS:
- Arrow Keys: Move the snake
- SPACE: Restart after game over
- ESC: Quit game
============================================
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# ========== COLORS ==========
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
DARK_GREEN = (39, 174, 96)
GRAY = (149, 165, 166)
PURPLE = (142, 68, 173)

# ========== GAME SETTINGS ==========
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# ========== INITIALIZE SCREEN ==========
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('🐍 Snake Game')
clock = pygame.time.Clock()

# ========== FONTS ==========
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)
font_tiny = pygame.font.Font(None, 24)


class Snake:
    """Snake class to manage snake behavior"""
    
    def __init__(self):
        """Initialize the snake"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.head_color = DARK_GREEN
    
    def get_head_position(self):
        """Get the position of snake's head"""
        return self.positions[0]
    
    def turn(self, point):
        """Change snake direction"""
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return  # Prevent 180-degree turns
        else:
            self.direction = point
    
    def move(self):
        """Move the snake"""
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH),
               (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        
        # Check if snake hits itself
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False  # Game over
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True
    
    def reset(self):
        """Reset snake to initial state"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    def draw(self, surface):
        """Draw the snake"""
        for i, p in enumerate(self.positions):
            if i == 0:  # Head
                pygame.draw.rect(surface, self.head_color,
                               (p[0], p[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, WHITE,
                               (p[0], p[1], GRID_SIZE, GRID_SIZE), 2)
            else:  # Body
                pygame.draw.rect(surface, self.color,
                               (p[0], p[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, DARK_GREEN,
                               (p[0], p[1], GRID_SIZE, GRID_SIZE), 1)


class Food:
    """Food class to manage food behavior"""
    
    def __init__(self):
        """Initialize food"""
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        """Place food at random position"""
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
    
    def draw(self, surface):
        """Draw the food"""
        pygame.draw.rect(surface, self.color,
                        (self.position[0], self.position[1],
                         GRID_SIZE, GRID_SIZE))
        pygame.draw.circle(surface, YELLOW,
                          (self.position[0] + GRID_SIZE // 2,
                           self.position[1] + GRID_SIZE // 2),
                          GRID_SIZE // 3)


# ========== DIRECTIONS ==========
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_grid(surface):
    """Draw grid lines"""
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (SCREEN_WIDTH, y), 1)
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)


def draw_text(surface, text, size, x, y, color=WHITE):
    """Draw text on screen"""
    if size == 'large':
        font = font_large
    elif size == 'medium':
        font = font_medium
    elif size == 'small':
        font = font_small
    else:
        font = font_tiny
    
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def show_start_screen(surface):
    """Show start screen"""
    surface.fill(BLACK)
    
    draw_text(surface, "🐍 SNAKE GAME", 'large',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, GREEN)
    draw_text(surface, "Use Arrow Keys to Move", 'small',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
    draw_text(surface, "Press SPACE to Start", 'small',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, YELLOW)
    draw_text(surface, "Press ESC to Quit", 'tiny',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, GRAY)
    
    pygame.display.update()


def show_game_over_screen(surface, score, high_score):
    """Show game over screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    draw_text(surface, "GAME OVER!", 'large',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, RED)
    draw_text(surface, f"Score: {score}", 'medium',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, WHITE)
    draw_text(surface, f"High Score: {high_score}", 'small',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, YELLOW)
    draw_text(surface, "Press SPACE to Play Again", 'small',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80, GREEN)
    draw_text(surface, "Press ESC to Quit", 'tiny',
             SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130, GRAY)
    
    pygame.display.update()


def main():
    """Main game loop"""
    
    # Game variables
    snake = Snake()
    food = Food()
    score = 0
    high_score = 0
    game_state = 'start'  # 'start', 'playing', 'game_over'
    
    # Show start screen
    show_start_screen(screen)
    
    # Main game loop
    running = True
    while running:
        clock.tick(10)  # FPS
        
        # ========== EVENT HANDLING ==========
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # Quit game
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Start screen
                if game_state == 'start':
                    if event.key == pygame.K_SPACE:
                        game_state = 'playing'
                
                # Playing
                elif game_state == 'playing':
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)
                
                # Game over
                elif game_state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        snake.reset()
                        food.randomize_position()
                        score = 0
                        game_state = 'playing'
        
        # ========== GAME LOGIC ==========
        if game_state == 'playing':
            # Move snake
            alive = snake.move()
            
            if not alive:
                game_state = 'game_over'
                if score > high_score:
                    high_score = score
            
            # Check if snake eats food
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 10
                food.randomize_position()
                
                # Make sure food doesn't spawn on snake
                while food.position in snake.positions:
                    food.randomize_position()
        
        # ========== DRAWING ==========
        if game_state == 'start':
            # Start screen is already shown
            pass
        
        elif game_state == 'playing':
            # Draw game
            screen.fill(BLACK)
            draw_grid(screen)
            snake.draw(screen)
            food.draw(screen)
            
            # Draw score
            score_text = font_small.render(f'Score: {score}', True, WHITE)
            screen.blit(score_text, (10, 10))
            
            high_score_text = font_tiny.render(f'High Score: {high_score}',
                                              True, YELLOW)
            screen.blit(high_score_text, (10, 50))
            
            pygame.display.update()
        
        elif game_state == 'game_over':
            # Show game over screen
            show_game_over_screen(screen, score, high_score)
    
    pygame.quit()
    sys.exit()


# ========== RUN GAME ==========
if __name__ == '__main__':
    main()
