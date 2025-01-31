import sys
import pygame
import pygame.freetype
import pickle
from constants import *
from player import Player
from asteroid import *
from asteroidfield import AsteroidField
from upgrades import Upgrade
from shot import Shot



def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    GAME_FONT = pygame.freetype.Font("arial.ttf", 24)
    filename = 'HighScore.pk'
    keys = pygame.key.get_pressed()

    
    with open(filename, 'rb') as fi:
        HIGH_SCORE = pickle.load(fi)

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    boss_asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    upgrades = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    Asteroid.containers = (asteroids, updateable, drawable)
    AsteroidField.containers = (updateable)
    BossAsteroid.containers = (boss_asteroids, updateable, drawable)
    Upgrade.containers = (upgrades, updateable, drawable)
    Shot.containers = (shots, updateable, drawable)
    asteroid_field = AsteroidField()
    #upgrade_field = UpgradeField()

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    dt = 0
    High = False
    upgrade = Upgrade(300, 500)
    small = 0
    upgrade_time = 0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        for obj in asteroids or boss_asteroids:
            if obj.collides_with(player):

                score = 3 * player.killed[0] + 2 * player.killed[1] + player.killed[2] + 5 * player.boss_kills + 2 * sum(player.upgrades)

                if score > HIGH_SCORE:
                    High = True
                    HIGH_SCORE = score
                    with open(filename, 'wb') as fi:
                        # dump your data into the file
                        pickle.dump(HIGH_SCORE, fi)

                screen.fill("black")

                if High:
                    text_surface, rect = GAME_FONT.render("New High Score", (255, 223, 0))
                    screen.blit(text_surface, (550, 240)) 

                text_surface, rect = GAME_FONT.render(f"Score = {score}", (255, 255, 255))
                screen.blit(text_surface, (520, 200))

                text_surface, rect = GAME_FONT.render("Press Space to Quit", (255, 255, 255))
                screen.blit(text_surface, (500, 350))
                    
                pygame.display.flip()

                dt = clock.tick(60) / 1000

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return

                    if keys[pygame.K_SPACE]:
                        sys.exit()
                #sys.exit()

        for obj in asteroids:
            for shot in shots:
                if obj.collides_with(shot) and obj.invincible <= 0:
                    shot.hits += 1
                    if shot.hits >= 1 + player.upgrades[3]:
                        shot.kill()
                    player.kills += 1
                    obj.split()
                    if obj.radius == ASTEROID_MIN_RADIUS and len(upgrades)== 0 and small >= 10 and upgrade_time >= dt:
                        upgrade = Upgrade(obj.position.x, obj.position.y)
                        small = 0
                        upgrade_time = -10
                    if obj.radius == ASTEROID_MIN_RADIUS:
                        player.killed[0] += 1
                        small += 1
                    elif obj.radius == ASTEROID_MAX_RADIUS:
                        player.killed[2] += 1
                    else:
                        player.killed[1] += 1

        for obj in boss_asteroids:
            for shot in shots:
                if obj.collides_with(shot) and obj.invincible <= 0:
                    shot.hits += 1
                    if shot.hits >= 1 + player.upgrades[3]:
                        shot.kill()
                    obj.hit(SHOT_DAMAGE + player.upgrades[4])

        
        for obj in upgrades:
            if obj.collides_with(player):
                obj.kill()
                player.upgrades[obj.upgrade] += 1

        for obj in updateable:
            obj.update(dt)

        screen.fill("black")


        text_surface, rect = GAME_FONT.render(f"{player.kills} Asteroids destroyed! {asteroid_field.spawns}", (255, 255, 255))
        screen.blit(text_surface, (1, 1))

        for obj in drawable:
            obj.draw(screen)

        
        pygame.display.flip()

        dt = clock.tick(60) / 1000
        upgrade_time += dt


if __name__ == "__main__":
    main()
