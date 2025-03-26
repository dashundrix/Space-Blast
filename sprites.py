import pygame
import random
import math
from settings import *
from main import *



# Player Class
class Player:
    def __init__(self, x, y, ship_type=1):
        self.ship_type = ship_type
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # Use different frames based on ship type
        if ship_type == 1:  # Falcon
            self.frames = PLAYER_FRAMES
        elif ship_type == 2:  # Destroyer
            self.frames = PLAYER_FRAMES2
        else:  # Phantom or default
            self.frames = PLAYER_FRAMES3
        
        self.direction = "idle"
        self.frame_index = 0
        self.animation_speed = 4
        self.frame_counter = 0
        self.image = self.frames[self.direction][self.frame_index]
        
        # Set ship-specific attributes based on ship_type
        if ship_type == 1:  # Falcon
            self.speed = PLAYER_SPEED  # Normal speed
            self.lives = 10
            self.max_lives = 10
            self.bullet_power = 2
        elif ship_type == 2:  # Destroyer
            self.speed = PLAYER_SPEED - 2  # Slower
            self.lives = 1000  # More health
            self.max_lives = 12
            self.bullet_power = 1  # Stronger bullets
        elif ship_type == 3:  # Phantom
            self.speed = PLAYER_SPEED + 2  # Faster
            self.lives = 8  # Less health
            self.max_lives = 8
            self.bullet_power = 1.5  # Medium bullet power
        else:
            # Default values
            self.speed = PLAYER_SPEED
            self.lives = 10
            self.max_lives = 10
            self.bullet_power = 1
            
        # Power-up attributes
        self.powerup_active = False
        self.powerup_type = None
        self.powerup_end_time = 0
        
        # Health and powerup bar attributes
        self.health_bar_width = 300
        self.health_bar_height = 30
        self.health_bar_x = 30
        self.health_bar_y = HEIGHT - 100
        
        self.powerup_bar_width = 270
        self.powerup_bar_height = 10
        self.powerup_bar_x = 30
        self.powerup_bar_y = HEIGHT - 60
    
    # Update the move method to use the ship-specific speed
    def move(self, keys):
        moving = False
        
        # Reset direction to idle by default
        self.direction = "idle"
        
        # Horizontal movement (left and right)
        if keys[pygame.K_a] and self.rect.x - self.speed >= 0:
            self.rect.x -= self.speed
            self.direction = "left"
            moving = True
        elif keys[pygame.K_d] and self.rect.x + self.speed + self.rect.width <= WIDTH:
            self.rect.x += self.speed
            self.direction = "right"
            moving = True
        
        # Vertical movement (up and down)
        if keys[pygame.K_w] and self.rect.y - self.speed >= 0:
            self.rect.y -= self.speed
            moving = True
            if self.direction == "left":
                self.direction = "up-left"
            elif self.direction == "right":
                self.direction = "up-right"
            else:
                self.direction = "up"
        
        elif keys[pygame.K_s] and self.rect.y + self.speed + self.rect.height <= HEIGHT:
            self.rect.y += self.speed
            moving = True
            if self.direction == "left":
                self.direction = "down-left"
            elif self.direction == "right":
                self.direction = "down-right"
            else:
                self.direction = "down"
        
        # If no movement detected, set direction to idle
        if not moving:
            self.direction = "idle"
        
        # Update animation frames
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            max_frames = len(self.frames[self.direction])
            self.frame_index = (self.frame_index + 1) % max_frames
            self.frame_counter = 0
        
        # Update current frame with bounds check
        self.frame_index = min(self.frame_index, len(self.frames[self.direction]) - 1)
        self.image = self.frames[self.direction][self.frame_index]
        
    def draw(self, WIN):
        # Draw the player ship
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        
        # Draw health bar background
        pygame.draw.rect(WIN, (169, 169, 169), (self.health_bar_x, self.health_bar_y, 
                                               self.health_bar_width, self.health_bar_height), border_radius=7)
        
        # Calculate health percentage and current width
        health_percentage = self.lives / self.max_lives
        current_health_width = health_percentage * self.health_bar_width
        
        # Determine health bar color based on percentage
        health_color = (0, 255, 0) if health_percentage > 0.3 else (255, 0, 0)
        
        # Draw the filled portion of the health bar
        pygame.draw.rect(WIN, health_color, (self.health_bar_x, self.health_bar_y, 
                                            current_health_width, self.health_bar_height), border_radius=7)
        
        # Add health text
        health_text = pygame.font.SysFont('Arial', 18).render(f"HP: {int(self.lives)}/{self.max_lives}", 
                                                             True, (255, 255, 255))
        WIN.blit(health_text, (self.health_bar_x + 10, self.health_bar_y + 5))
        
        # Draw powerup duration bar if a powerup is active
        current_time = pygame.time.get_ticks()
        if self.powerup_active and current_time < self.powerup_end_time:
            # Calculate remaining time percentage
            total_duration = self.powerup_end_time - self.powerup_start_time
            remaining_time = self.powerup_end_time - current_time
            time_percentage = remaining_time / total_duration
            
            # Draw powerup bar background
            pygame.draw.rect(WIN, (50, 50, 150), (self.powerup_bar_x, self.powerup_bar_y, 
                                                 self.powerup_bar_width, self.powerup_bar_height), border_radius=7)
            
            # Draw remaining time
            current_powerup_width = time_percentage * self.powerup_bar_width
            pygame.draw.rect(WIN, (0, 100, 255), (self.powerup_bar_x, self.powerup_bar_y, 
                                                 current_powerup_width, self.powerup_bar_height), border_radius=7)
            
            # Add powerup text
            #powerup_text = pygame.font.SysFont('Arial', 14).render(f"Power Up: {int(remaining_time/1000)}s", 
                                                                 #True, (255, 255, 255))
            #WIN.blit(powerup_text, (self.powerup_bar_x + 10, self.powerup_bar_y - 15))

    def lose_life(self):
        self.lives -= 0.5

    def is_alive(self):
        return self.lives > 0
        
    def activate_powerup(self, powerup_type, duration=POWERUP1_DURATION):
        """Activate a powerup for the specified duration"""
        self.powerup_active = True
        self.powerup_type = powerup_type
        self.powerup_start_time = pygame.time.get_ticks()
        self.powerup_end_time = self.powerup_start_time + duration
        
    def update_powerups(self):
        """Check if powerups have expired"""
        current_time = pygame.time.get_ticks()
        if self.powerup_active and current_time >= self.powerup_end_time:
            self.powerup_active = False
            self.powerup_type = None
            return False  # Powerup expired
        return self.powerup_active  # Return if powerup is still active

    
