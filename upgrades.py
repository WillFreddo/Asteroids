import pygame
from constants import *
from circleshape import CircleShape
import random

class Upgrade(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, UPGRADE_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.upgrade = random.randint(0,3)
        self.colour = UPGRADE_COLOUR[self.upgrade]
        self.despawn = 0
        self.c_time = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, self.square(), 2)

    def square(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius
        a = self.position + forward * self.radius - right
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        d = self.position + forward * self.radius + right
        return [a, b, c, d]
    
    def rotate(self, dt):
        self.rotation += UPGRADE_TURN_SPEED * dt

    def blink(self, dt):
        self.c_time += dt 
        
        if self.c_time >= 0.5:
            self.c_time = 0

            if self.colour != "black":
                self.colour = "black"
        
            elif self.colour == "black":
                self.colour = UPGRADE_COLOUR[self.upgrade]
            
    def update(self, dt):
        self.timer -= dt
        self.rotate(dt)

        self.despawn += dt
        if self.despawn + 3 >= UPGRADE_DESPAWN:
            self.blink(dt)
        
        if self.despawn >= UPGRADE_DESPAWN:
            self.kill()

