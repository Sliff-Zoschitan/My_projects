import pygame
import random
from Sprite import sprite
from Drawing import drawing
from Slipper import Slippers

pygame.init()
work = True
while work:
    w = 1280
    h = 720
    #pygame.mixer.music.load('Sounds/Test.mp3')
    #pygame.mixer.music.play()
    

    win = pygame.display.set_mode((w, h))
    bckg_img = pygame.image.load("Images/Fon.png")
    death_img = pygame.image.load("Images/Death.png")
    cat1_img = pygame.image.load("Images/Cat1.png")
    cat2_img = pygame.image.load("Images/Cat2.png")
    cat3_img = pygame.image.load("Images/Cat3.png")
    host1_img = pygame.image.load("Images/Host1.png")
    host2_img = pygame.image.load("Images/Host2.png")
    host3_img = pygame.image.load("Images/Host3.png")
    slipper_img = pygame.image.load("Images/Slipper.png")

    bckg = sprite(0, 0, 720, 4020, bckg_img, -7, 0)
    death = sprite(0, 0, 720, 1280, death_img, 0, 0)
    cat = sprite(1000, 300, 314, 187, cat1_img, 7, 5)
    cat.jump_count = 30
    cat.divider = 30
    cat.jump_count_end = 30
    host = sprite(50, 300, 360, 230, host1_img, 0, 0)
    slippers = [sprite(50, 300, 80, 164, slipper_img, -7, 0) for _ in range(0, 10)]
    lose = False
    play = True
    new_slipper = False
    i = 0
    while play:
        if not(lose):
            i += 1
            if bckg.x <= -bckg.w: bckg.x = 0
            drawing(win, bckg.x ,bckg.y, bckg.img)
            drawing(win, bckg.x + bckg.w, bckg.y, bckg.img)
            drawing(win, cat.x, cat.y, cat.img)
            drawing(win, host.x, host.y, host.img)
            if (i % 40 > 0)and(i % 40 < 10):
                cat.img = cat1_img
                host.img = host3_img
            elif (i % 40 > 10)and(i % 40 < 20):
                cat.img = cat2_img
                host.img = host2_img
            elif (i % 40 > 20)and(i % 40 < 30):
                cat.img = cat1_img
                host.img = host1_img
            elif (i % 40 > 30)and(i % 40 < 40):
                cat.img = cat2_img
                host.img = host2_img
            if i % 300 == 0:
                new_slipper = True
                lose = Slippers(lose, cat.x, cat.y, cat.w, cat.h, new_slipper, win, 10, slippers)
                new_slipper = False
            else:
                lose = Slippers(lose, cat.x, cat.y, cat.w, cat.h, new_slipper, win, 10, slippers)
            bckg.x += bckg.speed[0]
            bckg.y += bckg.speed[1]
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and cat.x + cat.w < w:          #перемещение вправо
                cat.x += cat.speed[0]
            if keys[pygame.K_LEFT] and cat.x > 0:                   #перемещение вправо
                cat.x -= cat.speed[0]
            if not (cat.jump):
                if keys[pygame.K_DOWN] and cat.y + cat.h < h:       #перемещение вниз
                    cat.y += cat.speed[1]
                if keys[pygame.K_UP] and cat.y > 250:               #перемещение вверх
                    cat.y -= cat.speed[1]
            else:                                                   #прыжок
                cat.Jump()
            if keys[pygame.K_SPACE]:
                cat.jump = True
            if cat.x <= host.x + host.w:
                lose = True

        else:
            drawing(win, death.x, death.y, death.img)
            if keys[pygame.K_r]:
                play = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                work = False
        keys = pygame.key.get_pressed()

        pygame.time.delay(3)
        pygame.display.update()