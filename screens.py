from settings import *
import sys
import os

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

    LEADERBOARD_BUTTON_IMAGE = pygame.image.load("assets/LEADERBOARD_BUTTON.png")
    LEADERBOARD_BUTTON_IMAGE = pygame.transform.scale(LEADERBOARD_BUTTON_IMAGE, (96 , 96))

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
    leaderboard_button = pygame.Rect(WIDTH - 140, HEIGHT - 140 , 128, 128)
    reyes_logo = pygame.Rect(10, HEIGHT - 64 - 10 , 128, 128)

    

    WIN.fill((0, 0, 0))
    WIN.blit(BG, (0, bg_y))
    WIN.blit(BG, (0, bg_y - HEIGHT))

    # Check if the background has scrolled off screen, and reset it
    if bg_y >= HEIGHT:
        bg_y = 0  # Reset the background position when it reaches the height of the screen

    WIN.blit(SPACEBLAST_LOGO,(spaceblast_logo.x,spaceblast_logo.y))
    WIN.blit(PLAY_BUTTON_FRAMES[frame_index], (play_button.x, play_button.y))
    WIN.blit(DIFFICULTY_BUTTON_IMAGE, (difficulty_button.x, difficulty_button.y))
    WIN.blit(LEADERBOARD_BUTTON_IMAGE, (leaderboard_button.x, leaderboard_button.y)) 
    leaderboard_text = pygame.font.SysFont('Arial', 25).render("Leaderboard", True, (255, 255, 255))
    WIN.blit(leaderboard_text, (leaderboard_button.x + 48 - leaderboard_text.get_width()//2, 
                               leaderboard_button.y + 48 - leaderboard_text.get_height()//2 + 60))
    WIN.blit(EXIT_BUTTON_IMAGE, (exit_button.x, exit_button.y))
    WIN.blit(REYES_LOGO, (reyes_logo.x, reyes_logo.y))
    

    cursor_rect = cursor_img.get_rect()
    cursor_rect.center = pygame.mouse.get_pos()
    WIN.blit(cursor_img, cursor_rect)
    
    pygame.display.update()
    
    return play_button, difficulty_button,leaderboard_button, exit_button, bg_y

def display_character_selection(WIN, bg_y, cursor_img):
    """Display character selection screen with different animated ship options"""
    # Set up fonts
    title_font = pygame.font.SysFont('Arial', 48)
    button_font = pygame.font.SysFont('Arial', 24)
    
    # Create ship selection frames - using your existing animation system
    ship_types = [
        {
            "id": 1,
            "name": "Falcon",
            "frames": PLAYER_FRAMES,  # Use your existing animation frames
            "stats": "Speed: [ I I I . . ]\nPower: [ I I . . . ]\nHealth: [ I I I I . ]",
            "description": "Balanced fighter with good maneuverability"
        },
        {
            "id": 2,
            "name": "Destroyer",
            "frames": PLAYER_FRAMES,  # For now using same frames, you can replace with new ones
            "stats": "Speed: [ I I . . . ]\nPower: [ I I I I . ]\nHealth: [ I I I I I ]",
            "description": "Heavy fighter with powerful weapons"
        },
        {
            "id": 3,
            "name": "Phantom",
            "frames": PLAYER_FRAMES,  # For now using same frames, you can replace with new ones
            "stats": "Speed: [ I I I I . ]\nPower: [ I I I . . ]\nHealth: [ I I . . . ]",
            "description": "Fast scout ship with rapid-fire weapons"
        }
    ]
    
    # Animation variables
    animation_speed = 4
    frame_counters = [0, 0, 0]
    frame_indices = [0, 0, 0]
    
    # Create ship selection buttons
    ship_spacing = 300
    start_x = WIDTH // 2 - (ship_spacing * 3) // 2 + ship_spacing // 2 - 60
    
    ship_rects = [
        pygame.Rect(start_x, HEIGHT // 2 - 100, PLAYER_WIDTH, PLAYER_HEIGHT),
        pygame.Rect(start_x + ship_spacing, HEIGHT // 2 - 100, PLAYER_WIDTH, PLAYER_HEIGHT),
        pygame.Rect(start_x + ship_spacing * 2, HEIGHT // 2 - 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    ]
    
    # Create back button
    back_button = pygame.Rect(50, HEIGHT - 80, 120, 50)
    back_text = button_font.render("Back", True, (255, 255, 255))
    
    # Create select button
    select_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
    select_text = button_font.render("Select Ship", True, (255, 255, 255))
    
    # Track selected ship
    selected_ship = 1  # Default to first ship
    
    # Main selection loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(60)  # Limit to 60 FPS for consistent animations
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if a ship was clicked
                for i, rect in enumerate(ship_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_ship = ship_types[i]["id"]
                
                # Check if back button was clicked
                if back_button.collidepoint(mouse_pos):
                    return None  # Return to title screen without selection
                
                # Check if select button was clicked
                if select_button.collidepoint(mouse_pos):
                    return selected_ship  # Return the selected ship ID
        
        # Update background position for scrolling effect
        bg_y += 1
        if bg_y >= HEIGHT:
            bg_y = 0
            
        # Draw everything
        WIN.fill((0, 0, 0))
        WIN.blit(BG, (0, bg_y))
        WIN.blit(BG, (0, bg_y - HEIGHT))
        
        # Draw title
        title_text = title_font.render("SELECT YOUR SHIP", True, (255, 255, 255))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))
        
        # Draw ships with animations
        for i, ship in enumerate(ship_types):
            # Update animation
            frame_counters[i] += 1
            if frame_counters[i] >= animation_speed:
                frame_indices[i] = (frame_indices[i] + 1) % len(ship["frames"]["idle"])
                frame_counters[i] = 0
            
            # Draw selection highlight
            if ship["id"] == selected_ship:
                highlight_rect = ship_rects[i].inflate(40, 40)
                pygame.draw.rect(WIN, (0, 255, 0), highlight_rect, 3, border_radius=10)
            
            # Draw ship animation frame
            current_frame = ship["frames"]["idle"][frame_indices[i]]
            WIN.blit(current_frame, ship_rects[i])
            
            # Draw ship name
            name_text = button_font.render(ship["name"], True, (255, 255, 255))
            WIN.blit(name_text, (ship_rects[i].centerx - name_text.get_width() // 2, 
                                ship_rects[i].bottom + 10))
            
            # Draw ship stats
            stats_lines = ship["stats"].split('\n')
            for j, line in enumerate(stats_lines):
                stat_text = pygame.font.SysFont('Arial', 18).render(line, True, (200, 200, 200))
                WIN.blit(stat_text, (ship_rects[i].centerx - stat_text.get_width() // 2, 
                                    ship_rects[i].bottom + 40 + j * 20))
            
            # Draw ship description
            desc_text = pygame.font.SysFont('Arial', 16).render(ship["description"], True, (180, 180, 180))
            WIN.blit(desc_text, (ship_rects[i].centerx - desc_text.get_width() // 2, 
                                ship_rects[i].bottom + 90))
        
        # Draw back button
        pygame.draw.rect(WIN, (80, 80, 80), back_button, border_radius=5)
        pygame.draw.rect(WIN, (150, 150, 150), back_button, 2, border_radius=5)
        WIN.blit(back_text, (back_button.centerx - back_text.get_width()//2, 
                            back_button.centery - back_text.get_height()//2))
        
        # Draw select button
        pygame.draw.rect(WIN, (0, 100, 0), select_button, border_radius=5)
        pygame.draw.rect(WIN, (0, 200, 0), select_button, 2, border_radius=5)
        WIN.blit(select_text, (select_button.centerx - select_text.get_width()//2, 
                              select_button.centery - select_text.get_height()//2))
        
        # Draw cursor
        cursor_rect = cursor_img.get_rect()
        cursor_rect.center = pygame.mouse.get_pos()
        WIN.blit(cursor_img, cursor_rect)
        
        pygame.display.update()
    
    return selected_ship



# Add these new functions for leaderboard functionality
def save_score(player_name, score):
    """Save a player's score to the leaderboard file"""
    try:
        # Open the file in append mode
        with open("leaderboard.txt", "a") as file:
            # Write the name and score on a new line
            file.write(f"{player_name},{score}\n")
    except Exception as e:
        print(f"Error saving score: {e}")

def load_scores():
    """Load all scores from the leaderboard file and return sorted list"""
    scores = []
    try:
        # Check if file exists first
        if not os.path.exists("leaderboard.txt"):
            return []
            
        # Open the file in read mode
        with open("leaderboard.txt", "r") as file:
            # Read each line
            for line in file:
                # Split the line by comma to get name and score
                if "," in line:
                    name, score_str = line.strip().split(",")
                    # Convert score to integer
                    score = int(score_str)
                    scores.append((name, score))
    except Exception as e:
        print(f"Error loading scores: {e}")
    
    # Sort scores by score value (highest first)
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return only top 10 scores
    return scores[:10]

# Add name input screen
def display_name_input(WIN, score, cursor_img):
    """Display screen for player to enter their name"""
    # Set up fonts
    title_font = pygame.font.SysFont('Arial', 48)
    input_font = pygame.font.SysFont('Arial', 36)
    
    # Create input box
    input_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2, 400, 50)
    input_text = ""
    active = True
    
    # Create submit button
    submit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    submit_text = pygame.font.SysFont('Arial', 24).render("Submit", True, (255, 255, 255))
    
    # Background image
    GAMEOVER_BG = pygame.image.load("assets/backgroundspaceview2.png")
    GAMEOVER_BG = pygame.transform.scale(GAMEOVER_BG, (WIDTH, HEIGHT))
    
    # Main input loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        # Submit name
                        if input_text:
                            save_score(input_text, score)
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        # Limit name length to 15 characters
                        if len(input_text) < 24:
                            input_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if submit_button.collidepoint(mouse_pos) and input_text:
                    save_score(input_text, score)
                    return
        
        # Draw everything
        WIN.blit(GAMEOVER_BG, (0, 0))
        
        # Draw title
        title_text = title_font.render(f"Your Score: {score}", True, (255, 255, 255))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        # Draw prompt
        prompt_text = input_font.render("Enter your name:", True, (255, 255, 255))
        WIN.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 80))
        
        # Draw input box
        pygame.draw.rect(WIN, (100, 100, 100), input_box)
        pygame.draw.rect(WIN, (255, 255, 255), input_box, 2)
        
        # Draw input text
        text_surface = input_font.render(input_text, True, (255, 255, 255))
        WIN.blit(text_surface, (input_box.x + 10, input_box.y + 10))
        
        # Draw submit button
        button_color = (0, 150, 0) if input_text else (100, 100, 100)
        pygame.draw.rect(WIN, button_color, submit_button, border_radius=5)
        pygame.draw.rect(WIN, (255, 255, 255), submit_button, 2, border_radius=5)
        WIN.blit(submit_text, (submit_button.centerx - submit_text.get_width()//2, 
                              submit_button.centery - submit_text.get_height()//2))
        
        # Draw cursor
        cursor_rect = cursor_img.get_rect()
        cursor_rect.center = pygame.mouse.get_pos()
        WIN.blit(cursor_img, cursor_rect)
        
        pygame.display.update()


# Add leaderboard display screen
def display_leaderboard(WIN, bg_y, cursor_img):
    """Display the leaderboard screen"""
    # Load scores
    scores = load_scores()
    
    # Background image
    LEADERBOARD_BG = pygame.image.load("assets/backgroundspaceview.jpg")
    LEADERBOARD_BG = pygame.transform.scale(LEADERBOARD_BG, (WIDTH, HEIGHT))

    # Create font for title and scores
    title_font = pygame.font.SysFont('Arial', 48)
    score_font = pygame.font.SysFont('Arial', 24)
    
    # Create back button
    back_button = pygame.Rect(50, HEIGHT - 80, 120, 50)
    back_text = pygame.font.SysFont('Arial', 24).render("Back", True, (255, 255, 255))
    
    # Main leaderboard loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    return bg_y  # Return to title screen
        
        # Update background position for scrolling effect
        bg_y += 1
        if bg_y >= HEIGHT:
            bg_y = 0
            
        # Draw everything
        WIN.fill((0, 0, 0))
        WIN.blit(LEADERBOARD_BG, (0, 0))
        
        # Draw title
        title_text = title_font.render("LEADERBOARD", True, (255, 255, 255))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))
        
        # Draw scores
        if not scores:
            no_scores_text = score_font.render("No scores yet!", True, (255, 255, 255))
            WIN.blit(no_scores_text, (WIDTH // 2 - no_scores_text.get_width() // 2, HEIGHT // 2))
        else:
            # Calculate centered positions
            table_width = 500  # Total width of our table
            left_margin = (WIDTH - table_width) // 2  # Starting X position to center the table
            
            # Column positions
            rank_x = left_margin
            name_x = left_margin + 100
            score_x = left_margin + 400
            
            # Draw header
            header_y = 120
            rank_header = score_font.render("Rank", True, (255, 255, 0))
            name_header = score_font.render("Name", True, (255, 255, 0))
            score_header = score_font.render("Score", True, (255, 255, 0))
            
            WIN.blit(rank_header, (rank_x, header_y))
            WIN.blit(name_header, (name_x, header_y))
            WIN.blit(score_header, (score_x, header_y))
            
            # Draw horizontal line
            pygame.draw.line(WIN, (255, 255, 255), 
                            (left_margin - 20, header_y + 30), 
                            (left_margin + table_width, header_y + 30), 2)
            
            # Draw each score entry
            for i, (name, score) in enumerate(scores):
                y_pos = 170 + i * 40
                rank_text = score_font.render(f"{i+1}.", True, (255, 255, 255))
                name_text = score_font.render(str(name), True, (255, 255, 255))
                score_text = score_font.render(str(score), True, (255, 255, 255))
                
                WIN.blit(rank_text, (rank_x, y_pos))
                WIN.blit(name_text, (name_x, y_pos))
                WIN.blit(score_text, (score_x, y_pos))

        
        # Draw back button
        pygame.draw.rect(WIN, (80, 80, 80), back_button, border_radius=5)
        pygame.draw.rect(WIN, (150, 150, 150), back_button, 2, border_radius=5)
        WIN.blit(back_text, (back_button.centerx - back_text.get_width()//2, 
                            back_button.centery - back_text.get_height()//2))
        
        # Draw cursor
        cursor_rect = cursor_img.get_rect()
        cursor_rect.center = pygame.mouse.get_pos()
        WIN.blit(cursor_img, cursor_rect)
        
        pygame.display.update()
    
    return bg_y

# Function to display the pause screen with transparency
def display_pause_screen(WIN):
    gameover.play()
    BUTTON_WIDTH = 230
    BUTTON_HEIGHT = 50
   
    EXIT_BUTTON_IMAGE = pygame.image.load("assets/Exit_Button.png")
    EXIT_BUTTON_IMAGE = pygame.transform.scale(EXIT_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))
    

    PAUSE_BG = pygame.image.load("assets/backgroundspaceview.jpg")  # Create this image
    PAUSE_BG = pygame.transform.scale(PAUSE_BG, (WIDTH, HEIGHT))
   
    font = pygame.font.SysFont('Arial', 48)
    pause_text = font.render("PAUSED", True, (255, 255, 255))

  
    continue_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 , BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    # Draw the background image instead of using a transparent overlay
    WIN.blit(PAUSE_BG, (0, 0))
    WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2 + 3 , 10))

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
    # First check if the score is in the top 10
    current_scores = load_scores()
    is_top_score = False
    
    # If there are fewer than 10 scores, or the score is higher than the lowest top 10 score
    if len(current_scores) < 9 or (current_scores and score > current_scores[-1][1]):
        is_top_score = True
    
    # If it's a top score and greater than 0, prompt for name immediately
    if is_top_score and score > 0:
        display_name_input(WIN, score, cursor_img)
    
    # Set up fonts
    title_font = pygame.font.SysFont('Arial', 60)
    button_font = pygame.font.SysFont('Arial', 30)
    score_font = pygame.font.SysFont('Arial', 40)

    BUTTON_WIDTH = 230
    BUTTON_HEIGHT = 50
   
    # Load and scale button images
    EXIT_BUTTON_IMAGE = pygame.image.load("assets/Exit_Button.png")
    EXIT_BUTTON_IMAGE = pygame.transform.scale(EXIT_BUTTON_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))

    GAMEOVER_BG = pygame.image.load("assets/backgroundspaceview2.png")
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





