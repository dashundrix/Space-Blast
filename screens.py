from settings import *
import sys

# Function to display the title screen
def display_title_screen(WIN, BG, bg_y, cursor_img):

    BUTTON_WIDTH = 230
    BUTTON_HEIGHT = 50
    BUTTON_SPACING = 8

    # Load and scale ALL button images
    SPACEBLAST_LOGO = pygame.image.load("assets/SpaceBlast.png")
    SPACEBLAST_LOGO = pygame.transform.scale(SPACEBLAST_LOGO, (700,320))

    PLAY_BUTTON_IMAGE = pygame.image.load("assets/Start_Button.png")
    PLAY_BUTTON_IMAGE = pygame.transform.scale(PLAY_BUTTON_IMAGE, (BUTTON_WIDTH* 4, BUTTON_HEIGHT))
    
    REYES_LOGO = pygame.image.load("assets/SeanReyesGames.png")
    REYES_LOGO = pygame.transform.scale(REYES_LOGO, (64,64))
    
    DIFFICULTY_BUTTON_IMAGE = pygame.image.load("assets/Difficulty_Button.png")
    DIFFICULTY_BUTTON_IMAGE = pygame.transform.scale(DIFFICULTY_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))
    
    EXIT_BUTTON_IMAGE = pygame.image.load("assets/Exit_Button.png")
    EXIT_BUTTON_IMAGE = pygame.transform.scale(EXIT_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))

    # Get frame width from the sprite sheet automatically
    frame_width = PLAY_BUTTON_IMAGE.get_width() // 4
    frame_height = PLAY_BUTTON_IMAGE.get_height()

    PLAY_BUTTON_FRAMES = [
        PLAY_BUTTON_IMAGE.subsurface((frame_width * i, 0, frame_width, frame_height))
        for i in range(4)
    ]
    
    # Animation timing
    current_time = pygame.time.get_ticks()
    animation_speed = 200
    frame_index = (current_time // animation_speed) % 4
    

    # Create button rectangles
    start_y = HEIGHT // 2 
    spaceblast_logo = pygame.Rect(WIDTH // 2 - 300, 30 , 128, 128)
    play_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, start_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    difficulty_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, start_y + (BUTTON_HEIGHT + BUTTON_SPACING) * 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    reyes_logo = pygame.Rect(10, HEIGHT - 64 - 10 , 128, 128)
    

    WIN.fill((0, 0, 0))
    WIN.blit(BG2, (0, bg_y))
    WIN.blit(BG2, (0, bg_y - HEIGHT))

    # Check if the background has scrolled off screen, and reset it
    if bg_y >= HEIGHT:
        bg_y = 0  # Reset the background position when it reaches the height of the screen

    WIN.blit(SPACEBLAST_LOGO,(spaceblast_logo.x,spaceblast_logo.y))
    WIN.blit(PLAY_BUTTON_FRAMES[frame_index], (play_button.x, play_button.y))
    WIN.blit(DIFFICULTY_BUTTON_IMAGE, (difficulty_button.x, difficulty_button.y))
    WIN.blit(EXIT_BUTTON_IMAGE, (exit_button.x, exit_button.y))
    WIN.blit(REYES_LOGO, (reyes_logo.x, reyes_logo.y))
    

    cursor_rect = cursor_img.get_rect()
    cursor_rect.center = pygame.mouse.get_pos()
    WIN.blit(cursor_img, cursor_rect)
    
    pygame.display.update()
    
    return play_button, difficulty_button, exit_button, bg_y

#def display_character_selection(WIN, BG, bg_y):
    # Create font for title
    font = pygame.font.SysFont('ADLaM Display', 48)
    select_text = font.render("SELECT YOUR SHIP", True, (255, 255, 255))
    
    # Character slots dimensions
    SLOT_WIDTH = 200
    SLOT_HEIGHT = 200
    SPACING = 50
    
    # Load character ships (add your ship images)
    ship1 = pygame.image.load("assets/ship1.png")
    ship2 = pygame.image.load("assets/ship2.png")
    ship3 = pygame.image.load("assets/ship3.png")
    
    # Scale ships to fit slots
    ship1 = pygame.transform.scale(ship1, (SLOT_WIDTH - 40, SLOT_HEIGHT - 40))
    ship2 = pygame.transform.scale(ship2, (SLOT_WIDTH - 40, SLOT_HEIGHT - 40))
    ship3 = pygame.transform.scale(ship3, (SLOT_WIDTH - 40, SLOT_HEIGHT - 40))
    
    # Create character slots
    total_width = (SLOT_WIDTH * 3) + (SPACING * 2)
    start_x = (WIDTH - total_width) // 2
    
    slot1 = pygame.Rect(start_x, HEIGHT // 2 - SLOT_HEIGHT // 2, SLOT_WIDTH, SLOT_HEIGHT)
    slot2 = pygame.Rect(start_x + SLOT_WIDTH + SPACING, HEIGHT // 2 - SLOT_HEIGHT // 2, SLOT_WIDTH, SLOT_HEIGHT)
    slot3 = pygame.Rect(start_x + (SLOT_WIDTH + SPACING) * 2, HEIGHT // 2 - SLOT_HEIGHT // 2, SLOT_WIDTH, SLOT_HEIGHT)
    
    # Scrolling background
    WIN.fill((0, 0, 0))
    WIN.blit(BG, (0, bg_y))
    WIN.blit(BG, (0, bg_y - HEIGHT))
    
    if bg_y >= HEIGHT:
        bg_y = 0
    
    # Draw title
    WIN.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, HEIGHT // 4))
    
    # Draw character slots
    for slot in [slot1, slot2, slot3]:
        pygame.draw.rect(WIN, (100, 100, 100), slot, border_radius=10)
        pygame.draw.rect(WIN, (255, 255, 255), slot, 3, border_radius=10)
    
    # Draw ships in slots
    WIN.blit(ship1, (slot1.x + 20, slot1.y + 20))
    WIN.blit(ship2, (slot2.x + 20, slot2.y + 20))
    WIN.blit(ship3, (slot3.x + 20, slot3.y + 20))
    
    # Draw ship names
    name_font = pygame.font.SysFont('Arial', 24)
    ship1_name = name_font.render("Fighter", True, (255, 255, 255))
    ship2_name = name_font.render("Destroyer", True, (255, 255, 255))
    ship3_name = name_font.render("Scout", True, (255, 255, 255))
    
    WIN.blit(ship1_name, (slot1.centerx - ship1_name.get_width()//2, slot1.bottom + 10))
    WIN.blit(ship2_name, (slot2.centerx - ship2_name.get_width()//2, slot2.bottom + 10))
    WIN.blit(ship3_name, (slot3.centerx - ship3_name.get_width()//2, slot3.bottom + 10))
    
    pygame.display.update()
    
    return [slot1, slot2, slot3], bg_y

# Function to display the pause screen with transparency
def display_pause_screen(WIN):
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 80
   
    EXIT_BUTTON_IMAGE = pygame.image.load("assets/Exit_Button.png")
    EXIT_BUTTON_IMAGE = pygame.transform.scale(EXIT_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))
    

    PAUSE_BG = pygame.image.load("assets/backgroundspaceview.jpg")  # Create this image
    PAUSE_BG = pygame.transform.scale(PAUSE_BG, (WIDTH, HEIGHT))
   
    font = pygame.font.SysFont('Arial', 60)
    pause_text = font.render("PAUSED", True, (255, 0, 0))

  
    continue_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 , BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # Draw the background image instead of using a transparent overlay
    WIN.blit(PAUSE_BG, (0, 0))
    WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))

    # Draw continue button
    pygame.draw.rect(WIN, (0, 255, 0), continue_button)
    continue_text = pygame.font.SysFont('Arial', 30).render("Continue", True, (0, 0, 0))
    WIN.blit(continue_text, (continue_button.x + (continue_button.width - continue_text.get_width()) // 2, 
                            continue_button.y + (continue_button.height - continue_text.get_height()) // 2))

    # Draw exit button
    WIN.blit(EXIT_BUTTON_IMAGE, (exit_button.x, exit_button.y))

    # Draw cursor
    cursor_rect = cursor_img.get_rect()
    cursor_rect.center = pygame.mouse.get_pos()
    WIN.blit(cursor_img, cursor_rect)

    pygame.display.update()

    return continue_button, exit_button

# Game Over Display
def display_game_over(WIN, score, cursor_img):
    # Set up fonts
    title_font = pygame.font.SysFont('Arial', 60)
    button_font = pygame.font.SysFont('Arial', 30)
    score_font = pygame.font.SysFont('Arial', 40)

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 80
   
    # Load and scale button images
    EXIT_BUTTON_IMAGE = pygame.image.load("assets/Exit_Button.png")
    EXIT_BUTTON_IMAGE = pygame.transform.scale(EXIT_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))

    GAMEOVER_BG = pygame.image.load("assets/backgroundspaceview.jpg")  # Create this image
    GAMEOVER_BG = pygame.transform.scale(GAMEOVER_BG, (WIDTH, HEIGHT))
   
    # Create text surfaces
    game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = button_font.render("Restart", True, (255, 255, 255))
   
    # Create button rectangles
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, BUTTON_WIDTH, BUTTON_HEIGHT)
   
   
    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    return "restart"
                elif exit_button.collidepoint(mouse_pos):
                    return "exit"
       
        # Update cursor position
        cursor_rect = cursor_img.get_rect()
        cursor_rect.center = pygame.mouse.get_pos()
       
        # REDRAW EVERYTHING each frame
        # 1. Start with the overlay
        WIN.blit(GAMEOVER_BG, (0, 0))
       
        # 2. Draw all text elements
        WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
        WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
       
        # 3. Draw restart button
        pygame.draw.rect(WIN, (50, 50, 50), restart_button)
        pygame.draw.rect(WIN, (100, 100, 100), restart_button, 3)  # Button border
        WIN.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                               restart_button.centery - restart_text.get_height() // 2))
        
        # 4. Draw exit button
        WIN.blit(EXIT_BUTTON_IMAGE, (exit_button.x, exit_button.y))
       
        # 5. Draw cursor last
        WIN.blit(cursor_img, cursor_rect)
        
        # 6. Update display
        pygame.display.update()



