import pygame


class sprite:
    x = 0
    y = 0
    h = 0
    w = 0
    img = pygame.image.load("Images/Fon.png")
    speed = (0,0)
    draw = False
    jump = False
    jump_count = 40
    divider = 56
    jump_count_end = 47
    def __init__(self,x,y,h,w,img,*speed):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.img = img
        self.speed = speed
    def Jump(self):
        if self.jump_count >= -self.jump_count_end:
            if self.jump_count > 0:
                self.y -= (self.jump_count**2) / self.divider
            else:
                self.y += (self.jump_count**2) / self.divider
            self.jump_count -= 1
        else:
            self.jump = False
            self.jump_count = self.jump_count_end
