import pygame 
import random
import numpy 
import pathlib
GAME_RUNNUNG = True 
WIDTH = 1000
HEIGHT = 800 
FPS = 30
KOEF_SPEED = 10
SPEED = 3 * KOEF_SPEED
BACK_SPEED = KOEF_SPEED
ROTATE_SPEED = 2
SHOOT_DELAY = 2000
BAR_HEIGHT = 50
START_AMMO = 10
SUPPLY_FR = 30000
RESPAWN_TIME = 5000
DESTR_TANK_DRAG = 1 * KOEF_SPEED
DESPAWN_DESTR_TANK_DELAY = 60000
GRAY = (150, 150, 150)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
RED = (250, 0, 0)
BLUE = (0, 0, 250)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BAR_COLOUR = (250, 200, 50)

class Destroyed_tank(pygame.sprite.Sprite):
    def __init__(self, x, y, fi):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(destr_img, fi)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.center = (x, y)
        self.xpos = self.rect.x * KOEF_SPEED
        self.ypos = self.rect.y * KOEF_SPEED
        self.hit_points = 100
        self.ammo = START_AMMO
        self.destr = pygame.time.get_ticks()
        all_sprites.add(self)
        all_destr.add(self)

    def update(self):
        self.rect.x = self.xpos / KOEF_SPEED
        self.rect.y = self.ypos / KOEF_SPEED
        now = pygame.time.get_ticks()
        if now - self.destr > DESPAWN_DESTR_TANK_DELAY:
            self.kill()

    def damage(self, hp_lost):
        self.hit_points -= hp_lost
        if self.hit_points <= 0:
            exp = Expl(*self.rect.center)
            all_sprites.add(exp)
            self.kill()

