import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot



class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.upgrades = [0, 0, 0, 0, 0]
        self.kills = 0
        self.killed = [0 ,0, 0]
        self.boss_kills = 0
        # movement speed, shot speed, bullet size, bullet pierce, bullet damage

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        self.wrap()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * (PLAYER_SPEED + 50 * self.upgrades[0]) * dt

    def shoot(self):
        if self.timer > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN - (0.1 * self.upgrades[1])

    def wrap(self):
        if self.position[0] <= 0:
            a = self.position[0]
            self.position[0] = SCREEN_WIDTH + a
        
        if self.position[0] >= SCREEN_WIDTH:
            a = SCREEN_WIDTH - self.position[0]
            self.position[0] = a

        if self.position[1] <= 0:
            a = self.position[1]
            self.position[1] = SCREEN_HEIGHT + a

        if self.position[1] >= SCREEN_HEIGHT:
            a = SCREEN_HEIGHT - self.position[1]
            self.position[1] = a