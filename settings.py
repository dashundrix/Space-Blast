import pygame
import random



# Game Settings
WIDTH, HEIGHT = 1280, 680
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters")

cursor_img = pygame.image.load('assets/MOUSE_POINTER.png')
cursor_img = pygame.transform.scale(cursor_img, (64, 64))

BG = pygame.transform.scale(pygame.image.load("assets/Space Background.png"), (WIDTH, HEIGHT))
BG1 = pygame.transform.scale(pygame.image.load("assets/Space Background1.png"), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load("assets/Space Background2.jpg"), (WIDTH, HEIGHT))

CURRENT_BG = BG # Changing the map

BG_SCROLL_SPEED = 0.5  # Adjust this value to control the scrolling speed
bg_y = 0  # This will track the y position of the background

#BG/MENU SOUNDS
def play_game_music():
    pygame.mixer.music.load('assets/normal bgm.mp3')  # Replace with your game music file
    pygame.mixer.music.set_volume(1)  # Set the volume (optional)
    pygame.mixer.music.play(-1)  # Play the music in a loop



# Load sound
pygame.mixer.init()
shoot_sound_player = pygame.mixer.Sound("assets/shoot_player.wav")  # Ensure this path is correct
shoot_sound_enemy = pygame.mixer.Sound("assets/shoot_enemy.wav")  # Ensure this path is correct
normal_bg = pygame.mixer.Sound("assets/normal bgm.mp3")  # Ensure this path is correct


# Player Settings
PLAYER_WIDTH, PLAYER_HEIGHT = 128, 128
PLAYER_SPEED = 10


PLAYER_SPRITE_SHEETS = {
    "idle": "assets/SPACESHIP 1.png",
    "up": "assets/SPACESHIP1_UP.png",
    "right": "assets/SPACESHIP1_RIGHT.png",
    "left": "assets/SPACESHIP1_LEFT.png",
    "down": "assets/SPACESHIP 1.png",
    "up-left": "assets/SPACESHIP1_LEFT.png",  
    "up-right": "assets/SPACESHIP1_RIGHT.png",  
    "down-left": "assets/SPACESHIP1_LEFT.png",  
    "down-right": "assets/SPACESHIP1_RIGHT.png",  
}

PLAYERBULLET1_IMAGE_SHEET = pygame.image.load("assets/Bullet 1.png")
PLAYERBULLET2_IMAGE_SHEET = pygame.image.load("assets/Dual_Bullet.png")

# Frame counts for each sprite sheet
PLAYER_FRAME_COUNT = {
    "idle": 12,
    "up": 6,
    "right": 6,
    "left": 6,
    "down": 12,
    "up-left": 6, 
    "up-right": 6,
    "down-left": 6,
    "down-right": 6,
}

PLAYER_FRAMES = {}
for direction, sprite_sheet_path in PLAYER_SPRITE_SHEETS.items():
    sprite_sheet = pygame.image.load(sprite_sheet_path)
    frame_count = PLAYER_FRAME_COUNT[direction]
    frame_width = sprite_sheet.get_width() // frame_count
    frame_height = sprite_sheet.get_height()

    # Extract and scale frames
    PLAYER_FRAMES[direction] = [
        pygame.transform.scale(
            sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)),
            (PLAYER_WIDTH, PLAYER_HEIGHT),
        )
        for i in range(frame_count)
    ]

PLAYERBULLET_WIDTH, PLAYERBULLET_HEIGHT = 50,60 

PLAYERBULLET1_FRAME_COUNT = 4
PLAYERBULLET1_FRAME_WIDTH = PLAYERBULLET1_IMAGE_SHEET.get_width() // PLAYERBULLET1_FRAME_COUNT
PLAYERBULLET1_FRAME_HEIGHT = PLAYERBULLET1_IMAGE_SHEET.get_height()

PLAYERBULLET2_FRAME_COUNT = 5
PLAYERBULLET2_FRAME_WIDTH = PLAYERBULLET2_IMAGE_SHEET.get_width() // PLAYERBULLET2_FRAME_COUNT
PLAYERBULLET2_FRAME_HEIGHT = PLAYERBULLET2_IMAGE_SHEET.get_height()



PLAYERBULLET1_FRAMES = []
for i in range(PLAYERBULLET1_FRAME_COUNT):  # Ensure PLAYERBULLET1_FRAME_COUNT is defined
    frame = PLAYERBULLET1_IMAGE_SHEET.subsurface(
        pygame.Rect(i * PLAYERBULLET1_FRAME_WIDTH, 0, PLAYERBULLET1_FRAME_WIDTH, PLAYERBULLET1_FRAME_HEIGHT)
    )
    frame = pygame.transform.scale(frame, (PLAYERBULLET_WIDTH, PLAYERBULLET_HEIGHT))  # Scale to bullet size
    PLAYERBULLET1_FRAMES.append(frame)

