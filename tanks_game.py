import pygame 
import random
import numpy 

WIDTH = 800
HEIGHT = 800 
FPS = 30
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.Surface((40, 40))
        pygame.draw.rect(self.image_orig, GREEN, [10, 10, 20, 20])
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.center = (x, y)
        self.rot = 0
        self.rot_speed = 1
        self.speed_x = 5
        self.speed_y = 0

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self, keys):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > WIDTH - 50:
            self.rect.right = WIDTH - 50 



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
    all_players.update(30)
    screen.fill(GRAY)
    all_players.draw(screen)
    pygame.display.flip()
pygame.quit()
