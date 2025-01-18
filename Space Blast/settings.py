import pygame

# Game Settings
WIDTH, HEIGHT = 1280, 680
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters")

BG = pygame.transform.scale(pygame.image.load("assets/Space Background.png"), (WIDTH, HEIGHT))
BG_SCROLL_SPEED = 3  # Adjust this value to control the scrolling speed
bg_y = 0  # This will track the y position of the background

# Load sound
pygame.mixer.init()
shoot_sound_player = pygame.mixer.Sound("assets/shoot_player.wav")  # Ensure this path is correct
shoot_sound_enemy = pygame.mixer.Sound("assets/shoot_enemy.wav")  # Ensure this path is correct

# Player Settings
PLAYER_WIDTH, PLAYER_HEIGHT = 128, 128
PLAYER_SPEED = 7
PLAYER_IMAGE_SHEET = pygame.image.load("assets/SPACESHIP 1.png")

FRAME_COUNT = 12
FRAME_WIDTH = PLAYER_IMAGE_SHEET.get_width() // FRAME_COUNT
FRAME_HEIGHT = PLAYER_IMAGE_SHEET.get_height()

PLAYER_FRAMES = []
for i in range (FRAME_COUNT):
    frame = PLAYER_IMAGE_SHEET.subsurface(
        pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)
    )

    frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
    PLAYER_FRAMES.append(frame)
# Enemy Settings
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 60
ENEMY_SPEED = 3
ENEMY_IMAGE = pygame.image.load("assets/enemy.png")
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Asteroid Settings
ASTEROID_WIDTH, ASTEROID_HEIGHT = 100, 100
ASTEROID_SPEED = 6
ASTEROID_IMAGE = pygame.image.load("assets/asteroid.png")
ASTEROID_IMAGE = pygame.transform.scale(ASTEROID_IMAGE, (ASTEROID_WIDTH, ASTEROID_HEIGHT))

# Bullet Settings
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
BULLET_SPEED = 7
BULLET_INTERVAL = 200  # 300 milliseconds cooldown for both player and enemies
ENEMY_BULLET_SPEED = 5  # Enemy bullet speed
ENEMY_BULLET_INTERVAL = 700  # Time interval between enemy shots in milliseconds