class Expl(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = expl_img[0]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 50
        self.rect.center = (x, y)
        self.current_img = 0
        self.time_change = pygame.time.get_ticks()
        all_expls.add(self)
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.time_change > 100:
            self.current_img += 1
            self.time_change = now
        if self.current_img == len(shoot_img):
            self.kill()
        else:
            self.image = expl_img[self.current_img]
            self.image.set_colorkey(WHITE)
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = dot_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 37
        print(self.rect)
        self.rect.x = x - 50
        self.rect.y = y - 50
    
    def update(self):
        pass
class Supplises(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = supply_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.radius = 15
    
    def update(self):
        pass
class Fires(pygame.sprite.Sprite):
    def __init__(self, x, y, fi):
        pygame.sprite.Sprite.__init__(self)
        self.rot = fi
        self.image = pygame.transform.rotate(shoot_img[0], self.rot)
        self.image.set_colorkey(WHITE)
        self.shoot_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.current_img = 0
        self.time_change = pygame.time.get_ticks()
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.time_change > 100:
            self.current_img += 1
            self.time_change = now
        if self.current_img == len(shoot_img):
            self.kill()
        else:
            self.image = pygame.transform.rotate(shoot_img[self.current_img], self.rot)
            self.image.set_colorkey(WHITE)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, fi):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        pygame.draw.rect(self.image, RED, [3, 2, 4, 6])
        self.image.set_colorkey(BLACK)
        self.rot = fi  
        self.image = pygame.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()
        self.radius = 2
        self.speed_forward = 8 * SPEED
        # константа чтобы снаряд не попадал в тот же танк
        self.rect.center = (x, y)
        self.speed_x = self.speed_forward * numpy.sin(numpy.pi * self.rot / 180)
        self.speed_y = self.speed_forward * numpy.cos(numpy.pi * self.rot / 180)
        self.rect.x -= 1.6 * self.speed_x / KOEF_SPEED
        self.rect.y -= 1.6 * self.speed_y / KOEF_SPEED
        self.xpos = self.rect.x * KOEF_SPEED
        self.ypos = self.rect.y * KOEF_SPEED
        fires = Fires(*self.rect.center, fi)
        fires.add(all_sprites)
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
        self.image = self.image_orig.copy()
        self.image_orig.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.center = (x, y)
        self.xpos = self.rect.x * KOEF_SPEED
        self.ypos = self.rect.y * KOEF_SPEED
        self.rot = 0
        self.rot_speed = 0
        self.speed_forward = 0
        self.speed_x = 0
        self.speed_y = 0
        self.hit_points = 100
        self.ammo = START_AMMO
        self.last_shoot = pygame.time.get_ticks()
        self.looses = 0
        self.destroyed = -5000
        self.zn_sp = 1
    def rotate(self):
        self.rot = (self.rot + self.rot_speed * self.zn_sp) % 360
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        self.image = new_image
        self.xpos -= (new_image.get_rect().width - self.rect.width) * KOEF_SPEED / 2
        self.ypos -= (new_image.get_rect().height - self.rect.height) * KOEF_SPEED / 2
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.destroyed > RESPAWN_TIME:
            if self.speed_forward < 0:
                self.zn_sp = -1
            else:
                self.zn_sp = 1
            self.rotate()
            self.speed_x = - self.speed_forward * numpy.sin(numpy.pi * self.rot / 180)
            self.speed_y = - self.speed_forward * numpy.cos(numpy.pi * self.rot / 180)
            self.xpos += self.speed_x
            self.ypos += self.speed_y 
            self.rect.x = self.xpos / KOEF_SPEED
            self.rect.y = self.ypos / KOEF_SPEED
            if self.rect.right > WIDTH + 20:
                self.xpos = (WIDTH  + 20 - self.rect.width) * KOEF_SPEED
            if self.rect.left < -20:
                self.xpos = -20 * KOEF_SPEED 
            if self.rect.top < BAR_HEIGHT:
                self.ypos = BAR_HEIGHT * KOEF_SPEED
            if self.rect.bottom > HEIGHT + 20:
                self.ypos = (HEIGHT + 20 - self.rect.height) * KOEF_SPEED
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > SHOOT_DELAY and self.ammo > 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.rot)
            bullets.add(bullet)
            all_sprites.add(bullet)
            self.ammo -= 1
            self.last_shoot = pygame.time.get_ticks()
    def damage(self, hp_lost):
        self.hit_points -= hp_lost
        if self.hit_points <= 0:
            destr = Destroyed_tank(*self.rect.center, self.rot)
            exp = Expl(*self.rect.center)
            all_sprites.add(exp)
            draw_dirt(*self.rect.center)
            self.destroyed = pygame.time.get_ticks()
            self.ypos = random.randint(BAR_HEIGHT + 50, HEIGHT - 50) * KOEF_SPEED
            self.xpos = random.randint(50, WIDTH - 50) * KOEF_SPEED
            self.rect.center = (-200, random.randint(0, 800))
            self.rot = random.randint(0, 359)
            self.hit_points = 100
            self.looses += 1
            self.ammo = START_AMMO


    def supplying(self):
        x = random.randint(10, 40)
        self.hit_points += x
        if self.hit_points > 100:
            self.hit_points = 100
        self.ammo += (40 - x) // 10
def draw_text(text, size, x, y):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
def draw_ammobar(ammo):
    ammobar = pygame.Surface((100, 10))
    ammobar.fill(BAR_COLOUR)
    for i in range(ammo):
        pygame.draw.rect(ammobar, YELLOW, [i * 10 + 2, 3, 6, 8])
        pygame.draw.rect(ammobar, RED, [i * 10 + 4, 0, 2, 1])
        pygame.draw.rect(ammobar, BLACK, [i * 10 + 3, 1, 4, 2])
    return ammobar
