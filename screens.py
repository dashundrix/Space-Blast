from settings import *

# Function to display the title screen
def display_title_screen(WIN, BG, bg_y):
    # Create font and title text
    font = pygame.font.SysFont('ADLaM Display', 60)
    title_text = font.render("SPACE BLAST", True, (255, 255, 255))

    PLAY_BUTTON_WIDTH = 200
    PLAY_BUTTON_HEIGHT = 80
    PLAY_BUTTON_IMAGE = pygame.image.load("assets/Start_Button.png")
    PLAY_BUTTON_IMAGE = pygame.transform.scale(PLAY_BUTTON_IMAGE, (PLAY_BUTTON_WIDTH, PLAY_BUTTON_HEIGHT))
    
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, PLAY_BUTTON_WIDTH, PLAY_BUTTON_HEIGHT)
    
    # Scroll the background just like the game
    WIN.fill((0, 0, 0))  # Black background
    
    # Draw the first background
    WIN.blit(BG, (0, bg_y))  
    # Draw the second background just below the first one
    WIN.blit(BG, (0, bg_y - HEIGHT))  

    # Check if the background has scrolled off screen, and reset it
    if bg_y >= HEIGHT:
        bg_y = 0  # Reset the background position when it reaches the height of the screen

    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    WIN.blit(PLAY_BUTTON_IMAGE, (play_button.x, play_button.y))

   
    pygame.display.update()
    
    return play_button, bg_y

# Function to display the pause screen with transparency
def display_pause_screen(WIN):
    font = pygame.font.SysFont('Arial', 60)
    pause_text = font.render("PAUSED", True, (255, 0, 0))

    # Create a semi-transparent overlay (RGBA color with alpha channel)
    overlay = pygame.Surface((WIDTH, HEIGHT))  # Create a surface with the same size as the window
    overlay.set_alpha(1)  # Set alpha value for transparency (0 is fully transparent, 255 is fully opaque)
    overlay.fill((0, 0, 0))  # Fill with black color (you can change this color as needed)

    # Blit the overlay onto the window
    WIN.blit(overlay, (0, 0))

    # Draw the "PAUSED" text on top of the transparent overlay
    WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))

    # Continue button
    continue_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(WIN, (0, 255, 0), continue_button)  # Green button
    continue_text = pygame.font.SysFont('Arial', 30).render("Continue", True, (0, 0, 0))
    WIN.blit(continue_text, (continue_button.x + (continue_button.width - continue_text.get_width()) // 2, continue_button.y + (continue_button.height - continue_text.get_height()) // 2))

    # Exit button
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
    pygame.draw.rect(WIN, (255, 0, 0), exit_button)  # Red button
    exit_text = pygame.font.SysFont('Arial', 30).render("Exit", True, (0, 0, 0))
    WIN.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, exit_button.y + (exit_button.height - exit_text.get_height()) // 2))

    pygame.display.update()

    return continue_button, exit_button

# Game Over Display
def display_game_over(WIN):
    font = pygame.font.SysFont('Arial', 60)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)