import pygame
import random
import sys
import settings
from settings import *
from sprites import *
from screens import *



# Drawing Function
def draw(WIN, CURRENT_BG, player, enemies, bullets, dual_bullets, powerup_dualgun,
         enemy_bullets, asteroids, explosions, bg_y, score, gamelevel, boss, boss1_spawned ):
    # Clear the screen first
    WIN.fill((0, 0, 0))
    
    # Draw the first background
    WIN.blit(settings.CURRENT_BG, (0, bg_y))  
    # Draw the second background just below the first one
    
    WIN.blit(settings.CURRENT_BG, (0, bg_y - HEIGHT))   

    # Check if the background has scrolled off screen, and reset it
    if bg_y >= HEIGHT:
        bg_y = 0  # Reset the background position when it reaches the height of the screen
    
    player.draw(WIN)
    
    if boss1_spawned and boss is not None:    
        boss.draw(WIN)
        
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

    for dual_bullet in dual_bullets:
        dual_bullet.draw(WIN)
    for powerup1 in powerup_dualgun:
        powerup1.draw(WIN)

    #Powerrup Mana
    mana_bar_width = 270
    mana_bar_height = 10
    mana_bar_x = 30
    mana_bar_y = HEIGHT - 60

    pygame.draw.rect(WIN, ("blue"), (mana_bar_x, mana_bar_y, mana_bar_width, mana_bar_height))
    
    # Display Health Bar
    health_bar_width = 300
    health_bar_height = 30
    health_bar_x = 30
    health_bar_y = HEIGHT - 100
    
    pygame.draw.rect(WIN, (169, 169, 169), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

    health_percentage = player.lives / 10
    current_health_width = health_percentage * health_bar_width

    health_color = (0, 255, 0) if health_percentage > 0.3 else (255, 0, 0)
    pygame.draw.rect(WIN, health_color, (health_bar_x, health_bar_y, current_health_width, health_bar_height))

    score_text = pygame.font.SysFont('Arial', 50).render(f"{score}", True, (255, 255, 255))
    #current_level = pygame.font.SysFont('Arial', 24).render(f"Level {gamelevel}", True, (255, 255, 255))
   
    WIN.blit(score_text, (WIDTH //2 , 10))
    #WIN.blit(current_level, (10, 60))
   
    pygame.display.update()
    return bg_y  # Return the updated bg_y to continue scrolling

# Main Game Loop
def main():
    run = True
    clock = pygame.time.Clock()
   
    global gamelevel
    gamelevel = 1
    
    player = Player(500, 350)
    enemies = [Enemy(random.randint(0, WIDTH - ENEMY_WIDTH), -100) for _ in range(1 + gamelevel // 2)]
    boss = False
    bullets = []
    dual_bullets = []
    enemy_bullets = []
    asteroids = []
    explosions = []
    powerup_dualgun = []
    
    previous_score = 0
    score = 0
    boss1_spawned = False

    powerup1_interval = 5000
    last_bullet_time = 0
    last_dual_bullet_time = 0
    last_powerup1_time = 0
    current_bullet_interval = settings.BULLET_INTERVAL
    
    dualfire_end_time = 0

    dualfire = False
    singlefire = True
    
    bg_y = 0  # Start the background position at the top
    game_paused = False
    map_speed = settings.BG_SCROLL_SPEED
   
    play_button, difficulty_button, exit_button, bg_y = display_title_screen(WIN, BG, bg_y)
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
                    settings.play_game_music()
                elif difficulty_button.collidepoint(event.pos):
                    # Add difficulty selection logic here
                    pass
                elif exit_button.collidepoint(event.pos):
                    run = False
                    game_started = True
                
       
        # Continuously update the background position to scroll it
        bg_y += 1  # Increase the vertical position for scrolling effect
        if bg_y >= HEIGHT:  # Reset background when it scrolls off the screen
            bg_y = 0
        # Redraw the title screen with updated background position
        play_button, difficulty_button, exit_button, bg_y = display_title_screen(WIN, BG, bg_y)

        # Refresh the screen after drawing the title screen with updated bg_y
        pygame.display.update()

    # Track the previous state of the ESC key
    prev_esc_state = False

    # Main game loop
    while run:
        clock.tick(60)

        
        time = pygame.time.get_ticks() / 1000  # Get time in seconds
       
        
        if score >= 300 * (gamelevel) and score != previous_score:
            gamelevel += 1
            previous_score = score  # Update the previous score to prevent continuous level increase
            map_speed += 3  # Increase map speed for the new level

            
            # ///// BACKGROUND CHANGE ///// AnyLogic can apply 
            # Add background changing logic here
            if True:  # Even levels
                settings.CURRENT_BG = settings.BG
                print("Changed to BG1")
            else:  # Odd levels
                settings.CURRENT_BG = settings.BG
                print("Changed to BG")
            # Reset and update the enemies list for the new level
            enemies = [Enemy(random.randint(0, WIDTH - ENEMY_WIDTH), -100) for _ in range(gamelevel)]

        # Spawn the boss after 10 seconds
        if time >= 20 and not boss1_spawned:
            boss1_spawned = True
            boss = Boss1(WIDTH // 2 - BOSS_WIDTH // 2, -300)  # Initialize the boss
            print("Boss spawned!")  # Debugging: Confirm boss spawn

        if boss1_spawned and boss is not None:
            boss.move()  # Move the boss if it has been spawned
        
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
        
        # Spawn power-ups at random intervals
        if current_time - last_powerup1_time > powerup1_interval:
            powerup_x = random.randint(0, WIDTH - POWERUP_WIDTH)
            powerup_y = random.randint(-100, -50)  # Start above the screen
            powerup_dualgun.append(PowerUpDualGun(powerup_x, powerup_y))
            last_powerup1_time = current_time
            powerup1_interval = random.randint(7000, 13000)  # Randomize next spawn interval
                
            # Check for collision between player and enemies

        # Update and handle power-up behavior
        for powerup1 in powerup_dualgun[:]:
            powerup1.move()
            if powerup1.rect.colliderect(player.rect):  # Player collects power-up
                random_effect = random.randint(1, 4)
                
                if random_effect == 1:
                    dualfire = True
                    singlefire = False
                    print("Dual Machingun")
                elif random_effect == 2:
                    dualfire = True
                    singlefire = True
                    print("Triple Machingun")
                elif random_effect == 3:
                    current_bullet_interval = 130  # Set the current interval directly
                    settings.BULLET_INTERVAL = 130  # Keep settings in sync
                    print(f"New BULLET_INTERVAL: {settings.BULLET_INTERVAL}")

                elif random_effect == 4:
                  player.lives += 2
                  if player.lives > 10:
                      player.lives = 10
                print("HEALTH +")

                    
                dualfire_end_time = current_time + DUALFIRE_DURATION  # Set duration
                powerup_dualgun.remove(powerup1)
            elif powerup1.rect.y > HEIGHT:  # Remove off-screen power-ups
                powerup_dualgun.remove(powerup1)
        # Check if dualfire duration has ended
        if dualfire and current_time > dualfire_end_time:
            dualfire = False
            singlefire = True
            current_bullet_interval = 200  # Set the current interval directly
            settings.BULLET_INTERVAL = 200  # Keep settings in sync
    
       
        if singlefire == True : # Single Bullet Firing
            if current_time - last_bullet_time > current_bullet_interval:
                bullets.append(Bullet(player.rect.x, player.rect.y))
                last_bullet_time = current_time
                shoot_sound_player.play()

        if dualfire == True : # Dual Bullet Firing (testing mode — always enabled)
            if current_time - last_dual_bullet_time > current_bullet_interval:  # Use a separate timer for dual bullets
                dual_bullets.append(BulletDual(player.rect.x, player.rect.y))
                last_dual_bullet_time = current_time
                shoot_sound_player.play()

        # Move and draw regular bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.y < 0:
                bullets.remove(bullet)
            bullet.draw(WIN)

        # Move and draw dual bullets
        for dual_bullet in dual_bullets[:]:
            dual_bullet.move()
            if dual_bullet.rect_left.y < 0 and dual_bullet.rect_right.y < 0:  # Remove if both are off-screen
                dual_bullets.remove(dual_bullet)
            dual_bullet.draw(WIN)

        # Move Enemies
        for enemy in enemies[:]:
            enemy.move(player)
            enemy_removed = False  # Flag to track if the enemy is already removed

            # Check collision with regular bullets
            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.take_damage()  # Decrease the enemy's health by 1
                    if enemy.take_damage():
                        explosions.append(Explosion(enemy.rect.centerx - 10, enemy.rect.centery - 10))
                        enemies.remove(enemy)  # Remove the enemy
                        enemies.append(Enemy(random.randint(0, WIDTH - ENEMY_WIDTH), -100))
                        score += 10  # Increase score when an enemy is killed
                        enemy_removed = True  # Mark enemy as removed
                    bullets.remove(bullet)  # Remove the bullet after collision
                    break  # Exit bullet loop if collision occurs


            if enemy_removed:
                continue  # Skip checking dual bullets if the enemy is already removed

            # Check collision with dual bullets
            for dual_bullet in dual_bullets[:]:
                if enemy.rect.colliderect(dual_bullet.rect_left) or enemy.rect.colliderect(dual_bullet.rect_right):
                    enemy.take_damage()  # Decrease the enemy's health by 1
                    if enemy.take_damage():
                        explosions.append(Explosion(enemy.rect.centerx - 10, enemy.rect.centery - 10))
                        enemies.remove(enemy)  # Remove the enemy
                        enemies.append(Enemy(random.randint(0, WIDTH - ENEMY_WIDTH), -100))
                        score += 10  # Increase score when an enemy is killed
                        enemy_removed = True  # Mark enemy as removed
                    dual_bullets.remove(dual_bullet)  # Remove the dual bullet after collision
                    break  # Exit dual bullet loop if collision occurs

            if enemy_removed:
                continue  # Skip processing this enemy further

            # Enemy shooting logic
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
                explosions.append(Explosion(player.rect.centerx - 10, player.rect.centery - 10))
                enemy_bullets.remove(enemy_bullet)

        # Manage Explosions
        for explosion in explosions[:]:
            if explosion.is_expired(current_time):
                explosions.remove(explosion)

        # Scroll Map background
        bg_y += map_speed 
        

        bg_y = draw(WIN, settings.CURRENT_BG, player, enemies, bullets, dual_bullets, 
                    powerup_dualgun, enemy_bullets, asteroids, explosions, bg_y, score, gamelevel, boss,  boss1_spawned)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
