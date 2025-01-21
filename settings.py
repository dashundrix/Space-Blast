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
PLAYERBULLET1_IMAGE_SHEET = pygame.image.load("assets/Bullet 1.png")


PLAYER_FRAME_COUNT = 12
FRAME_WIDTH = PLAYER_IMAGE_SHEET.get_width() // PLAYER_FRAME_COUNT
FRAME_HEIGHT = PLAYER_IMAGE_SHEET.get_height()

PLAYERBULLET_WIDTH, PLAYERBULLET_HEIGHT = 25,30 

PLAYERBULLET1_FRAME_COUNT = 4
PLAYERBULLET1_FRAME_WIDTH = PLAYERBULLET1_IMAGE_SHEET.get_width() // PLAYERBULLET1_FRAME_COUNT
PLAYERBULLET1_FRAME_HEIGHT = PLAYERBULLET1_IMAGE_SHEET.get_height()


PLAYER_FRAMES = []
for i in range (PLAYER_FRAME_COUNT):
    frame = PLAYER_IMAGE_SHEET.subsurface(
        pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)
    )

    frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
    PLAYER_FRAMES.append(frame)

PLAYERBULLET1_FRAMES = []
for i in range(PLAYERBULLET1_FRAME_COUNT):  # Ensure PLAYERBULLET1_FRAME_COUNT is defined
    frame = PLAYERBULLET1_IMAGE_SHEET.subsurface(
        pygame.Rect(i * PLAYERBULLET1_FRAME_WIDTH, 0, PLAYERBULLET1_FRAME_WIDTH, PLAYERBULLET1_FRAME_HEIGHT)
    )
    frame = pygame.transform.scale(frame, (PLAYERBULLET_WIDTH, PLAYERBULLET_HEIGHT))  # Scale to bullet size
    PLAYERBULLET1_FRAMES.append(frame)

# Enemy Settings
ENEMY_WIDTH, ENEMY_HEIGHT = 64, 64
ENEMY_SPEED = 3
ENEMY_IMAGE = pygame.image.load("assets/enemy.png")
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Asteroid Settings
ASTEROID_WIDTH, ASTEROID_HEIGHT = 150, 150
ASTEROID_SPEED = 6
ASTEROID_IMAGE = pygame.image.load("assets/asteroid.png")
ASTEROID_IMAGE = pygame.transform.scale(ASTEROID_IMAGE, (ASTEROID_WIDTH, ASTEROID_HEIGHT))

# Bullet Settings
BULLET_WIDTH, BULLET_HEIGHT = 10, 15
BULLET_SPEED = 10
BULLET_INTERVAL = 100  # 300 milliseconds cooldown for both player and enemies
ENEMY_BULLET_SPEED = 10  # Enemy bullet speed
ENEMY_BULLET_INTERVAL = 180  # Time interval between enemy shots in milliseconds
