import pygame 
import random
import numpy

WIDTH = 800
HEIGHT = 800 
FPS = 30
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
SPEED = 5
ROTATE_SPEED = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.Surface((40, 40))
        pygame.draw.rect(self.image_orig, GREEN, [10, 0, 20, 20])
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.center = (x, y)
        self.rot = 0
        self.rot_speed = 0
        self.speed_forward = 5

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x -= self.speed_forward * numpy.sin(2 * numpy.pi * self.rot / 360)
        self.rect.y -= self.speed_forward * numpy.cos(2 * numpy.pi * self.rot / 360)
        if self.rect.right > WIDTH - 50:
            self.rect.right = WIDTH - 50 
        if self.rect.left < 50:
            self.rect.left = 50 
        if self.rect.top < 50:
            self.rect.top = 50 
        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50 



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TANKS")
clock = pygame.time.Clock()
all_players = pygame.sprite.Group()
player1 = Player(WIDTH / 4, HEIGHT / 4 )
player2 = Player(3 * WIDTH / 4, 3 * HEIGHT / 4)
all_players.add(player1)
all_players.add(player2)


screen.fill(GRAY)
running = True 
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
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

    all_players.update()
    screen.fill(GRAY)
    all_players.draw(screen)
    pygame.display.flip()
pygame.quit()