import pygame
import random
from constants import *
from circleshape import CircleShape
from upgrades import Upgrade
from healthbar import HealthBar

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.invincible = ASTEROID_INVUNERBILITY
    


    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)
        if self.invincible >= 0:
            self.invincible -= dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:

            return
        
        ra = random.uniform(20, 50)

        a = self.velocity.rotate(ra)
        b = self.velocity.rotate(-ra)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2


class BossAsteroid(CircleShape):

    def __init__(self, x, y, radius, kind):
        super().__init__(x, y, radius)
        self.invincible = ASTEROID_INVUNERBILITY - 0.75
        self.health = BOSS_HEALTH * kind
        self.kind = kind
        self.rebound = 1.25
    
    


    def draw(self, screen):
        pygame.draw.circle(screen, "gold", self.position, self.radius, 2)

    def update(self, dt):

        if self.rebound <= 0:
            self.bounce()
            self.rebound = 0.75

        self.position += (self.velocity * dt)
        if self.invincible >= 0:
            self.invincible -= dt
        
        if self.rebound >= 0:
            self.rebound -= dt

        

    def bounce(self):
        if self.position[0] <= 20:
            self.velocity[0] = -self.velocity[0]
        
        if self.position[0] >= SCREEN_WIDTH - 20:
            self.velocity[0] = -self.velocity[0]

        if self.position[1] <= 20:
            self.velocity[1] = -self.velocity[1]

        if self.position[1] >= SCREEN_HEIGHT - 20:
            self.velocity[1] = -self.velocity[1]
        
        if -30 >= self.position[0] >= SCREEN_WIDTH + 30:
            self.kill()
        
        if -30 >= self.position[1] >= SCREEN_HEIGHT + 30:
            self.kill()

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.split()

    def split(self):

        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS * 2:

            return
        
        ra = random.uniform(60, 90)

        a = self.velocity.rotate(ra)
        b = self.velocity.rotate(-ra)
        c = self.velocity

        new_radius = self.radius - (2 * ASTEROID_MIN_RADIUS)
        new_kind = self.kind - 1 
        asteroid = BossAsteroid(self.position.x, self.position.y, new_radius, new_kind)
        asteroid.velocity = a * 1.4
        asteroid = BossAsteroid(self.position.x, self.position.y, new_radius, new_kind)
        asteroid.velocity = b * 1.4
        asteroid = BossAsteroid(self.position.x, self.position.y, new_radius, new_kind)
        asteroid.velocity = c * 1.2