PLAYERBULLET2_FRAMES = []
for i in range(PLAYERBULLET2_FRAME_COUNT):  # Ensure PLAYERBULLET2_FRAME_COUNT is defined
    frame = PLAYERBULLET2_IMAGE_SHEET.subsurface(
        pygame.Rect(i * PLAYERBULLET2_FRAME_WIDTH, 0, PLAYERBULLET2_FRAME_WIDTH, PLAYERBULLET2_FRAME_HEIGHT)
    )
    frame = pygame.transform.scale(frame, (PLAYERBULLET_WIDTH, PLAYERBULLET_HEIGHT))  # Scale to bullet size
    PLAYERBULLET2_FRAMES.append(frame)

# Enemy Settings
ENEMY_WIDTH, ENEMY_HEIGHT = 64, 64
ENEMY_SPEED = 4
ENEMY_IMAGE = pygame.image.load("assets/enemy.png")
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMYBULLET1_IMAGE_SHEET = pygame.image.load("assets/Enemy Bullet 1.png")

ENEMYBULLET_WIDTH, ENEMYBULLET_HEIGHT = 50,60 

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
BOSS_WIDTH, BOSS_HEIGHT = 576, 256
BOSS_SPEED = 2
BOSS_IMAGE_SHEET = pygame.image.load("assets/Boss1.png")

BOSS1_FRAME_COUNT = 4
BOSS1_FRAME_WIDTH = BOSS_IMAGE_SHEET.get_width() // BOSS1_FRAME_COUNT
BOSS1_FRAME_HEIGHT = BOSS_IMAGE_SHEET.get_height()

BOSS1_FRAMES = []
for i in range(BOSS1_FRAME_COUNT):
    frame = BOSS_IMAGE_SHEET.subsurface(
        pygame.Rect(i * BOSS1_FRAME_WIDTH, 0, BOSS1_FRAME_WIDTH, BOSS1_FRAME_HEIGHT)
    )
    frame = pygame.transform.scale(frame, (BOSS_WIDTH, BOSS_HEIGHT))
    BOSS1_FRAMES.append(frame)

BOSS1_BULLET1_IMAGE_SHEET = pygame.image.load("assets/Enemy Bullet 1.png")
BOSS1_BULLET_WIDTH, BOSS1_BULLET_HEIGHT = 50,60
BOSS1_BULLET1_FRAME_COUNT = 4
BOSS_BULLET_SPEED = 10

BOSS1_BULLET1_FRAME_WIDTH = BOSS1_BULLET1_IMAGE_SHEET.get_width() // BOSS1_BULLET1_FRAME_COUNT
BOSS1_BULLET1_FRAME_HEIGHT = BOSS1_BULLET1_IMAGE_SHEET.get_height()

BOSS1_BULLET1_FRAMES = []
for i in range(BOSS1_BULLET1_FRAME_COUNT):
    frame = BOSS1_BULLET1_IMAGE_SHEET.subsurface(
        pygame.Rect(i * BOSS1_BULLET1_FRAME_WIDTH, 0, BOSS1_BULLET1_FRAME_WIDTH, BOSS1_BULLET1_FRAME_HEIGHT)
    )
    frame = pygame.transform.scale(frame, (BOSS1_BULLET_WIDTH, BOSS1_BULLET_HEIGHT))
    BOSS1_BULLET1_FRAMES.append(frame)

# Bullet Settings
BULLET_WIDTH, BULLET_HEIGHT = 10, 15
BULLET_SPEED = 10
BULLET_INTERVAL = 200 # 300 milliseconds cooldown for both player and enemies
ENEMY_BULLET_SPEED = 10  # Enemy bullet speed
ENEMY_BULLET_INTERVAL = 600 # Time interval between enemy shots in milliseconds

# Power-up Settings
POWERUP_WIDTH, POWERUP_HEIGHT = 74, 74
POWERUP_SPEED = 5


POWERUPDUALGUN_IMAGE_SHEET = pygame.image.load("assets/PowerUp1.png")

POWERUP1_FRAME_COUNT = 13

POWERUP1_FRAME_WIDTH = POWERUPDUALGUN_IMAGE_SHEET.get_width() // POWERUP1_FRAME_COUNT
POWERUP1_FRAME_HEIGHT = POWERUPDUALGUN_IMAGE_SHEET.get_height()

POWERUP1_DURATION = 12000  

POWERUPDUALGUN_FRAMES = []
for i in range(POWERUP1_FRAME_COUNT):
    frame = POWERUPDUALGUN_IMAGE_SHEET.subsurface(
        pygame.Rect(i * POWERUP1_FRAME_WIDTH, 0, POWERUP1_FRAME_WIDTH, POWERUP1_FRAME_HEIGHT)
    )
    frame = pygame.transform.scale(frame, (POWERUP_WIDTH, POWERUP_HEIGHT))
    POWERUPDUALGUN_FRAMES.append(frame)

