import pygame 
import random
import numpy 
import pathlib

WIDTH = 800
HEIGHT = 800 
FPS = 30
SPEED = 30
ROTATE_SPEED = 1
KOEF_SPEED = 10
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
RED = (250, 0, 0)
BLUE = (0, 0, 250)
BLACK = (0, 0, 0)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, fi):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        pygame.draw.rect(self.image, RED, [4, 2, 2, 6])
        self.image.set_colorkey(BLACK)
        self.rot = fi  
        self.image = pygame.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()
        self.speed_forward = 8 * SPEED
        # константа чтобы снаряд не попадал в тот же танк
        self.rect.center = (x, y)
        self.speed_x = self.speed_forward * numpy.sin(numpy.pi * self.rot / 180)
        self.speed_y = self.speed_forward * numpy.cos(numpy.pi * self.rot / 180)
        self.rect.x -= self.speed_x / KOEF_SPEED
        self.rect.y -= self.speed_y / KOEF_SPEED
        self.xpos = self.rect.x * KOEF_SPEED
        self.ypos = self.rect.y * KOEF_SPEED

    def update(self):
        self.xpos -= self.speed_x
        self.ypos -= self.speed_y
        self.rect.x = self.xpos / KOEF_SPEED
        self.rect.y = self.ypos / KOEF_SPEED
        if (self.rect.x < 0 or self.rect.x > WIDTH or 
           self.rect.y < 0 or self.rect.y > HEIGHT):
           self.kill()




class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = player_img
        #pygame.Surface((40, 40))
        #pygame.draw.rect(self.image_orig, GREEN, [10, 0, 20, 20])
        self.image = self.image_orig.copy()
        #self.image_orig.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.center = (x, y)
        self.xpos = self.rect.x * KOEF_SPEED
        self.ypos = self.rect.y * KOEF_SPEED
        self.rot = 0
        self.rot_speed = 0
        self.speed_forward = 0

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center


    def update(self):
        self.rotate()
        self.xpos -= self.speed_forward * numpy.sin(numpy.pi * self.rot / 180)
        self.ypos -= self.speed_forward * numpy.cos(numpy.pi * self.rot / 180)
        self.rect.x = self.xpos / KOEF_SPEED
        self.rect.y = self.ypos / KOEF_SPEED
        if self.rect.right > WIDTH + 50:
            self.rect.right = WIDTH + 50 
        if self.rect.left < -50:
            self.rect.left = -50 
        if self.rect.top < -50:
            self.rect.top = -50 
        if self.rect.bottom > HEIGHT + 50:
            self.rect.bottom = HEIGHT + 50 

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.rot)
        bullets.add(bullet)
        all_sprites.add(bullet)




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TANKS")
clock = pygame.time.Clock()

player_img = pygame.transform.scale(pygame.image.load(pathlib.Path(
    r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", "tank1.png"
    )), (60, 60)).convert()

all_players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player1 = Player(WIDTH / 4, HEIGHT / 4 )
player2 = Player(3 * WIDTH / 4, 3 * HEIGHT / 4)
all_players.add(player1)
all_players.add(player2)

all_sprites.add(player1, player2)

screen.fill(GRAY)
running = True 
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                player1.shoot()
            if event.key == pygame.K_DOWN:
                player1.speed_forward = -SPEED
            if event.key == pygame.K_UP:
                player1.speed_forward = SPEED
            if event.key == pygame.K_LEFT:
                player1.rot_speed = ROTATE_SPEED
            if event.key == pygame.K_RIGHT:
                player1.rot_speed = -ROTATE_SPEED
            if event.key == pygame.K_s:
                player2.speed_forward = -SPEED
            if event.key == pygame.K_w:
                player2.speed_forward = SPEED
            if event.key == pygame.K_a:
                player2.rot_speed = ROTATE_SPEED
            if event.key == pygame.K_d:
                player2.rot_speed = -ROTATE_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                player1.speed_forward = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1.rot_speed = 0
            if event.key == pygame.K_s or event.key == pygame.K_w:
                player2.speed_forward = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player2.rot_speed = 0

    all_sprites.update()
    screen.fill(GRAY)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()