import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Настройка экрана
screen = pygame.display.set_mode((800, 600))

# Название
pygame.display.set_caption("Space Invader")

# Лого
logo = pygame.image.load('Photos/rocket.png')
pygame.display.set_icon(logo)

# Фон
background = pygame.image.load('Photos/background.png')

# Музыка для фона

music = pygame.mixer_music.load("Sounds/background_song.mp3")
pygame.mixer_music.play(-1)

# Столкновение (пуля и инопланетянин)
def collison(a, b, c, d):
    dist = math.sqrt(math.pow(c - a, 2) + math.pow(d - b, 2))
    if dist < 32:
        return True

# Столкновение (игрок и инопланетянин)
def collison1(a, b, c, d):
    dist = math.sqrt(math.pow(c - a, 2) + math.pow(d - b, 2))
    if dist < 64:
        return True

# Счет
score = 0
font = pygame.font.Font('Font/freesansbold.ttf', 32)
textX = 0
textY = 0


def Show_score(x, y):
    sc = font.render('Score : ' + str(score), True, (255, 255, 255))
    screen.blit(sc, (x, y))


# Пуля
bullet_icon = pygame.image.load('Photos/bullet.png')
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = -5
bullet_state = 'ready'


def bullet(x, y):
    screen.blit(bullet_icon, (bulletX, bulletY))


# Игрок
player_icon = pygame.image.load('Photos/space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(player_icon, (x, y))


# Инопланетянин
number_of_enimies = 10
alien_icon = pygame.image.load('Photos/space-ship.png')
alienX = []
alienY = []
alienX_change = []
alienY_change = []
for i in range(number_of_enimies):
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(40, 120))
    alienX_change.append(4)
    alienY_change.append(40)


def alien(p, q):
    screen.blit(alien_icon, (p, q))


# Мгновенное убийство
def instant_killer():
    for y in range(number_of_enimies):
        alienY[y] = 2000


# Игра закончена
gameoverfont = pygame.font.Font('freesansbold.ttf', 64)
h = 0


def game_over():
    for k in range(number_of_enimies):
        game_changer = collison1(playerX, playerY, alienX[k], alienY[k])
        if game_changer is True:
            global h
            h = 1
    if h == 1:
        over = gameoverfont.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over, (200, 250))
        instant_killer()


#  Сохранение окна игры
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_SPACE:
                bullet_sound = pygame.mixer.Sound("Sounds/laser.wav")
                bullet_sound.play()
                bulletX = playerX + 16
                bullet_state = 'fire'
                bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            playerX_change = 0

    # Движение игрока
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    player(playerX, playerY)

    # Движение инопланетянина
    for j in range(number_of_enimies):
        alien(alienX[j], alienY[j])

        alienX[j] += alienX_change[j]

        if alienX[j] <= 0:
            alienX_change[j] = 2
            alienY[j] += alienY_change[j]
        elif alienX[j] >= 736:
            alienX_change[j] = -2
            alienY[j] += alienY_change[j]

    # Движение пули
    if bullet_state == 'fire':
        bulletY += bulletY_change
        bullet(bulletX, bulletY)
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
    # Столкновение
    for k in range(number_of_enimies):
        detect = collison(bulletX, bulletY, alienX[k], alienY[k])
        if detect is True:
            collision_sound = pygame.mixer.Sound("Sounds/explosion.wav")
            collision_sound.play()
            score += 1
            bullet_state = "ready"
            bulletY = 500
            alienY[k] = random.randint(40,120)

    game_over()
    Show_score(textX, textY)
    pygame.display.update()
