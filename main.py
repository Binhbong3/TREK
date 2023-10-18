import pygame
import random
import math
from pygame import mixer

pygame.init()

backgroundImg = pygame.image.load('background.png')
screen = pygame.display.set_mode((400, 600))

pygame.display.set_caption("Space Trek")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 165
playerX_change = 0

planet = ['pl1.png', 'pl2.png', 'pl3.png', 'pl4.png', 'pl5.png']
challengeImg = pygame.image.load(random.choice(planet))
challengeX = random.randrange(45, 285, 60)
challengeY = -50
challengeY_change = 0.05
time_challenge_change = 5


def player(x):
    screen.blit(playerImg, (x, 523))


def challenge(x, y):
    screen.blit(challengeImg, (x, y))


font1 = pygame.font.Font('freesansbold.ttf', 40)
font2 = pygame.font.Font('freesansbold.ttf', 20)
start_menu1_text = font1.render("SPACE TREK", True, (85, 213, 179))
start_menu2_text = font2.render("Press Any Key To Start", True, (202, 120, 179))


def start_menu():
    screen.blit(start_menu1_text, (78, 250))
    screen.blit(start_menu2_text, (97, 300))


score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 20)
highest_score_value = score_value


def score():
    score_text = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (20, 20))


def collision(x1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(522 - y2, 2))
    return distance > 20


go_font = pygame.font.Font('freesansbold.ttf', 40)
go_text = go_font.render("GAME OVER", True, (85, 213, 179))
final_score_font = pygame.font.Font('freesansbold.ttf', 25)
final_score_text = final_score_font.render("Score: " + str(score_value), True, (200, 200, 200))
highest_score_font = pygame.font.Font('freesansbold.ttf', 25)


def game_over(x):
    screen.blit(go_text, (80, 250))
    screen.blit(final_score_text, (150, 290))
    highest_score_text = highest_score_font.render("Highest Score: " + str(x), True, (200, 200, 150))
    screen.blit(highest_score_text, (100, 320))


pause_font1 = pygame.font.Font('freesansbold.ttf', 40)
pause_text1 = pause_font1.render('PAUSE', True, (200, 213, 179))
pause_font2 = pygame.font.Font('freesansbold.ttf', 20)
pause_text2 = pause_font2.render('Press Any Key To Continue', True, (150, 150, 130))


def pause():
    screen.blit(pause_text1, (138, 210))
    screen.blit(pause_text2, (70, 260))


background_music = mixer.Sound('backgroundmusic.mp3')
game_over_music = mixer.Sound('gameover.mp3')
pause_check = True
start_menu_check = True
running = True
while running:
    screen.blit(backgroundImg, (1, 1))

    if start_menu_check:
        start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                start_menu_check = False
    else:
        if pause_check:
            if collision(playerX, challengeX, challengeY):
                game_over_music.stop()
                background_music.play()
                score()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                            playerX_change = 0

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            playerX_change = 60
                        if event.key == pygame.K_LEFT:
                            playerX_change = -60
                        if event.key == pygame.K_ESCAPE:
                            pause_check = False
                    if 0 <= playerX + playerX_change <= 330:
                        playerX += playerX_change

                for i in range(time_challenge_change):
                    challengeY += challengeY_change

                if challengeY >= 800:
                    time_challenge_change += 1
                    challengeImg = pygame.image.load(random.choice(planet))
                    challengeX = random.randrange(45, 285, 60)
                    challengeY = -50
                    score_value += 1
            else:
                background_music.stop()
                game_over_music.play()
                highest_score_value = max(highest_score_value, score_value)
                game_over(highest_score_value)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        time_challenge_change = 5
                        challengeImg = pygame.image.load(random.choice(planet))
                        challengeX = random.randrange(45, 285, 60)
                        challengeY = -50
                        score_value = 0
                        playerX = 165
                        playerX_change = 0
        else:
            background_music.stop()
            pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    pause_check = True
        challenge(challengeX, challengeY)
        player(playerX)
    pygame.display.update()