def keys_upravl():
    global GAME_RUNNUNG
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUNNUNG = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                draw_text("PAUSE", 50, WIDTH / 2, HEIGHT / 2)
                pygame.display.flip()
                pause = True
                while pause:
                    clock.tick(FPS)
                    for eventpause in pygame.event.get():
                        if eventpause.type == pygame.KEYDOWN:
                            if eventpause.key == pygame.K_p:
                                pause = False
                        if eventpause.type == pygame.QUIT:
                            GAME_RUNNUNG = False 
                            pause = False
                player1.speed_forward = 0
                player2.speed_forward = 0
                player1.rot_speed = 0
                player2.rot_speed = 0
            if event.key == pygame.K_RSHIFT:
                player1.shoot()
            if event.key == pygame.K_SPACE:
                player2.shoot()
            if event.key == pygame.K_DOWN:
                player1.speed_forward = -BACK_SPEED
            if event.key == pygame.K_UP:
                player1.speed_forward = SPEED
            if event.key == pygame.K_LEFT:
                player1.rot_speed = ROTATE_SPEED
            if event.key == pygame.K_RIGHT:
                player1.rot_speed = -ROTATE_SPEED
            if event.key == pygame.K_s:
                player2.speed_forward = -BACK_SPEED
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
def spawn():
    prob_sup = random.randint(0, SUPPLY_FR)
    if prob_sup < 50:
        sup = Supplises(random.randint(50, WIDTH - 50), random.randint(BAR_HEIGHT, HEIGHT - 50))
        all_supplies.add(sup)
        all_sprites.add(sup)

def collids():
    cols_destr_player = pygame.sprite.groupcollide(
        all_players, all_destr, 
        False, False, pygame.sprite.collide_circle
        )
    for item in cols_destr_player:
        for jtem in cols_destr_player.get(item):
            jtem.xpos += item.speed_x / 5
            jtem.ypos += item.speed_y / 5
        item.xpos -= 2 * item.speed_x
        item.ypos -= 2 * item.speed_y
    cols_expl_player = pygame.sprite.groupcollide(
        all_players, all_expls, 
        False, False, pygame.sprite.collide_circle
        )
    for item in cols_expl_player:
        item.damage(10)
    cols_expl_sup = pygame.sprite.groupcollide(
        all_supplies, all_expls, 
        True, False, pygame.sprite.collide_circle
        )
    cols_dot_bul = pygame.sprite.groupcollide(
        all_dots, bullets, 
        False, True, pygame.sprite.collide_circle
        )
    cols_dot_sup = pygame.sprite.groupcollide(
        all_dots, all_supplies, 
        False, True, pygame.sprite.collide_circle
        )
    cols_player_dot = pygame.sprite.groupcollide(
        all_players, all_dots, 
        False, False, pygame.sprite.collide_circle
        )
    for item in cols_player_dot:
        item.damage(0)
        item.xpos -= 2 * item.speed_x
        item.ypos -= 2 * item.speed_y


    cols_suply_player = pygame.sprite.groupcollide(
        all_players, all_supplies,
        False, True, pygame.sprite.collide_circle
        )
    for item in cols_suply_player:
        item.supplying()
    cols_player_bullet = pygame.sprite.groupcollide(
        all_players, bullets,
        False, True, pygame.sprite.collide_circle
        )
    for hit in cols_player_bullet:
        hit.damage(40)
    cols_destr_bullet = pygame.sprite.groupcollide(
        all_destr, bullets,
        False, True, pygame.sprite.collide_circle
        )
    for hit in cols_destr_bullet:
        hit.damage(40)
    for i in all_players:
        for j in all_players:
            if not (i is j):
                colision_group = pygame.sprite.Group()
                colision_group.add(j)
                coli = pygame.sprite.spritecollide(i, colision_group,
                                     False, pygame.sprite.collide_circle
                                     )
                for hit in coli:
                    i.damage(0)
                    i.xpos -= 2 * i.speed_x
                    i.ypos -= 2 * i.speed_y

