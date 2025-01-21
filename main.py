import pygame
import random
import sys
from settings import *
from sprites import *

# Function to display the title screen
def display_title_screen(WIN, BG, bg_y):
    # Create font and title text
    font = pygame.font.SysFont('Arial', 60)
    title_text = font.render("SPACE BLAST", True, (255, 255, 255))
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    
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

    pygame.draw.rect(WIN, (0, 255, 0), play_button)  # Draw the "Play" button
    play_text = pygame.font.SysFont('Arial', 30).render("Play", True, (0, 0, 0))
    WIN.blit(play_text, (play_button.x + (play_button.width - play_text.get_width()) // 2, play_button.y + (play_button.height - play_text.get_height()) // 2))

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
# Drawing Function
def draw(WIN, BG, player, enemies, bullets, enemy_bullets, asteroids, explosions, bg_y):
    # Draw the first background
    WIN.blit(BG, (0, bg_y))  
    # Draw the second background just below the first one
    WIN.blit(BG, (0, bg_y - HEIGHT))  

    # Check if the background has scrolled off screen, and reset it
    if bg_y >= HEIGHT:
        bg_y = 0  # Reset the background position when it reaches the height of the screen

    player.draw(WIN)
    for enemy in enemies:
        enemy.draw(WIN)
    for bullet in bullets:
        bullet.draw(WIN)
    for enemy_bullet in enemy_bullets:
        enemy_bullet.draw(WIN)
    for asteroid in asteroids:
        asteroid.draw(WIN)
    for explosion in explosions:
        explosion.draw(WIN)

    # Display Health Bar
    font = pygame.font.SysFont('Arial', 24)
    life_text = font.render("Life ", True, (255, 255, 255))
    life_text_width = life_text.get_width()

    # Position the "Life" text on the left
    life_text_x =   WIDTH  - life_text_width - 220
    WIN.blit(life_text, (life_text_x, 20))

    # Position the health bar right next to the "Life" text
    health_bar_x = life_text_x + life_text_width + 10   

    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = WIDTH - health_bar_width - 20
    health_bar_y = 20

    pygame.draw.rect(WIN, (169, 169, 169), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

    health_percentage = player.lives / 10
    current_health_width = health_percentage * health_bar_width

    health_color = (0, 255, 0) if health_percentage > 0.3 else (255, 0, 0)
    pygame.draw.rect(WIN, health_color, (health_bar_x, health_bar_y, current_health_width, health_bar_height))

    pygame.display.update()
    return bg_y  # Return the updated bg_y to continue scrolling

# Game Over Display
def display_game_over(WIN):
    font = pygame.font.SysFont('Arial', 60)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# Main Game Loop
def main():
    run = True
    clock = pygame.time.Clock()

    player = Player(500, 350)
    enemies = [Enemy(random.randint(0, WIDTH - ENEMY_WIDTH), -100) for _ in range(1)]
    bullets = []
    enemy_bullets = []
    asteroids = []
    explosions = []
    score = 0
    last_bullet_time = 0
    bg_y = 0  # Start the background position at the top
    game_paused = False

    
    play_button, bg_y = display_title_screen(WIN, BG, bg_y)
    # Wait for player to click play button to start
    
    game_started = False
    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_started = True  # End the loop if quitting
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):  # Check if the play button was clicked
                    game_started = True  # Proceed to game loop after clicking play
                    game_paused = False  # Ensure it's not paused when game starts
        
        # Continuously update the background position to scroll it
        bg_y += 1  # Increase the vertical position for scrolling effect
        if bg_y >= HEIGHT:  # Reset background when it scrolls off the screen
            bg_y = 0
        # Redraw the title screen with updated background position
        play_button, bg_y = display_title_screen(WIN, BG, bg_y)

        # Refresh the screen after drawing the title screen with updated bg_y
        pygame.display.update()

    # Track the previous state of the ESC key
    prev_esc_state = False

    # Main game loop
    while run:
        clock.tick(60)

        # Pause handling (toggle pause on ESC press)
        keys = pygame.key.get_pressed()

        # Only toggle pause when the ESC key is first pressed
        if keys[pygame.K_ESCAPE] and not prev_esc_state:
            game_paused = not game_paused  # Toggle pause state
            prev_esc_state = True  # Set the previous ESC state to True when pressed

        # Reset prev_esc_state when ESC is released
        if not keys[pygame.K_ESCAPE]:
            prev_esc_state = False

        if game_paused:
            continue_button, exit_button = display_pause_screen(WIN)  # Show the pause screen with buttons

            # Wait for mouse clicks on the buttons
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):  # Check if Continue button is clicked
                        game_paused = False  # Unpause the game
                    elif exit_button.collidepoint(event.pos):  # Check if Exit button is clicked
                        run = False  # Exit the game

            continue  # Skip the rest of the loop and only update the pause screen

        # Game loop (running when not paused)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not player.is_alive():
            display_game_over(WIN)
            break

        # Game logic will only run if the game is not paused
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Automatically shoot continuously at regular intervals
        current_time = pygame.time.get_ticks()

        if current_time - last_bullet_time > BULLET_INTERVAL:
            bullets.append(Bullet(player.rect.x, player.rect.y))  # Fire bullet
            last_bullet_time = current_time  # Update the last bullet shot time
            shoot_sound_player.play()  # Play shoot sound

        # Move Bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.y < 0:
                bullets.remove(bullet)

        # Move Enemies
        for enemy in enemies[:]:
            enemy.move(player)
            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.take_damage()  # Decrease the enemy's health by 1

                    # Create explosion only when the enemy dies
                    if enemy.take_damage():
                        explosions.append(Explosion(enemy.rect.centerx - 10, enemy.rect.centery - 10))
                        enemies.remove(enemy)
                        enemies.append(Enemy(random.randint(0, WIDTH - ENEMY_WIDTH), -100))
                        score += 10  # Increase score when an enemy is killed
                    bullets.remove(bullet)  # Remove the bullet after collision
                    break

            enemy_bullet = enemy.shoot(current_time)
            if enemy_bullet:
                enemy_bullets.append(enemy_bullet)
                shoot_sound_enemy.play()

        # Move Asteroids
        if random.randint(1, 100) <= 1:
            asteroids.append(Asteroid(random.randint(0, WIDTH - ASTEROID_WIDTH), -ASTEROID_HEIGHT))

        for asteroid in asteroids[:]:
            asteroid.move()
            if asteroid.rect.y > HEIGHT:
                asteroids.remove(asteroid)

            if player.rect.colliderect(asteroid.rect):
                explosions.append(Explosion(player.rect.centerx - 10, player.rect.centery - 10))
                asteroids.remove(asteroid)
                player.lose_life()

        # Move Enemy Bullets
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move()
            if enemy_bullet.rect.y > HEIGHT:
                enemy_bullets.remove(enemy_bullet)

            if player.rect.colliderect(enemy_bullet.rect):
                player.lose_life()
                enemy_bullets.remove(enemy_bullet)

        # Manage Explosions
        for explosion in explosions[:]:
            if explosion.is_expired(current_time):
                explosions.remove(explosion)

        # Scroll Map background
        bg_y += BG_SCROLL_SPEED  

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        WIN.blit(score_text, (10, 10))
        
        bg_y = draw(WIN, BG, player, enemies, bullets, enemy_bullets, asteroids, explosions, bg_y)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
