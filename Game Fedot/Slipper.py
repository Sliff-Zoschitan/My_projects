import pygame
import random
from Sprite import sprite
from Drawing import drawing


def Slippers(lose, cat_x, cat_y, cat_w, cat_h, new_slipper, win, i, slippers):
    if i > 0:
        i -= 1
        if slippers[i].draw:
            if slippers[i].jump:
                slippers[i].x += slippers[i].speed[0]
                slippers[i].Jump()
                if not(slippers[i].jump):
                    slippers[i].speed = (-7, 0)
            else:
                slippers[i].jump_count = 40
                slippers[i].jump_count_end = 47
                slippers[i].x += slippers[i].speed[0]
            drawing(win, slippers[i].x, slippers[i].y, slippers[i].img)
        else:
            if new_slipper:
                slippers[i].draw = True
                slippers[i].jump = True
                slippers[i].x = 50
                slippers[i].y = 300
                slippers[i].speed = (random.randint(4, 12), 0)  #random.randint(7, 14)
                new_slipper = False
        if slippers[i].x + slippers[i].w < 0:
            slippers[i].draw = False
        if (slippers[i].x + slippers[i].w >= cat_x) and (slippers[i].x <= cat_x + cat_w) and (slippers[i].y + slippers[i].h >= cat_y) and (slippers[i].y <= cat_y + cat_h):
            lose = True
        lose = Slippers(lose, cat_x, cat_y, cat_w, cat_h, new_slipper, win, i, slippers)
    return lose