# Bullet Classes Player
class Bullet:
    def __init__(self, x, y,power=1):
        self.rect = pygame.Rect(x + PLAYER_WIDTH // 2 - BULLET_WIDTH - 13 , y - PLAYERBULLET_HEIGHT + 13 , BULLET_WIDTH, BULLET_HEIGHT)
        self.frames = PLAYERBULLET1_FRAMES
        self.frame_index = 0
        self.animation_speed = 1
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]
        self.power = power



    def move(self):
        self.rect.y -= BULLET_SPEED
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0

        

        self.image = self.frames[self.frame_index]
   
    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

class BulletDual:
    def __init__(self, x, y, power=1):
        self.rect_left = pygame.Rect(x , y + PLAYERBULLET_HEIGHT // 2 - 20, BULLET_WIDTH, BULLET_HEIGHT)  # Left bullet
        self.rect_right = pygame.Rect(x + PLAYER_WIDTH // 2 + 14  , y + PLAYERBULLET_HEIGHT // 2 - 20, BULLET_WIDTH, BULLET_HEIGHT)  # Right bullet
        self.frames = PLAYERBULLET2_FRAMES
        self.frame_index = 0
        self.animation_speed = 1
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]
        self.initial_y = y
        self.spread_factor = 0.01  # Adjust this value to control spread amount
        self.power = power
    

    def move(self):
        distance_traveled = self.initial_y - self.rect_left.y
        spread_amount = distance_traveled * self.spread_factor 
        
        self.rect_left.x -= spread_amount
        self.rect_right.x += spread_amount
        
        self.rect_left.y -= BULLET_SPEED
        self.rect_right.y -= BULLET_SPEED
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0

            self.image = self.frames[self.frame_index]

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect_left.x, self.rect_left.y))  # Draw left bullet
        WIN.blit(self.image, (self.rect_right.x, self.rect_right.y))  # Draw right bullet