def interface():
    pygame.draw.rect(screen, BAR_COLOUR, [0, 0, WIDTH, BAR_HEIGHT])
    draw_text(str(player2.looses), 20, WIDTH / 2 + 50, 10)
    draw_text(str(player1.looses), 20, WIDTH / 2 - 50, 10)
    pygame.draw.rect(screen, RED, [50, 10, 100, 10])
    pygame.draw.rect(screen, RED, [WIDTH - 150, 10, 100, 10])
    pygame.draw.rect(screen, GREEN, [50, 10, player2.hit_points, 10])
    pygame.draw.rect(screen, GREEN, [WIDTH - 150, 10, player1.hit_points, 10])
    screen.blit(draw_ammobar(player2.ammo), (50, 30))
    if player2.ammo > 10 :
        draw_text("+", 20, 155, 23)
    screen.blit(draw_ammobar(player1.ammo), (WIDTH - 150, 30))
    if player1.ammo > 10 :
        draw_text("+", 20, WIDTH - 45, 23)
    now = pygame.time.get_ticks()
    for pl in all_players:
        x, y = pl.rect.center
        pygame.draw.rect(screen, BLUE, [x - 10, y + 15, 20, 2])
        if (now - pl.last_shoot) < SHOOT_DELAY:
            pygame.draw.rect(screen, RED,
                [x - 10, y + 15, 20 * (now - pl.last_shoot) / SHOOT_DELAY, 2]
            )
        else:
            pygame.draw.rect(screen, RED, [x - 10, y + 15, 20, 2])

def draw_dirt(x, y):
    grass_surf.blit(pygame.transform.rotate(
        dirt, random.randint(0, 360)),(x - 40, y - 40))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TANKS")
clock = pygame.time.Clock()

# загрузка изображений

dirt = pygame.transform.scale(pygame.image.load(pathlib.Path(
    r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", "dirt_expl.png"
    )), (80, 80)).convert()
dirt.set_colorkey(WHITE)
player_img = pygame.transform.scale(pygame.image.load(pathlib.Path(
    r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", "tank1.png"
    )), (60, 60)).convert()
destr_img = pygame.transform.scale(pygame.image.load(pathlib.Path(
    r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", "destr_tank.png"
    )), (60, 60)).convert()
dot_img = pygame.transform.scale(pygame.image.load(pathlib.Path(
    r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", "dot.png"
    )), (100, 100)).convert()
supply_img = pygame.transform.scale(pygame.image.load(pathlib.Path(
    r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", "supply.png"
    )), (40, 40)).convert()
grass_img = pygame.transform.scale(pygame.image.load(pathlib.Path(
    r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", "grass.png"
    )), (1000, 1000)).convert()
grass_surf = pygame.Surface((1000, 1000))
grass_surf.blit(grass_img, (0, 0))
shoot_img = []
for i in range(2):
    filename = 'shoot{}.png'.format(i+1)
    shoot_img.append(pygame.transform.scale(pygame.image.load(pathlib.Path(
        r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", filename
        )), (20, 20)).convert())
expl_img = []
for i in range(8):
    filename = 'expl{}.png'.format(i)
    expl_img.append(pygame.transform.scale(pygame.image.load(pathlib.Path(
        r"C:\Users\^_^\Desktop\proga\tanks", "tanks_game_images", filename
        )), (150, 150)).convert())
# начало основной части 
all_players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_expls = pygame.sprite.Group()
all_supplies = pygame.sprite.Group()
all_dots = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_destr = pygame.sprite.Group()
player1 = Player(WIDTH / 4, HEIGHT / 4 )
player2 = Player(3 * WIDTH / 4, 3 * HEIGHT / 4)

dot = Dot(500, 400)
all_dots.add(dot)
all_sprites.add(dot)

all_players.add(player1, player2)
#all_sprites.add(player1, player2)

while GAME_RUNNUNG:
    clock.tick(FPS)
    keys_upravl()
    spawn()
    all_sprites.update()
    all_players.update()
    collids()
    screen.blit(grass_surf, (0, 0))
    all_sprites.draw(screen)
    all_players.draw(screen)
    interface()
    pygame.display.flip()
pygame.quit()