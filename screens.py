from settings import *
import settings
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

    title_font = pygame.font.SysFont('Arial', 48)
    button_font = pygame.font.SysFont('Arial', 24)
    
    # Load star sprite sheet
    star_sheet = pygame.image.load("assets/Star.png")
    
    # Extract frames from the sprite sheet
    star_frames = []
    frame_width = star_sheet.get_width() // 7
    frame_height = star_sheet.get_height()
    
    for i in range(7):
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame.blit(star_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (20, 20))
        star_frames.append(frame)
    
    # Load empty star image
    empty_star_img = pygame.image.load("assets/Empty Star.png")
    empty_star_img = pygame.transform.scale(empty_star_img, (20, 20))
    
    # Load pilot images
    pilot_images = [
        pygame.image.load("assets/Pilot 1.png"),
        pygame.image.load("assets/Pilot 2.png"),
        pygame.image.load("assets/Pilot 3.png")
    ]
    
    # Load pilot voice sounds
    pilot_voices = [
        pygame.mixer.Sound("assets/Pilot 1 Voice.mp3"),  # Make sure these files exist
        pygame.mixer.Sound("assets/Pilot 2 Voice.mp3"),
        pygame.mixer.Sound("assets/Pilot 3 Voice.mp3")
    ]
    
    # Set volume for voice clips
    for voice in pilot_voices:
        voice.set_volume(0.7)  # Adjust volume as needed
    
    # Scale pilot images to appropriate size (half window height)
    pilot_height = HEIGHT // 2
    for i in range(len(pilot_images)):
        # Calculate width to maintain aspect ratio
        aspect_ratio = pilot_images[i].get_width() / pilot_images[i].get_height()
        pilot_width = int(pilot_height * aspect_ratio)
        pilot_images[i] = pygame.transform.scale(pilot_images[i], (pilot_width, pilot_height))
    
    # Pilot animation variables
    pilot_x = -pilot_images[0].get_width()  # Start off-screen
    target_pilot_x = 40  # Target position when selected
    pilot_slide_speed = 20  # Speed of sliding animation
    
    # Star animation variables
    star_animation_speed = 8
    star_frame_counter = 0
    star_frame_index = 0
    
    ship_types = [
        {
            "id": 1,
            "name": "Falcon",
            "frames": PLAYER_FRAMES,  
            "stats": {
                "Speed": 3,
                "Power": 3,
                "Health": 4
            },
            "description": "Balanced fighter with good maneuverability",
            "pilot_index": 0  # Index to pilot_images
        },
        {
            "id": 2,
            "name": "Destroyer",
            "frames": PLAYER_FRAMES2,  
            "stats": {
                "Speed": 2,
                "Power": 4,
                "Health": 5
            },
            "description": "Heavy fighter with powerful weapons",
            "pilot_index": 1  # Index to pilot_images
        },
        {
            "id": 3,
            "name": "Phantom",
            "frames": PLAYER_FRAMES3,
            "stats": {
                "Speed": 5,
                "Power": 2,
                "Health": 2
            },
            "description": "Fast scout ship with rapid-fire weapons",
            "pilot_index": 2  # Index to pilot_images
        }
    ]
    
    # Ship animation variables
    animation_speed = 4
    frame_counters = [0, 0, 0]
    frame_indices = [0, 0, 0]
    
    # Create ship selection buttons
    ship_spacing = 300
    start_x = WIDTH // 2 - (ship_spacing * 3) // 2 + ship_spacing // 2 + 60
    
    ship_rects = [
        pygame.Rect(start_x, HEIGHT // 2 - 110, PLAYER_WIDTH, PLAYER_HEIGHT),
        pygame.Rect(start_x + ship_spacing, HEIGHT // 2 - 110, PLAYER_WIDTH, PLAYER_HEIGHT),
        pygame.Rect(start_x + ship_spacing * 2, HEIGHT // 2 - 110, PLAYER_WIDTH, PLAYER_HEIGHT)
    ]
    
    # Create back button
    back_button = pygame.Rect(50, HEIGHT - 80, 120, 50)
    back_text = button_font.render("Back", True, (255, 255, 255))
    
    # Create select button
    select_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
    select_text = button_font.render("Select Ship", True, (255, 255, 255))
    
    # Track selected ship
    selected_ship = 1  # Default to first ship
    previous_selected_ship = 1  # To detect changes in selection
    
    # Play initial pilot voice
    pilot_voices[ship_types[selected_ship-1]["pilot_index"]].play()
    
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
                        if selected_ship != ship_types[i]["id"]:
                            selected_ship = ship_types[i]["id"]
                            # Play the voice of the newly selected pilot
                            pygame.mixer.stop()  # Stop any currently playing voice
                            pilot_voices[ship_types[selected_ship-1]["pilot_index"]].play()
                
                # Check if back button was clicked
                if back_button.collidepoint(mouse_pos):
                    return None  # Return to title screen without selection
                
                # Check if select button was clicked
                if select_button.collidepoint(mouse_pos):
                    # Play confirmation voice before returning
                    pygame.mixer.stop()
                    pilot_voices[ship_types[selected_ship-1]["pilot_index"]].play()
                    pygame.time.delay(500)  # Short delay to let voice start playing
                    return selected_ship  # Return the selected ship ID
        
        # Check if selection changed
        if selected_ship != previous_selected_ship:
            # Reset pilot position to slide in from left
            pilot_x = -pilot_images[ship_types[selected_ship-1]["pilot_index"]].get_width()
            previous_selected_ship = selected_ship
        
        # Update pilot position (slide animation)
        if pilot_x < target_pilot_x:
            pilot_x += pilot_slide_speed
            if pilot_x > target_pilot_x:
                pilot_x = target_pilot_x
        
        # Update background position for scrolling effect
        bg_y += 1
        if bg_y >= HEIGHT:
            bg_y = 0
        
        # Update star animation
        star_frame_counter += 1
        if star_frame_counter >= star_animation_speed:
            star_frame_index = (star_frame_index + 1) % len(star_frames)
            star_frame_counter = 0
        
        # Draw everything
        WIN.fill((0, 0, 0))
        WIN.blit(BG, (0, bg_y))
        WIN.blit(BG, (0, bg_y - HEIGHT))
        
        # Draw title
        title_text = title_font.render("Select Your Ship", True, (255, 255, 255))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))
        
        # Draw the selected pilot image
        current_pilot_index = ship_types[selected_ship-1]["pilot_index"]
        WIN.blit(pilot_images[current_pilot_index], (pilot_x, HEIGHT // 2 - pilot_height // 2))
        
        # Draw pilot name and quote
        pilot_names = ["Ranger Alex", "Captain Vega", "Lieutenant Nova"]  # Add pilot names
        pilot_name_text = pygame.font.SysFont('Arial', 24).render(pilot_names[current_pilot_index], True, (255, 220, 0))
        WIN.blit(pilot_name_text, (pilot_x + 20, HEIGHT // 2 + pilot_height // 2 + 10))
        
        # Draw ships with animations
        for i, ship in enumerate(ship_types):
            # Update ship animation
            frame_counters[i] += 1
            if frame_counters[i] >= animation_speed:
                frame_indices[i] = (frame_indices[i] + 1) % len(ship["frames"]["idle"])
                frame_counters[i] = 0
            
            # Draw selection highlight
            if ship["id"] == selected_ship:
                highlight_rect = ship_rects[i].inflate(30, 30)
                pygame.draw.rect(WIN, (0, 255, 0), highlight_rect, 3, border_radius=10)
            
            # Draw ship animation frame
            current_frame = ship["frames"]["idle"][frame_indices[i]]
            WIN.blit(current_frame, ship_rects[i])
            
            # Draw ship name
            name_text = button_font.render(ship["name"], True, (255, 255, 255))
            WIN.blit(name_text, (ship_rects[i].centerx - name_text.get_width() // 2,
                                ship_rects[i].bottom + 10))
            
            # Draw ship stats with animated stars
            stat_y_offset = ship_rects[i].bottom + 40
            for j, (stat_name, stat_value) in enumerate(ship["stats"].items()):
                # Draw stat name
                stat_text = pygame.font.SysFont('Arial', 18).render(f"{stat_name}:", True, (200, 200, 200))
                WIN.blit(stat_text, (ship_rects[i].centerx - 80, stat_y_offset + j * 30))
                
                # Draw stars for this stat
                for k in range(5):  # 5 stars total
                    star_x = ship_rects[i].centerx - 10 + k * 25  # Adjust spacing between stars
                    star_y = stat_y_offset + j * 30
                    
                    # Draw filled or empty star based on stat value
                    if k < stat_value:
                        # Use the current animation frame for filled stars
                        WIN.blit(star_frames[star_frame_index], (star_x, star_y))
                    else:
                        WIN.blit(empty_star_img, (star_x, star_y))
            
            # Draw ship description
            desc_text = pygame.font.SysFont('Arial', 16).render(ship["description"], True, (180, 180, 180))
            WIN.blit(desc_text, (ship_rects[i].centerx - desc_text.get_width() // 2,
                                ship_rects[i].bottom + 130))
        
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
    pygame.draw.rect(WIN, (0, 0, 0), continue_button, 3)
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

    GAMEOVER_BG = pygame.image.load("assets/backgroundspaceview2.png")
    GAMEOVER_BG = pygame.transform.scale(GAMEOVER_BG, (WIDTH, HEIGHT))
   
    # Create text surfaces
    game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = button_font.render("Restart", True, (255, 255, 255))
    mainmenu_text = button_font.render("Main Menu", True, (255, 255, 255))
   
    # Create button rectangles - ADJUSTED POSITIONS
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    main_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 50)
   
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
                elif main_menu_button.collidepoint(mouse_pos):
                    return "exit"  # Use the existing "exit" return value for main menu
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()  # Actually exit the game completely
                    sys.exit()
       
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
       
        # 4. Draw main menu button
        pygame.draw.rect(WIN, (50, 50, 50), main_menu_button)
        pygame.draw.rect(WIN, (100, 100, 100), main_menu_button, 3)  # Button border
        WIN.blit(mainmenu_text, (main_menu_button.centerx - mainmenu_text.get_width() // 2,
                               main_menu_button.centery - mainmenu_text.get_height() // 2))

        # 5. Draw exit button
        pygame.draw.rect(WIN, (50, 50, 50), exit_button)
        pygame.draw.rect(WIN, (100, 100, 100), exit_button, 3)  # Button border
        exit_text = button_font.render("Quit Game", True, (255, 255, 255))
        WIN.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2,
                           exit_button.centery - exit_text.get_height() // 2))
       
        # 6. Draw cursor last
        WIN.blit(cursor_img, cursor_rect)
       
        # 7. Update display
        pygame.display.update()






