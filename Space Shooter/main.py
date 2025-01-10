import pygame
import random
import sys
from settings import *
from sprites import *

# Drawing Function
def draw(WIN, BG, player, enemies, bullets, enemy_bullets, asteroids, explosions):
    WIN.blit(BG, (0, 0))
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
    life_text = font.render("LIFE: ", True, (255, 255, 255))
    WIN.blit(life_text, (790, 40))

    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = 790
    health_bar_y = 20

    pygame.draw.rect(WIN, (169, 169, 169), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

    health_percentage = player.lives / 10
    current_health_width = health_percentage * health_bar_width
    pygame.draw.rect(WIN, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

    pygame.display.update()


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
    enemies = [Enemy(random.randint(0, WIDTH - ENEMY_WIDTH), -100) for _ in range(2)]
    bullets = []
    enemy_bullets = []
    asteroids = []
    explosions = []

    last_bullet_time = 0

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not player.is_alive():
            display_game_over(WIN)
            break

        keys = pygame.key.get_pressed()
        player.move(keys)

        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > BULLET_INTERVAL:
            bullets.append(Bullet(player.rect.x, player.rect.y))
            last_bullet_time = current_time
            shoot_sound_player.play()

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

                    bullets.remove(bullet)  # Remove the bullet after collision
                    break

            enemy_bullet = enemy.shoot(current_time)
            if enemy_bullet:
                enemy_bullets.append(enemy_bullet)
                shoot_sound_enemy.play()

        # Move Asteroids
        if random.randint(1, 100) <= 2:
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

        draw(WIN, BG, player, enemies, bullets, enemy_bullets, asteroids, explosions)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