# Enemy Class
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.image = ENEMY_IMAGE
        self.last_shot_time = 0  # Time of the last shot in milliseconds
        self.lives = 3  # Set the number of lives for each enemy
        self.random_offset_y = random.randint(50, 100)
        self.random_offset_x = random.randint(10, 30)
        self.sway_direction = 1  # Start swaying to the right
        self.sway_distance = 0
        self.max_sway_distance = 60  # Maximum sway in pixels

    def move(self, player):
        if self.rect.x < player.rect.x - self.random_offset_x:
            self.rect.x += ENEMY_SPEED
        elif self.rect.x > player.rect.x + self.random_offset_x:
            self.rect.x -= ENEMY_SPEED
        if self.rect.y < player.rect.y - self.random_offset_y:
            self.rect.y += ENEMY_SPEED
        elif self.rect.y > player.rect.y + (self.random_offset_y - 300):
            self.rect.y -= ENEMY_SPEED

         # Sway/jiggle movement when the enemy is roughly in front of the player
        if abs(self.rect.x - player.rect.x) < self.random_offset_x:
            self.rect.x += self.sway_direction * ENEMY_SPEED

         # Reverse direction when reaching the max sway distance
            self.sway_distance += self.sway_direction * ENEMY_SPEED
        if abs(self.sway_distance) >= self.max_sway_distance:
            self.sway_direction *= -1  # Change sway direction

    def shoot(self, current_time):
        if current_time - self.last_shot_time > ENEMY_BULLET_INTERVAL:
            self.last_shot_time = current_time
            return EnemyBullet(self.rect.x + ENEMY_WIDTH // 2 - BULLET_WIDTH // 2, self.rect.y + ENEMY_HEIGHT)
        return None

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

    def take_damage(self):
        """Reduce the enemy's life when hit by a bullet."""
        self.lives -= 1
        if self.lives <= 0:
            
            return True  # Enemy should be destroyed
        return False

class Boss1:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BOSS_WIDTH, BOSS_HEIGHT)
        self.frames = BOSS1_FRAMES
        self.frame_index = 0
        self.animation_speed = 6
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]
        self.health = 500
        self.max_health = 500
        self.movement_pattern = 0
        self.shoot_timer = 0
        self.shoot_delay = 3000
        self.phase = 1

    def move(self):
        # Phase 1: Side to side movement
        if self.rect.y < 90:  # Move down until it reaches y = 100
            self.rect.y += 2
        
        if self.phase == 1:
            
            if self.movement_pattern == 0:
                self.rect.x += 3
                
                if self.rect.x > WIDTH - BOSS_WIDTH:
                    self.movement_pattern = 1
                if self.rect.y == - HEIGHT - BOSS_HEIGHT:
                    self.rect.y += 2

            else:
                self.rect.x -= 3
                if self.rect.x < 0:
                    self.movement_pattern = 0

        # Phase 2: Diagonal movement (activates at 50% health)
        elif self.phase == 2:
            if self.movement_pattern == 0:
                self.rect.x += 4
                self.rect.y += 2
                if self.rect.x > WIDTH - BOSS_WIDTH or self.rect.y > HEIGHT//2:
                    self.movement_pattern = 1
            else:
                self.rect.x -= 4
                self.rect.y -= 2
                if self.rect.x < 0 or self.rect.y < 0:
                    self.movement_pattern = 0

        # Update animation
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0
            self.image = self.frames[self.frame_index]

    def shoot(self, current_time):
        bullets = []
        if current_time - self.shoot_timer > self.shoot_delay:
            # Define gun positions relative to boss center
            gun_positions = [
                # Center guns (2)
                (-20, self.rect.height - 20),  # Left center gun
                (20, self.rect.height - 20),   # Right center gun
                
                # Left wing guns (2)
                (-self.rect.width//3, self.rect.height),     # Outer left gun
                (-self.rect.width//4 + 30, self.rect.height - 30),   # Inner left gun
                
                # Right wing guns (2)
                (self.rect.width//3, self.rect.height),      # Outer right gun
                (self.rect.width//4 - 30, self.rect.height - 30)     # Inner right gun
            ]
            
            if self.phase == 1:
                # Phase 1: Alternating patterns
                pattern_cycle = (current_time // 5000) % 5  # Change pattern every 3 seconds
                
                if pattern_cycle == 0:
                    # Straight shots
                    for x_offset, y_offset in gun_positions:
                        bullets.append(BossBullet1(
                            self.rect.centerx + x_offset, 
                            self.rect.y + y_offset, 
                            0,  # Straight down
                            "straight"
                        ))
                elif pattern_cycle == 1:
                    # Sine wave shots
                    for x_offset, y_offset in gun_positions:
                        bullets.append(BossBullet1(
                            self.rect.centerx + x_offset, 
                            self.rect.y + y_offset, 
                            0,
                            "sine"
                        ))
                else:
                    # Spiral shots from center guns only
                    for x_offset, y_offset in gun_positions[:2]:  # Center guns
                        bullets.append(BossBullet1(
                            self.rect.centerx + x_offset, 
                            self.rect.y + y_offset, 
                            0,
                            "spiral"
                        ))
            
            elif self.phase == 2:
                # Phase 2: More complex patterns
                # Center guns fire spiral patterns
                for x_offset, y_offset in gun_positions[:2]:  # Center guns
                    bullets.append(BossBullet1(
                        self.rect.centerx + x_offset, 
                        self.rect.y + y_offset, 
                        0,
                        "spiral"
                    ))
                
                # Wing guns fire sine wave patterns
                for x_offset, y_offset in gun_positions[2:]:  # Wing guns
                    # Left side
                    bullets.append(BossBullet1(
                        self.rect.centerx + x_offset, 
                        self.rect.y + y_offset, 
                        -30 if x_offset < 0 else 30,  # Angle based on which side
                        "sine"
                    ))
            
            self.shoot_timer = current_time
        
        return bullets


    def take_damage(self, damage):
        self.health -= damage
        if self.health <= self.max_health * 0.5 and self.phase == 1:
            self.phase = 2
            self.shoot_delay = 2000  # Faster shooting in phase 2
        elif self.health <= self.max_health * 0.25 and self.phase == 2:
            self.phase = 3
            self.shoot_delay = 1500  # Slower but more bullets in phase 3

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

            # Draw health bar above the boss
        health_bar_width = BOSS_WIDTH
        health_bar_height = 10  # Small height as requested
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y - 15  # Position above the boss
        
        # Draw background (empty health)
        pygame.draw.rect(WIN, (169, 169, 169), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        # Draw filled portion based on current health
        health_percentage = self.health / self.max_health  # Assuming max health is 100
        current_health_width = health_percentage * health_bar_width
        
        # Color changes from green to yellow to red as health decreases
        if health_percentage > 0.6:
            health_color = (0, 255, 0)  # Green
        elif health_percentage > 0.3:
            health_color = (255, 255, 0)  # Yellow
        else:
            health_color = (255, 0, 0)  # Red
            
        pygame.draw.rect(WIN, health_color, (health_bar_x, health_bar_y, current_health_width, health_bar_height))

class BossBullet1:
    def __init__(self, x, y, direction, pattern="straight"):
        self.rect = pygame.Rect(x - BOSS1_BULLET_WIDTH // 2, y, BOSS1_BULLET_WIDTH, BOSS1_BULLET_HEIGHT)
        self.frames = BOSS1_BULLET1_FRAMES
        self.frame_index = 0
        self.animation_speed = 5
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]
        self.direction = direction  # Angle in degrees or simple direction (-1, 0, 1)
        self.pattern = pattern  # Movement pattern: "straight", "sine", "spiral", "homing"
        self.speed = BOSS_BULLET_SPEED
        self.age = 0  # Track how long the bullet has existed
        self.origin_x = x  # Remember starting position for patterns
        self.origin_y = y
        self.amplitude = 50  # For sine wave pattern
        self.frequency = 0.05  # For sine wave pattern
        self.spiral_radius = 1.5  # Starting radius for spiral pattern
        self.spiral_growth = 0.3  # How much the radius grows per frame
        
    def move(self):
        self.age += 1
        
        if self.pattern == "straight":
            # Simple straight movement based on angle
            if self.direction in [-2, -1, 0, 1, 2]:
                # Simple directional movement
                self.rect.x += self.direction * (self.speed // 2)
                self.rect.y += self.speed
            else:
                # Angular movement
                angle_rad = math.radians(self.direction)
                self.rect.x += math.cos(angle_rad) * self.speed
                self.rect.y += math.sin(angle_rad) * self.speed
                
        elif self.pattern == "sine":
            # Sine wave pattern
            # Move downward while oscillating horizontally
            self.rect.y += self.speed
            # Calculate horizontal position based on sine wave
            self.rect.x = self.origin_x + math.sin(self.age * self.frequency) * self.amplitude
            
        elif self.pattern == "spiral":
            # Spiral outward pattern
            angle_rad = math.radians(self.age * 10)  # Rotate 10 degrees per frame
            radius = self.spiral_radius + (self.age * self.spiral_growth)
            
            # Calculate new position based on spiral
            self.rect.x = self.origin_x + math.cos(angle_rad) * radius
            self.rect.y = self.origin_y + math.sin(angle_rad) * radius
            
        elif self.pattern == "homing":
            # This would require player position, so we'll implement a simpler version
            # that just accelerates downward
            self.rect.y += self.speed * (1 + self.age * 0.01)
        
        # Update animation
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0
            
        self.image = self.frames[self.frame_index]
        
    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

# Asteroid Class
class Asteroid:
    def __init__(self, x, y):
        # Get random frames for the asteroid from the settings
        self.frames = get_random_asteroid_frames()
        self.frame_index = 0
        self.animation_speed = 10
        self.frame_counter = 0
        self.rect = pygame.Rect(x, y, ASTEROID_WIDTH, ASTEROID_HEIGHT)
        self.image = self.frames[self.frame_index]
        self.horizontal_direction = random.choice([-1, -0.5, 0, 0.5, 1])
        self.horizontal_speed = random.uniform(1, 3)

    def move(self):
        self.rect.y += ASTEROID_SPEED
        self.rect.x += self.horizontal_direction * self.horizontal_speed
        
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0
        
        self.image = self.frames[self.frame_index]

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

class EnemyBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x , y, BULLET_WIDTH, BULLET_HEIGHT)
        self.frames = ENEMYBULLET1_FRAMES
        self.frame_index = 0
        self.animation_speed = 1
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]

    def move(self):
        self.rect.y += ENEMY_BULLET_SPEED
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0
        

        self.image = self.frames[self.frame_index]
   
    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))





class Explosion:
    def __init__(self, x, y, duration=300):  # Duration in milliseconds
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()  # Start time for the animation
        self.duration = duration
        self.current_frame = 0  # Start with the first frame
        self.frame_time = duration // EXPLOSION_FRAME_COUNT + 100 # Time per frame

    def is_expired(self, current_time):
        # Check if the explosion animation's total duration has elapsed
        return current_time - self.start_time > self.duration

    def draw(self, surface):
        # Calculate the current frame based on elapsed time
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.current_frame = (elapsed_time // self.frame_time) % EXPLOSION_FRAME_COUNT

        # Draw the current frame of the explosion
        if self.current_frame < len(EXPLOSION_FRAMES):  # Ensure within bounds
            frame_image = EXPLOSION_FRAMES[self.current_frame]
            surface.blit(frame_image, (self.x, self.y))

class PowerUpDualGun:
    def __init__(self, x, y, power_type = 'dual_gun'):
        self.rect = pygame.Rect(x, y, POWERUP_WIDTH, POWERUP_HEIGHT)
        self.power_type = power_type
        self.frames = POWERUPDUALGUN_FRAMES
        self.frame_index = 0
        self.animation_speed = 5
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]
        self.horizontal_direction = random.choice([-0.5, -0.2, 0, 0.2, 0.5])
        self.horizontal_speed = random.uniform(1, 3)
    
    def move(self):
        self.rect.y += POWERUP_SPEED
        self.rect.x += self.horizontal_direction * self.horizontal_speed
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)  # Wrap around the index
            self.frame_counter = 0

        self.image = self.frames[self.frame_index]

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
