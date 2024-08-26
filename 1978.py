# July 8 - August 26, 2024
# 1978, Space Invaders released [???]

import decimal
from decimal import *
import pygame
from pygame import *
from pygame.locals import *
import pygame.freetype
import time
import math
import sys
import os
import random
import keyboard
from svg import Parser, Rasterizer
import asyncio

# Try to declare all your globals at once to facilitate compilation later.
COUNT_DOWN = 3

# Do init here
# Load any assets right now to avoid lag at runtime or network errors.



# Do not add anything from here, especially sys.exit/pygame.quit
# asyncio.run is non-blocking on pygame-wasm and code would be executed
# right before program start main()

# ggenije
# This game is powered by PyGame. The Windows build was built with PyInstaller. The web build was built with PygBag (Python web assembly).
# https://youtu.be/FfWpgLFMI7w
# pro.sfxr.me
# https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_collision_and_intesection.md
# https://icons8.com/icons/set/space-invaders--animated
# https://www.freepik.com/free-vector/futuristic-spaceship-collection-with-flat-design_2898820.htm#query=space%20fighter&position=1&from_view=keyword&track=ais_user&uuid=5e43d284-9e98-4b88-a912-680fec6643a0
# https://www.freepik.com/free-vector/funny-game-monsters-collection_1529196.htm#fromView=search&page=2&position=7&uuid=20b22d67-42fc-4208-b742-6e63656f1697
# https://www.youtube.com/watch?v=F69-t33e8tk
# https://www.freepik.com/free-vector/hand-painted-watercolor-galaxy-background_14237502.htm#fromView=search&page=1&position=0&uuid=801401a5-0317-4fcc-a9aa-ff0df8e0039f
# https://nerdparadise.com/programming/pygame/part3
# https://www.geeksforgeeks.org/how-to-add-music-playlist-in-pygame/
# https://stackoverflow.com/questions/120584/svg-rendering-in-a-pygame-application-prior-to-pygame-2-0-pygame-did-not-suppo
# https://stackoverflow.com/questions/20088670/pygame-smooth-fonts


