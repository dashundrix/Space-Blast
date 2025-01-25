import pygame
import random



# Game Settings
WIDTH, HEIGHT = 1280, 680
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters")

BG = pygame.transform.scale(pygame.image.load("assets/Space Background.png"), (WIDTH, HEIGHT))
BG1 = pygame.transform.scale(pygame.image.load("assets/Space Background1.png"), (WIDTH, HEIGHT))

CURRENT_BG = BG # Changing the map

BG_SCROLL_SPEED = 3  # Adjust this value to control the scrolling speed
bg_y = 0  # This will track the y position of the background



# Load sound
pygame.mixer.init()
shoot_sound_player = pygame.mixer.Sound("assets/shoot_player.wav")  # Ensure this path is correct
shoot_sound_enemy = pygame.mixer.Sound("assets/shoot_enemy.wav")  # Ensure this path is correct
normal_bg = pygame.mixer.Sound("assets/normal bgm.mp3")  # Ensure this path is correct


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
ENEMY_SPEED = 4
ENEMY_IMAGE = pygame.image.load("assets/enemy.png")
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMYBULLET1_IMAGE_SHEET = pygame.image.load("assets/Enemy Bullet 1.png")

ENEMYBULLET_WIDTH, ENEMYBULLET_HEIGHT = 25,30 

ENEMYBULLET1_FRAME_COUNT = 4
ENEMYBULLET1_FRAME_WIDTH = ENEMYBULLET1_IMAGE_SHEET.get_width() // ENEMYBULLET1_FRAME_COUNT
ENEMYBULLET1_FRAME_HEIGHT = ENEMYBULLET1_IMAGE_SHEET.get_height()

ENEMYBULLET1_FRAMES = []
for i in range(ENEMYBULLET1_FRAME_COUNT):  # Ensure ENEMYBULLET1_FRAME_COUNT is defined
    frame = ENEMYBULLET1_IMAGE_SHEET.subsurface(
        pygame.Rect(i * ENEMYBULLET1_FRAME_WIDTH, 0, ENEMYBULLET1_FRAME_WIDTH, ENEMYBULLET1_FRAME_HEIGHT)
    )
    frame = pygame.transform.scale(frame, (ENEMYBULLET_WIDTH, ENEMYBULLET_HEIGHT))  # Scale to bullet size
    ENEMYBULLET1_FRAMES.append(frame)

# Explosion Settings
EXPLOSION_IMAGE_SHEET = pygame.image.load("assets/Explosion1.png")
EXPLOSION_WIDTH, EXPLOSION_HEIGHT = 90, 90
EXPLOSION_FRAME_COUNT = 12
EXPLOSION_FRAMES_WIDTH = EXPLOSION_IMAGE_SHEET.get_width() // EXPLOSION_FRAME_COUNT
EXPLOSION_FRAMES_HEIGHT = EXPLOSION_IMAGE_SHEET.get_height()

EXPLOSION_FRAMES = []
for i in range(EXPLOSION_FRAME_COUNT):
    frame = EXPLOSION_IMAGE_SHEET.subsurface(
        pygame.Rect(i * EXPLOSION_FRAMES_WIDTH, 0, EXPLOSION_FRAMES_WIDTH, EXPLOSION_FRAMES_HEIGHT)
    )
    frame = pygame.transform.scale(frame, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))
    EXPLOSION_FRAMES.append(frame)


ASTEROID_WIDTH, ASTEROID_HEIGHT = 120, 120
ASTEROID_SPEED = 6

# Randomly select asteroid image sheets
Random_Asteroid_Image = [
    pygame.image.load("assets/asteroid.png"),
    pygame.image.load("assets/asteroid2.png")
]

# Function to get random asteroid frames
def get_random_asteroid_frames():
    asteroid_image_sheet = random.choice(Random_Asteroid_Image)
    frame_count = 4
    frame_width = asteroid_image_sheet.get_width() // frame_count
    frame_height = asteroid_image_sheet.get_height()

    asteroid_frames = []
    for i in range(frame_count):
        frame = asteroid_image_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (ASTEROID_WIDTH, ASTEROID_HEIGHT))
        asteroid_frames.append(frame)

    return asteroid_frames
#Boss1
BOSS_WIDTH, BOSS_HEIGHT = 256, 256
BOSS_SPEED = 2


# Bullet Settings
BULLET_WIDTH, BULLET_HEIGHT = 10, 15
BULLET_SPEED = 7
BULLET_INTERVAL = 200 # 300 milliseconds cooldown for both player and enemies
ENEMY_BULLET_SPEED = 7  # Enemy bullet speed
ENEMY_BULLET_INTERVAL = 300 # Time interval between enemy shots in milliseconds


#BG/MENU SOUNDS
def play_game_music():
    pygame.mixer.music.load('assets/normal bgm.mp3')  # Replace with your game music file
    pygame.mixer.music.set_volume(1)  # Set the volume (optional)
    pygame.mixer.music.play(-1)  # Play the music in a loop