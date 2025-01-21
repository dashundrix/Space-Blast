import pygame
import random
from settings import *
from main import *



# Player Class
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.frames = PLAYER_FRAMES
        self.frame_index = 0
        self.animation_speed = 4
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]

        self.lives = 12  # Starting lives

    def move(self, keys):
        moving = False
      
        if keys[pygame.K_a] and self.rect.x - PLAYER_SPEED >= 0:
            self.rect.x -= PLAYER_SPEED
            moving = True
        if keys[pygame.K_d] and self.rect.x + PLAYER_SPEED + self.rect.width <= WIDTH:
            self.rect.x += PLAYER_SPEED
            moving = True
        if keys[pygame.K_w] and self.rect.y - PLAYER_SPEED >= 0:
            self.rect.y -= PLAYER_SPEED
            moving = True
        if keys[pygame.K_s] and self.rect.y + PLAYER_SPEED + self.rect.height <= HEIGHT:
            self.rect.y += PLAYER_SPEED
            moving = True

        # Idle Animation Logic
        if not moving:  # If no movement, cycle through idle frames
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.frame_counter = 0
        else:
            self.frame_index = 0  # Reset to frame 0 when moving

        # Update Current Frame
        self.image = self.frames[self.frame_index]
    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

    def lose_life(self):
        self.lives -= 1

    def is_alive(self):
        return self.lives > 0
    
# Bullet Classes Player
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + PLAYER_WIDTH // 2 - BULLET_WIDTH , y, BULLET_WIDTH, BULLET_HEIGHT)
        self.frames = PLAYERBULLET1_FRAMES
        self.frame_index = 0
        self.animation_speed = 1
        self.frame_counter = 0
        self.image = self.frames[self.frame_index]



    def move(self):
        self.rect.y -= BULLET_SPEED
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.frame_counter = 0

        else:
            self.frame_index = 0
        

        self.image = self.frames[self.frame_index]
    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))


# Enemy Class
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.image = ENEMY_IMAGE
        self.last_shot_time = 0  # Time of the last shot in milliseconds
        self.lives = 3  # Set the number of lives for each enemy
        self.random_offset_y = random.randint(50, 250)
        self.random_offset_x = random.randint(10, 30)

    def move(self, player):
        if self.rect.x < player.rect.x - self.random_offset_x:
            self.rect.x += ENEMY_SPEED
        elif self.rect.x > player.rect.x + self.random_offset_x:
            self.rect.x -= ENEMY_SPEED
        if self.rect.y < player.rect.y - self.random_offset_y:
            self.rect.y += ENEMY_SPEED
        elif self.rect.y > player.rect.y + (self.random_offset_y - 300):
            self.rect.y -= ENEMY_SPEED

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


# Asteroid Class
class Asteroid:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ASTEROID_WIDTH, ASTEROID_HEIGHT)
        self.image = ASTEROID_IMAGE

    def move(self):
        self.rect.y += ASTEROID_SPEED

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))





class EnemyBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x , y, BULLET_WIDTH, BULLET_HEIGHT)

    def move(self):
        self.rect.y += ENEMY_BULLET_SPEED

    def draw(self, WIN):
        pygame.draw.rect(WIN, "red", self.rect)

class Explosion:
    def __init__(self, x, y, duration=200):  # Duration in milliseconds
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.image = pygame.transform.scale(
            pygame.image.load("assets/explosion.png"), (40, 40)
        ) 

    def is_expired(self, current_time):
        return current_time - self.start_time > self.duration

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))  # Draw the image