GameOver = 0
async def main():
    global COUNT_DOWN

    # avoid this kind declaration, prefer the way above
    COUNT_DOWN = 3

    # Do your rendering here, note that it's NOT an infinite loop,
    # and it is fired only when VSYNC occurs
    # Usually 1/60 or more times per seconds on desktop
    # could be less on some mobile devices
    
    # Initialize pygame
    #pygame.mixer.pre_init(11025, 8, 2, 1024)
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.init()
    screen_width = 1280
    screen_height = 720
    flags = DOUBLEBUF | pygame.RESIZABLE
    screen = pygame.display.set_mode((screen_width, screen_height), flags, 16)
    clock = pygame.time.Clock()

    font = pygame.freetype.Font("./Fonts/Dosis/static/Dosis-Bold.ttf", 36)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    
    camShake = [0, 0]
    camShake2 = [0, 0]

    def distanceto(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    def MUSIC_SETUP():
        global playlist, Music_end
        playlist = list()
        playlist.append ( "./GameLauncher/assets/games/1978/audio/Kevin MacLeod - Space Fighter Loop.mp3" )
        playlist.append ( "./GameLauncher/assets/games/1978/audio/Kevin MacLeod - Galactic Rap.mp3" )
        playlist.append ( "./GameLauncher/assets/games/1978/audio/Kevin MacLeod - Brain Dance.mp3" )
        playlist.append ( "./GameLauncher/assets/games/1978/audio/Kevin MacLeod - Cloud Dancer.mp3" )
        playlist.append ( "./GameLauncher/assets/games/1978/audio/Kevin MacLeod - Mesmerizing Galaxy Loop.mp3" )
        Music_end = pygame.USEREVENT
        pygame.mixer.music.load ( playlist[0] )  
        playlist.pop(0)
        pygame.mixer.music.play()
        pygame.mixer.music.queue ( playlist[0] )
        playlist.pop(0)
        pygame.mixer.music.set_endevent ( Music_end )  

    # SVG! YAY!
    def load_svg(filename, scale=None, size=None, clip_from=None, fit_to=None, foramt='RGBA'):
        svg = Parser.parse_file(filename)
        scale = min((fit_to[0] / svg.width, fit_to[1] / svg.height)
                    if fit_to else ([scale if scale else 1] * 2))
        width, height = size if size else (svg.width, svg.height)
        surf_size = round(width * scale), round(height * scale)
        buffer = Rasterizer().rasterize(svg, *surf_size, scale, *(clip_from if clip_from else 0, 0))
        return  pygame.image.frombuffer(buffer, surf_size, foramt)

    # Title and Icon and background
    pygame.display.set_caption("1978")
    icon = pygame.image.load('./GameLauncher/assets/games/1978/img/SPACE FIGHTERS SVG icons8.png')
    pygame.display.set_icon(icon)
    background = pygame.image.load('./GameLauncher/assets/games/1978/img/5438849.jpg').convert_alpha()
    background = pygame.transform.scale(background, (screen_width, screen_height))
    backgroundRect = pygame.Rect(background.get_rect())
    background2 = load_svg('./GameLauncher/assets/games/1978/img/vignette.svg')
    background2 = pygame.transform.scale(background2, (screen_width, screen_height))
    backgroundRect2 = pygame.Rect(background2.get_rect())

    # Player
    # playerImg = pygame.image.load('./GameLauncher/assets/games/1978/img/player.png').convert_alpha()
    playerImg = load_svg('./GameLauncher/assets/games/1978/img/player.svg')
    playerPos = [(1280 - playerImg.get_width()/2.5)/2, (720 - playerImg.get_height()/2.5)/2 + 240]
    playerPosChange = [0, 0]
    playerRect = pygame.Rect(playerImg.get_rect(center = playerPos))

    def player():
        # playerImg = pygame.image.load('./GameLauncher/assets/games/1978/img/player.png').convert_alpha()
        playerImg = load_svg('./GameLauncher/assets/games/1978/img/player.svg')
        playerImg = pygame.transform.scale(playerImg, (playerImg.get_width()/2.5 * WindowScale, playerImg.get_height()/2.5 * WindowScale))
        playerRect = pygame.Rect(playerImg.get_rect(center = playerPos))
        screen.blit(playerImg, ((playerPos[0]+camShake[0])*WindowXscale, (playerPos[1]+camShake[1])*WindowYscale))

    # Enemy
    enemyImageNumber = []
    enemyImg = []
    enemyPos = []
    enemyPosChange = []
    enemyRect = []
    for i in range(24):
        enemyImageNumber.append(random.randint(1,9))
        # enemyImg = pygame.image.load(f"./GameLauncher/assets/games/1978/img/alien{enemyImageNumber}.png").convert_alpha()
        enemyImg.append(load_svg(f"./GameLauncher/assets/games/1978/img/alien{enemyImageNumber[i]}.svg"))
        enemyPos.append([random.randint(100, screen_width - 20 - int(enemyImg[i].get_width()//1.7)), random.randint(50, 200)])
        enemyPosChange.append([(random.randint(0, 1) * 280) - 140, 0])
        enemyRect.append(pygame.Rect(enemyPos[i][0], enemyPos[i][1], enemyImg[i].get_width(), enemyImg[i].get_height()))

    def respawnEnemy(i):
        global enemyImg
        global enemyPos
        global enemyPosChange
        global enemyImageNumber
        enemyImageNumber[i] = random.randint(1,9)
        enemyImg[i] = load_svg(f"./GameLauncher/assets/games/1978/img/alien{enemyImageNumber[i]}.svg")
        enemyPos[i] = [random.randint(100, screen_width - 20 - int(enemyImg[i].get_width()//1.7)), random.randint(50, 200)]
        enemyPosChange[i] = [(random.randint(0, 1) * 280) - 140, 0]

    for i in range(24):
        enemyImageNumber[i] = random.randint(1,9)
        enemyImg[i] = load_svg(f"./GameLauncher/assets/games/1978/img/alien{enemyImageNumber[i]}.svg")
        enemyPos[i] = [random.randint(100, screen_width - 20 - int(enemyImg[i].get_width()//1.7)), random.randint(50, 200)]
        enemyPosChange[i] = [(random.randint(0, 1) * 280) - 140, 0]

    def enemy(i):
        #enemyImg = pygame.image.load(f"./GameLauncher/assets/games/1978/img/alien{enemyImageNumber}.png").convert_alpha()
        enemyImg[i] = load_svg(f"./GameLauncher/assets/games/1978/img/alien{enemyImageNumber[i]}.svg")
        enemyImg[i] = pygame.transform.scale(enemyImg[i], (enemyImg[i].get_width()*WindowScale/2, enemyImg[i].get_height()*WindowScale/2))
        enemyRect[i] = pygame.Rect(enemyPos[i][0], enemyPos[i][1], enemyImg[i].get_width(), enemyImg[i].get_height())
        screen.blit(enemyImg[i], ((enemyPos[i][0]+camShake[0])*WindowXscale, (enemyPos[i][1]+camShake[1])*WindowYscale))

    # PlayerLaser
    # Ready - You can't see the laser on the screen.
    # Fire - The laser is currently moving.
    PlayerLaserNum = 0
    # playerLaserImg = pygame.image.load(f"./GameLauncher/assets/games/1978/img/PlayerLaser.png").convert_alpha()
    playerLaserImg = load_svg(f"./GameLauncher/assets/games/1978/img/PlayerLaser.svg")
    playerLaserImg = pygame.transform.scale(playerLaserImg, (playerLaserImg.get_width()*5, playerLaserImg.get_height()*3))
    playerLaserPos = []
    playerLaserState = []
    playerLaserPosChange = [0, -1200]
    playerLaserRect = []
    for i in range(24):
        playerLaserPos.append([0, 0])
        playerLaserState.append("ready")
        playerLaserRect.append(pygame.Rect(playerLaserPos[i][0] + playerLaserImg.get_width()*2, playerLaserPos[i][1] - playerLaserImg.get_height()*0.36, playerLaserImg.get_width(), playerLaserImg.get_height()))

    def playerLaser(num):
        #playerLaserImg = pygame.image.load(f"./GameLauncher/assets/games/1978/img/PlayerLaser.png").convert_alpha()
        playerLaserImg = load_svg(f"./GameLauncher/assets/games/1978/img/PlayerLaser.svg")
        playerLaserImg = pygame.transform.scale(playerLaserImg, (playerLaserImg.get_width()*WindowScale * 5, playerLaserImg.get_height()*WindowScale * 3))
        playerLaserRect[num] = pygame.Rect(playerLaserPos[i][0] + playerLaserImg.get_width()*2, playerLaserPos[i][1] - playerLaserImg.get_height()*0.36, playerLaserImg.get_width(), playerLaserImg.get_height())
        if playerLaserState[num] == "fire":
            screen.blit(playerLaserImg, ((playerLaserPos[num][0]+camShake[0])*WindowXscale + playerLaserImg.get_width() + 26.666667*WindowScale, (playerLaserPos[num][1]+camShake[1])*WindowYscale))
            
    ''' def draw_text(text, font, color, x, y, align):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "left":
            screen.blit(text_surface, (x, y))
        elif align == "center":
            text_rect.center = (x, y)
            screen.blit(text_surface, text_rect) '''
    def draw_text(text, font, color, x, y, align):
        text_rect = font.get_rect(text)
        text_rect.center = screen.get_rect().center
        if align == 'centerh':
            font.render_to(screen, (text_rect.center[0] - text_rect.width/2 + x, y), text, color)
        elif align == 'centerv':
            font.render_to(screen, (x, text_rect.center[1] - text_rect.height/2 + y), text, color)
        elif align == 'center':
            font.render_to(screen, (text_rect.center[0] - text_rect.width/2 + x, text_rect.center[1] - text_rect.height/2 + y), text, color)
        elif align == 'left':
            font.render_to(screen, (x, y), text, color)
        elif align == 'right':
            font.render_to(screen, (text_rect.center[0]*2 - text_rect.width + x, y), text, color)

    # Game Loop
    running = 1
    score = Decimal(0)
    scoreDisplay = Decimal(0)
    frames = 0
    start_time = time.time()
    delta_time = 0.000001
    game_time = -0.000001
    timeScale = 1
    GameFPS = 1/delta_time #60
    def constrain(val, min_val, max_val):
        if val < min_val: return min_val
        if val > max_val: return max_val
        return val

    particles = []

    MUSIC_SETUP()
    
    while running:
        mos_x, mos_y = pygame.mouse.get_pos()
        frames += 1
        (WindowWidth, WindowHeight) = pygame.display.get_surface().get_size()
        WindowXscale = WindowWidth / screen_width
        WindowYscale = WindowHeight / screen_height
        if WindowXscale < 0.01 and WindowYscale < 0.01:
            WindowScale = min(WindowXscale, WindowYscale)
        elif WindowXscale > 0.01 and WindowYscale > 0.01:
            WindowScale = min(WindowXscale, WindowYscale)
        else:
            WindowScale = 0.01
        delta_time = (time.time() - start_time) - game_time
        start_time += (1-timeScale) * delta_time
        delta_time *= timeScale
        game_time = time.time() - start_time
        if delta_time > 0:
            GameFPS = 1/delta_time
        else:
            GameFPS = math.inf
        font = pygame.freetype.Font("./Fonts/Dosis/static/Dosis-Bold.ttf", round(36*WindowScale))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
            if event.type == Music_end:    # A track has ended
                if len ( playlist ) > 0:       # If there are more tracks in the queue...
                    pygame.mixer.music.queue ( playlist.pop() ) # Queue the next one in the list
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not PlayerLaserNum >= 24:
                    for i in range(24):
                        if playerLaserState[i] == "ready":
                            playerLaserPos[i] = [playerPos[0] + random.randrange(-7, 7)*WindowScale, playerPos[1]+50]
                            playerLaserState[i] = "fire"
                            PlayerLaserNum += 1
                            playerLaserPos[i][1] = playerPos[1]+50
                            pygame.mixer.Sound("./GameLauncher/assets/games/1978/audio/PlayerLaserShoot.wav").play()
                            break 
        if not pygame.mixer.music.get_busy():
            MUSIC_SETUP()
        # If keystroke is pressed check whether its right or left
        keys = pygame.key.get_pressed()  # Checking pressed keys
        if keyboard.is_pressed('up') or keys[pygame.K_UP]:
            playerPosChange[1] -= 12 * delta_time
        if keyboard.is_pressed('down') or keys[pygame.K_DOWN]:
            playerPosChange[1] += 12 * delta_time
        if keyboard.is_pressed('left') or keys[pygame.K_LEFT]:
            playerPosChange[0] -= 12 * delta_time
        if keyboard.is_pressed('right') or keys[pygame.K_RIGHT]:
            playerPosChange[0] += 12 * delta_time

        # RGB - Red, Green, Blue
        screen.fill((0, 0, 32))
        # Background Image
        if (WindowWidth, WindowHeight) != (background.get_width(), background.get_height()):
            background = pygame.transform.scale(pygame.image.load('./GameLauncher/assets/games/1978/img/5438849.jpg'), (WindowWidth, WindowHeight))
            background2 = pygame.transform.scale(load_svg('./GameLauncher/assets/games/1978/img/vignette.svg'), (WindowWidth, WindowHeight))
        screen.blit(background, camShake)
        particles.append([[random.randint(screen_width*-1, screen_width), -100], [random.randint(0, 0) / 10 - 1, 300], random.randint(4, 6), -2, WHITE])
        for particle in particles:
            particle[0][0] += particle[1][0] * delta_time
            particle[0][1] += particle[1][1] * delta_time
            particle[2] += particle[3] * delta_time
            pygame.draw.circle(screen, particle[4], (round((particle[0][0]+round(camShake[0]))*WindowXscale), round((particle[0][1]+round(camShake[1]))*WindowYscale)), round(particle[2]*WindowScale))
            if particle[2] <= 0:
                particles.remove(particle)

        playerPos[0] += playerPosChange[0] * 100 * delta_time
        playerPos[1] += playerPosChange[1] * 100 * delta_time
        playerPosChange[0] *= 0.04**delta_time
        playerPosChange[1] *= 0.04**delta_time
        #playerPos[0] = constrain(playerPos[0], 0, screen_width - 135*WindowScale)
        #playerPos[1] = constrain(playerPos[1], 0, screen_height - 165*WindowScale)
        if WindowYscale >= WindowXscale:
            playerPos[1] = constrain(playerPos[1], 0, screen_height - playerImg.get_height()*WindowScale/2.5)
        else:
            playerPos[1] = constrain(playerPos[1], 0, screen_height - playerImg.get_height()/2.5)
        # Player Laser Movement
        enpoY = 0
        for i in range(24):
            enemyPos[i][0] += enemyPosChange[i][0] * delta_time
            enemyPos[i][1] += enemyPosChange[i][1] * delta_time
            if WindowXscale >= WindowYscale:
                playerPos[0] = constrain(playerPos[0], 0, screen_width - playerImg.get_width()*WindowScale/2.5)
                if enemyPos[i][0] >= screen_width - enemyImg[i].get_width()*WindowScale or enemyPos[i][0] <= 0:
                    enemyPos[i][0] -= enemyPosChange[i][0] * .1
                    enemyPosChange[i][0] *= -1.2
                    enemyPos[i][1] += 40
            else:
                playerPos[0] = constrain(playerPos[0], 0, screen_width - playerImg.get_width()/2.5)
                if enemyPos[i][0] >= screen_width - enemyImg[i].get_width() or enemyPos[i][0] <= 0:
                    enemyPos[i][0] -= enemyPosChange[i][0] * .1
                    enemyPosChange[i][0] *= -1.2
                    enemyPos[i][1] += 40
            enemyRect[i] = pygame.Rect(enemyPos[i][0], enemyPos[i][1], enemyImg[i].get_width(), enemyImg[i].get_height())
            playerLaserRect[i] = pygame.Rect(playerLaserPos[i][0] + playerLaserImg.get_width()*2, playerLaserPos[i][1] - playerLaserImg.get_height()*0.36, playerLaserImg.get_width(), playerLaserImg.get_height())
            if playerLaserPos[i][1] <= -60:
                PlayerLaserNum -= 1
                playerLaserPos[i][1] = 2000
                playerLaserState[i] = "ready"
            if enemyPos[i][1] >= enpoY:
                enpoY = enemyPos[i][1]
                if enpoY >= 400:
                    timeScale = 1 - ((enpoY/600 - .66667)**.5)
                else:
                    timeScale = 1
                background2.set_alpha(enpoY - 430)
            if enpoY >= 900:
                running = False
                GameOver = 1
            for j in range(24):
                if playerLaserRect[i].colliderect(enemyRect[j]):
                    score += Decimal(100)
                    camShake2[0] += 12
                    camShake2[1] += 12
                    pygame.mixer.Sound("./GameLauncher/assets/games/1978/audio/EnemyExplosion.wav").play()
                    for k in range(10):
                        particles.append([[playerLaserPos[i][0] + playerLaserImg.get_width()*2, playerLaserPos[i][1]], [math.sin(random.randrange(-180, 180))*240, math.cos(random.randrange(-180, 180))*240], random.randint(6, 9), -5, RED])
                    enemyImageNumber[j] = random.randint(1,9)
                    enemyImg[j] = load_svg(f"./GameLauncher/assets/games/1978/img/alien{enemyImageNumber[j]}.svg")
                    enemyPos[j] = [random.randint(100, screen_width - 20 - int(enemyImg[j].get_width()//1.7)), random.randint(50, 200)]
                    enemyPosChange[j] = [(random.randint(0, 1) * 280) - 140, 0]
                    PlayerLaserNum -= 1
                    playerLaserPos[i][1] = 2000
                    playerLaserState[i] = "ready"
            playerLaserPos[i][1] += playerLaserPosChange[1] * delta_time * (playerLaserState[i] == "fire")
            # pygame.draw.rect(screen, RED, playerLaserRect[i])
            # pygame.draw.rect(screen, RED, enemyRect[i])
            playerLaser(i)
            enemy(i)
        player()
        screen.blit(background2, camShake)
        PlayerLaserNum = constrain(PlayerLaserNum, 0, 24)
        scoreDisplay += (Decimal(score)-Decimal(scoreDisplay)) * Decimal(delta_time) * Decimal(5)
        scoreDisplay2 = round(Decimal(scoreDisplay))
        camShake = (random.randrange(-1, 1)*camShake2[0], random.randrange(-1, 1)*camShake2[1])
        camShake2[0] *= 0.01**delta_time
        camShake2[1] *= 0.01**delta_time
        draw_text(f"Score: {Decimal(scoreDisplay2)}", font, (abs(math.cos(game_time * 1.5) * 255), abs(math.sin(game_time * 2) * 255), abs(math.cos(game_time * 2.5) * 255)), (0+camShake[0])*WindowScale, (30+camShake[1])*WindowScale, "centerh")
        draw_text(f"Score: {Decimal(scoreDisplay2)}", font, (128, 64, 192), (1+camShake[0])*WindowScale, (31+camShake[1])*WindowScale, "centerh")
        pygame.display.flip()
        pygame.display.update()
        # clock.tick(24)

    camShake = 40
    while GameOver:
        mos_x, mos_y = pygame.mouse.get_pos()
        frames += 1
        (WindowWidth, WindowHeight) = pygame.display.get_surface().get_size()
        WindowXscale = WindowWidth / screen_width
        WindowYscale = WindowHeight / screen_height
        if WindowXscale < 0.01 and WindowYscale < 0.01:
            WindowScale = min(WindowXscale, WindowYscale)
        elif WindowXscale > 0.01 and WindowYscale > 0.01:
            WindowScale = min(WindowXscale, WindowYscale)
        else:
            WindowScale = 0.01
        delta_time = (time.time() - start_time) - game_time
        start_time += (1-timeScale) * delta_time
        delta_time *= timeScale
        game_time = time.time() - start_time
        if delta_time > 0:
            GameFPS = 1/delta_time
        else:
            GameFPS = math.inf
        font = pygame.freetype.Font("./Fonts/Dosis/static/Dosis-Bold.ttf", round(100*WindowScale))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameOver = 0
        pygame.mixer.music.stop()
        camShake = (random.randrange(-1, 1)*camShake2[0], random.randrange(-1, 1)*camShake2[1])
        camShake2[0] *= 0.01**delta_time
        camShake2[1] *= 0.01**delta_time
        if (WindowWidth, WindowHeight) != (background.get_width(), background.get_height()):
            background = pygame.transform.scale(pygame.image.load('./GameLauncher/assets/games/1978/img/5438849.jpg'), (WindowWidth, WindowHeight))
            background2 = pygame.transform.scale(load_svg('./GameLauncher/assets/games/1978/img/vignette.svg'), (WindowWidth, WindowHeight))
        screen.blit(background, camShake)
        screen.blit(background2, camShake)
        timeScale = 1
        draw_text(f"Score: {Decimal(scoreDisplay2)}", font, (abs(math.cos(game_time * 1.5) * 255), abs(math.sin(game_time * 2) * 255), abs(math.cos(game_time * 2.5) * 255)), (0+camShake[0])*WindowScale, (30+camShake[1])*WindowScale, "centerh")
        draw_text(f"Score: {Decimal(scoreDisplay2)}", font, (128, 64, 192), (1+camShake[0])*WindowScale, (31+camShake[1])*WindowScale, "centerh")
        draw_text("GAME OVER", font, (128, 64, 192), (-1+camShake[0])*WindowScale, (0+camShake[1])*WindowScale, "center")
        draw_text("GAME OVER", font, (128, 64, 192), (1+camShake[0])*WindowScale, (0+camShake[1])*WindowScale, "center")
        draw_text("GAME OVER", font, (128, 64, 192), (0+camShake[0])*WindowScale, (1+camShake[1])*WindowScale, "center")
        draw_text("GAME OVER", font, (128, 64, 192), (-1+camShake[0])*WindowScale, (1+camShake[1])*WindowScale, "center")
        draw_text("GAME OVER", font, (128, 64, 192), (1+camShake[0])*WindowScale, (1+camShake[1])*WindowScale, "center")
        draw_text("GAME OVER", font, (128, 64, 192), (0+camShake[0])*WindowScale, (-1+camShake[1])*WindowScale, "center")
        draw_text("GAME OVER", font, (128, 64, 192), (-1+camShake[0])*WindowScale, (-1+camShake[1])*WindowScale, "center")
        draw_text("GAME OVER", font, (128, 64, 192), (1+camShake[0])*WindowScale, (-1+camShake[1])*WindowScale, "center")
        draw_text("GAME OVER", font, (abs(math.cos(game_time * 1.5) * 255), abs(math.sin(game_time * 2) * 255), abs(math.cos(game_time * 2.5) * 255)), (0+camShake[0])*WindowScale, (0+camShake[1])*WindowScale, "center")
        pygame.display.flip()
        pygame.display.update()
            
    print(f"""

        Hello[{COUNT_DOWN}] from Python, MunaAlaneme

""")
    # pygame.display.update() should go right next line

    await asyncio.sleep(0)  # Very important, and keep it 0

    if not COUNT_DOWN:
        return

    COUNT_DOWN = COUNT_DOWN - 1

# This is the program entry point:
asyncio.run(main())