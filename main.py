import pygame, sys, os, random

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
os.system('cls')

clock = pygame.time.Clock()

WINDOW_SIZE = (1300, 800)
DISPLAY_SIZE = (288, 162)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((288, 162))

#CONSTS
FPS = 60
TILE_SIZE = 16
GRAVITY = 0.15

#COLORS
COLOR_BG = (25, 42, 84)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#dobra background color: (14, 19, 25)

#STUFF
level = 3
scroll = [0, 0]
screen_shake = 0
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ragdoll_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
playercloud_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
group_group = [bg_group, player_group, enemy_group, ragdoll_group, bullet_group, playercloud_group, flag_group]

#IMAGES
tile_topleft_img = pygame.image.load("data/media/tiles/tile_topleft.png").convert_alpha()
tile_top_img = pygame.image.load("data/media/tiles/tile_top.png").convert_alpha()
tile_topright_img = pygame.image.load("data/media/tiles/tile_topright.png").convert_alpha()
tile_left_img = pygame.image.load("data/media/tiles/tile_left.png").convert_alpha()
tile_middle_img = pygame.image.load("data/media/tiles/tile_middle.png").convert_alpha()
tile_right_img = pygame.image.load("data/media/tiles/tile_right.png").convert_alpha()
tile_bottomleft_img = pygame.image.load("data/media/tiles/tile_bottomleft.png").convert_alpha()
tile_bottom_img = pygame.image.load("data/media/tiles/tile_bottom.png").convert_alpha()
tile_bottomright_img = pygame.image.load("data/media/tiles/tile_bottomright.png").convert_alpha()
spike_up_img = pygame.image.load("data/media/tiles/spike_up.png").convert_alpha()
spike_down_img = pygame.image.load("data/media/tiles/spike_down.png").convert_alpha()
spike_right_img = pygame.image.load("data/media/tiles/spike_right.png").convert_alpha()
spike_left_img = pygame.image.load("data/media/tiles/spike_left.png").convert_alpha()
spike_cave_up_img = pygame.image.load("data/media/tiles/spike_cave_up.png").convert_alpha()
spike_cave_down_img = pygame.image.load("data/media/tiles/spike_cave_down.png").convert_alpha()
cave_left_img = pygame.image.load("data/media/tiles/cave_left.png").convert_alpha()
cave_right_img = pygame.image.load("data/media/tiles/cave_right.png").convert_alpha()
cave_top_img =pygame.image.load("data/media/tiles/cave_top.png").convert_alpha()
cave_bottom_img = pygame.image.load("data/media/tiles/cave_bottom.png").convert_alpha()
cave_bottomright_img = pygame.image.load("data/media/tiles/cave_bottomright.png").convert_alpha()
cave_bottomleft_img = pygame.image.load("data/media/tiles/cave_bottomleft.png").convert_alpha()
cave_bg_left_img = pygame.image.load("data/media/tiles/cave_bg_left.png").convert_alpha()
cave_bg_right_img =pygame.image.load("data/media/tiles/cave_bg_right.png").convert_alpha()
cave_bg_img =pygame.image.load("data/media/tiles/cave_bg.png").convert_alpha()
cave_bg_skull_img =pygame.image.load("data/media/tiles/cave_bg_skull.png").convert_alpha()
cave_bg_bones_img = pygame.image.load("data/media/tiles/cave_bg_bones.png").convert_alpha()

player_idle_img = pygame.image.load("data/media/characters/player/idle.png").convert_alpha()
player_jump_img = pygame.image.load("data/media/characters/player/jump.png").convert_alpha()
player_run_img_1 = pygame.image.load("data/media/characters/player/run1.png").convert_alpha()
player_run_img_2 = pygame.image.load("data/media/characters/player/run2.png").convert_alpha()
player_dead_img = pygame.image.load("data/media/characters/player/dead.png").convert_alpha()

enemy_idle_img = pygame.image.load("data/media/characters/enemy/idle.png").convert_alpha()
enemy_run1_img = pygame.image.load("data/media/characters/enemy/run1.png").convert_alpha()
enemy_run2_img = pygame.image.load("data/media/characters/enemy/run2.png").convert_alpha()
enemy_dead1_img = pygame.image.load("data/media/characters/enemy/dead1.png").convert_alpha()
enemy_dead2_img = pygame.image.load("data/media/characters/enemy/dead2.png").convert_alpha()

flag_0_img = pygame.image.load("data/media/flag/0.png").convert_alpha()
flag_1_img = pygame.image.load("data/media/flag/1.png").convert_alpha()
flag_2_img = pygame.image.load("data/media/flag/2.png").convert_alpha()

test_img = pygame.image.load("data/media/test.png")

#SOUNDS
#run1_sound = pygame.mixer.Sound('data/media/sound/run1.wav')
#run2_sound = pygame.mixer.Sound('data/media/sound/run2.wav')
jump_sound = pygame.mixer.Sound('data/media/sound/jump.wav')
shoot_sound = pygame.mixer.Sound('data/media/sound/shoot.wav')
player_death_sound = pygame.mixer.Sound('data/media/sound/player_death.wav')
enemy_death_sound = pygame.mixer.Sound('data/media/sound/enemy_death.wav')

jump_sound.set_volume(0.02)
shoot_sound.set_volume(0.15)
player_death_sound.set_volume(0.15)
enemy_death_sound.set_volume(0.15)



class World:
    def __init__(self):
        global level
        self.loadLevel(level)

    def loadLevel(self, level):
        #deleting existing elements
        for group in group_group:
            group.empty()

        #loading in map
        global scroll
        scroll = [0, 0]
        self.game_map = []
        f = open("data/levels/" + str(level) + ".csv",'r') 
        data = f.read()
        f.close()
        data = data.split('\n')
        for row in data:
            self.game_map.append(row.split(','))

    
        #assigning tile properties
        self.tiles = []  #[type, img, xy_coords, rect]              
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.tiles.append( ["main", tile_topleft_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] )
                if tile == '1':
                    self.tiles.append( ["main", tile_top_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] )
                if tile == '2':
                    self.tiles.append( ["main", tile_topright_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] )
                if tile == '3':
                    self.tiles.append( ["main", tile_left_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] )
                if tile == '4':
                    self.tiles.append( ["main", tile_middle_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] ) 
                if tile == '5':
                    self.tiles.append( ["main", tile_right_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] ) 
                if tile == '6':
                    self.tiles.append( ["main", tile_bottomleft_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] ) 
                if tile == '7':
                    self.tiles.append( ["main", tile_bottom_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] ) 
                if tile == '8':
                    self.tiles.append( ["main", tile_bottomright_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)] ) 
                if tile == '9':
                    self.tiles.append( ["spike", spike_up_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] + 9), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + 9, spike_up_img.get_width(), spike_up_img.get_height())] )
                if tile == '10':
                    self.tiles.append( ["spike", spike_down_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 2), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE - 2, spike_down_img.get_width(), spike_down_img.get_height())] )
                if tile == '11':
                    self.tiles.append( ["spike", spike_left_img, (x * TILE_SIZE - scroll[0] + 8, y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE + 8, y * TILE_SIZE - 4, spike_left_img.get_width(), spike_left_img.get_height())] )
                if tile == '12':
                    self.tiles.append( ["spike", spike_right_img, (x * TILE_SIZE - scroll[0] - 1, y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE -4, spike_right_img.get_width(), spike_right_img.get_height())] )
                if tile == '13':
                    global player
                    player = Player(x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1])
                if tile == '14':
                    enemy = Enemy(x * TILE_SIZE - scroll[0] + 8, y * TILE_SIZE - scroll[1]  + 8, "stationary")  
                if tile == '15':
                    enemy = Enemy(x * TILE_SIZE - scroll[0] + 8, y * TILE_SIZE - scroll[1] + 8, "patrol")
                if tile == '16':
                    self.tiles.append( ["spike", spike_cave_up_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, spike_right_img.get_width(), spike_right_img.get_height())] )
                if tile == '17':
                    flag = Flag(x * TILE_SIZE - scroll[0] + 6, y * TILE_SIZE - scroll[1] - 7)
                if tile == '18':
                    self.tiles.append( ["background", cave_bg_left_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_bg_right_img.get_width(), cave_bg_right_img.get_height())] )
                if tile == '19':
                    self.tiles.append( ["spike", spike_cave_down_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1] - 2), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE - 2, spike_right_img.get_width(), spike_right_img.get_height() - 5)] )
                if tile == '20':
                    self.tiles.append( ["background", cave_bg_right_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_bg_left_img.get_width(), cave_bg_left_img.get_height())] )
                if tile == '21':
                    self.tiles.append( ["background", cave_bg_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_bg_img.get_width(), cave_bg_img.get_height())] )
                if tile == '22':
                    self.tiles.append( ["background", cave_bg_skull_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_bg_skull_img.get_width(), cave_bg_skull_img.get_height())] )
                if tile == '23':
                    self.tiles.append( ["background", cave_bg_bones_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_bg_bones_img.get_width(), cave_bg_bones_img.get_height())] )
                if tile == '24':
                    self.tiles.append( ["main", cave_bottomright_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_bottomright_img.get_width(), cave_bottomright_img.get_height())] )
                if tile == '25':
                    self.tiles.append( ["main", cave_top_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_top_img.get_width(), cave_top_img.get_height())] )
                if tile == '26':
                    self.tiles.append( ["main", cave_bottomleft_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_bottomleft_img.get_width(), cave_bottomleft_img.get_height())] )
                if tile == '27':
                    self.tiles.append( ["main", cave_left_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_left_img.get_width(), cave_left_img.get_height())] )
                if tile == '28':
                    self.tiles.append( ["main", cave_bottom_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_bottom_img.get_width(), cave_bottom_img.get_height())] )
                if tile == '29':
                    self.tiles.append( ["main", cave_right_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, cave_right_img.get_width(), cave_right_img.get_height())] )
                x += 1
            y += 1


    def draw(self):
        display.blit(test_img, (-550 - scroll[0] * 0.1, -900 - scroll[1] * 0.05))
        for tile in self.tiles:
            if tile[0] == "background":
                display.blit(tile[1], (tile[2][0] - scroll[0], tile[2][1] - scroll[1]))
        for tile in self.tiles:
            if tile[0] == "main":
                display.blit(tile[1], (tile[2][0] - scroll[0], tile[2][1] - scroll[1]))
        for tile in self.tiles:
            if tile[0] == "spike":
                display.blit(tile[1], (tile[2][0] - scroll[0], tile[2][1] - scroll[1]))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, player_group)
        self.x = x
        self.y = y
        self.speed = 2
        self.vel_y = 0
        self.run_img = [player_run_img_1, player_run_img_2]
        self.img = player_idle_img
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.flipped = False
        self.jumping = False
        self.grounded = False
        self.running_timer = 0
        self.shoot_cooldown = 2
        self.dead = False

    def update(self):
        if not self.dead:
            dx = 0
            dy = 0

            #check if on ground
            for tile in world.tiles:
                    if tile[0] == "main":
                        if tile[3].colliderect(self.rect.x, self.rect.y + 1, self.width, self.height):
                            self.grounded = True
                            break
                        else:
                            self.grounded = False

            #movement
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                dx -= self.speed
                self.flipped = True
            if key[pygame.K_d]:
                dx += self.speed
                self.flipped = False
            if key[pygame.K_w] and self.grounded:
                self.vel_y -= 4
                self.jumping = True
                jump_sound.play()
            elif key[pygame.K_w] and not self.grounded and self.jumping == False: #Note to future riki: Zasto dva uslova za skok? Prvi je za kad je na zemlji i skoci (Pocetni velocity 0 + 2), drugi je za kad vec pada (Pocetni velocity -2 + 6)
                self.vel_y -= 6
                self.jumping = True
                cloud = PlayerCloud()
                jump_sound.play()
            if key[pygame.K_x] and self.shoot_cooldown <= 0:
                bullet = Bullet(self, "player", self.flipped)
                self.shoot_cooldown = 2 * FPS
                shoot_sound.play()
            self.shoot_cooldown -= 1

            #animation
            if not self.grounded:
                self.img = player_jump_img
            elif key[pygame.K_a] or key[pygame.K_d]:
                if self.running_timer % 7 == 0:
                    if self.running_timer % 14 == 0:
                        self.img = self.run_img[0]
                        #run1_sound.play()
                    else:
                        self.img = self.run_img[1]
                        #run2_sound.play()
                self.running_timer += 1
            else:
                self.img = player_idle_img
            
            #physics
            if not self.grounded:
                self.vel_y += GRAVITY
            else:
                self.vel_y += 0

            if self.vel_y > 0:
                self.vel_y = min(self.vel_y, 2) 
            if self.vel_y < 0:
                if self.vel_y < -4:
                    self.vel_y = -4
            dy += self.vel_y               #Note to future riki: Zasto je ovdje komplikovan kod? Kada bi skocio sa poda sve bi bilo ok, ali kada skoci cim padne sa poda (cim postane not grounded), nadoda se odma -6 na velocity sto bi bilo ok da je odam velocity 2 jer 2 - 6 = -4, ali bude 0.15 - 6 = -5.85 sto rezultira u mnogo vecem skoku

            #collision
            global screen_shake
            for tile in world.tiles:
                if tile[0] == "main":
                    #collision in x direction
                    if tile[3].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    #collision in y direction
                    if tile[3].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0: #if jumping
                            dy = tile[3].bottom - self.rect.top
                            self.vel_y = 0
                        if self.vel_y > 0: #if falling
                            dy = tile[3].top - self.rect.bottom
                            self.jumping = False
                            self.vel_y = 0
                if tile[0] == "spike":
                    if tile[3].colliderect(self.rect):
                        self.dead = True
                        ragdoll = Ragdoll()
                        screen_shake = 10
                        player_death_sound.play()
            for bullet in bullet_group:
                if self.rect.colliderect(bullet.rect):
                    self.dead = True
                    ragdoll = Ragdoll()
                    screen_shake = 10
                    bullet.kill()
                    player_death_sound.play()
            for flag in flag_group:
                if self.rect.colliderect(flag.rect):
                    global level
                    level += 1
                    world.loadLevel(level)

            self.rect.x += dx
            self.rect.y += dy

            display.blit(pygame.transform.flip(self.img, self.flipped, False), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.width, self.height))
            

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, mode):
        pygame.sprite.Sprite.__init__(self, enemy_group)
        self.x = x
        self.y = y
        self.img = enemy_idle_img
        self.rect = self.img.get_rect(center = (x, y))
        self.speed = 1
        self.mode = mode
        self.original_mode = mode
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.flipped = False
        self.grounded = False
        self.wait_timer = 0
        self.running_timer = 0
        self.shoot_timer = 10
        self.attack_timer = 0
        self.dead_timer = 0
        self.original_rect_x = 0
        #modes: stationary, patrol, attack, dead

    def update(self):
        if not player.dead and not self.mode == "dead":
            if player.rect.y >= self.rect.y and player.rect.y <= self.rect.y + self.height:
                    if self.flipped:
                        distance = self.rect.x - player.rect.x 
                    else:
                        distance = player.rect.x - self.rect.x 
                    if distance < 120 and distance > 0:
                        self.mode = "attack"
                        self.attack_timer = FPS * 5
                    
        if self.mode != "dead":
            for bullet in bullet_group:
                if self.rect.colliderect(bullet.rect):
                    self.mode = "dead"
                    self.rect.x -= 4
                    bullet.kill()
                    enemy_death_sound.play()

        if self.mode == "stationary":
            self.img = enemy_idle_img
            if self.wait_timer == 3 * FPS:
                self.flipped = not self.flipped
                self.wait_timer = 0
            self.wait_timer += 1

        if self.mode == "patrol":
            dx = 0
            self.grounded = False

            for tile in world.tiles:
                if tile[3].colliderect(self.rect.x + dx, self.rect.y, self.height, self.height):
                    dx = 0
                    self.flipped = not self.flipped 

                if self.flipped:
                    if tile[3].colliderect(self.rect.x - 12, self.rect.y + self.height, self.height, self.height):
                        self.grounded = True
                else:
                    if tile[3].colliderect(self.rect.x + 5, self.rect.y + self.height, self.height, self.height):
                        self.grounded = True

            if not self.grounded:
                self.flipped = not self.flipped

            if self.flipped:
                dx -= self.speed
            else:
                dx += self.speed
            self.rect.x += dx

            if self.running_timer % 8 == 0:
                if self.running_timer % 16 == 0:
                    self.img = enemy_run1_img
                else:
                    self.img = enemy_run2_img
            self.running_timer += 1

        if self.mode == "attack":
            pass
            self.img = enemy_idle_img
            if self.shoot_timer == 0:
                bullet = Bullet(self, "enemy", self.flipped)
                self.shoot_timer = FPS * 1
            self.shoot_timer -= 1
            if self.attack_timer <= 0 or player.dead:
                self.mode = self.original_mode
            self.attack_timer -= 1

        if self.mode == "dead":
            if self.original_rect_x == 0:
                self.original_rect_x = self.rect.x
            if self.dead_timer < 30:
                self.img = enemy_dead1_img
            else:
                self.img = enemy_dead2_img
                if self.flipped:
                    self.rect.x = self.original_rect_x - 5
                else:
                    self.rect.x = self.original_rect_x + 5
            self.dead_timer += 1

        display.blit(pygame.transform.flip(self.img, self.flipped, False), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.width, self.height))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, source, type, direction):
        pygame.sprite.Sprite.__init__(self, bullet_group)
        self.direction = direction
        if self.direction:
            self.x = source.rect.x - 2
        else:
            self.x = source.rect.x + source.width + 2
        self.y = source.rect.y + 7
        if type == "player":
            self.img = pygame.image.load("data/media/bullets/bullet_player.png")
            self.life_timer = 20
        elif type == "enemy":
            self.img = pygame.image.load("data/media/bullets/bullet_enemy.png") 
            self.life_timer = 100
        self.rect = self.img.get_rect(center = (self.x, self.y))
        self.direction = source.flipped
        self.speed = 4

    def update(self):
        if self.direction:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        display.blit(self.img, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.img.get_width(), self.img.get_height()))

        for tile in world.tiles:
            if tile[0] == "main":
                if self.rect.colliderect(tile[3]):
                    self.kill()
        if self.life_timer <= 0:
            self.kill()
        self.life_timer -= 1

class PlayerCloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, playercloud_group)
        self.x = player.rect.x + 4
        self.y = player.rect.y + 12
        self.img = pygame.image.load("data/media/cloud.png").convert_alpha()
        self.rect = self.img.get_rect(center = (self.x, self.y))

    def update(self):
        self.img.set_alpha(self.img.get_alpha() - 6)
        display.blit(self.img, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.img.get_width(), self.img.get_height()))
        
        if self.img.get_alpha() == 0:
            self.kill()
        
class Ragdoll(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, ragdoll_group)
        self.x = player.rect.x
        self.y = player.rect.y 
        self.img = player_dead_img
        self.rect = self.img.get_rect(center = player.rect.center)

        self.vel_y = -3
        self.dead_timer = 120

    def update(self):
        self.vel_y += GRAVITY
        if self.vel_y > 0:
            self.vel_y = min(self.vel_y, 2)

        self.rect.y += self.vel_y

        display.blit(self.img, (self.rect.x - scroll[0], self.rect.y - scroll[1], self.img.get_width(), self.img.get_height()))

        if self.dead_timer == 0:
            world.loadLevel(level)
        self.dead_timer -= 1

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, flag_group)
        self.x = x
        self.y = y
        self.img = [flag_0_img, flag_1_img, flag_2_img, flag_1_img]
        self.index = 0
        self.rect = self.img[self.index].get_rect(topleft = (self.x, self.y))
        self.width = self.img[0].get_width()
        self.height = self.img[0].get_height()

        self.img_timer = 10

    def update(self):
        self.img_timer -= 1
        if self.img_timer == 0:
            self.index = (self.index + 1) % 4 #modul makes sure that it iterates to the beggining when it reaches the end (4 % 4  = 0)
            self.img_timer = 10

        display.blit(self.img[self.index], (self.rect.x - scroll[0], self.rect.y - scroll[1], self.width, self.height))

class BgObject(pygame.sprite.Sprite):
    def __init__(self, x, y, img, parallax):
        pygame.sprite.Sprite.__init__(self, bg_group)
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect(topleft = (self.x, self.y))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.parallax = parallax

    def update(self):
        self.rect = (self.x - scroll[0] * self.parallax, self.y, self.width, self.height)
        display.blit(self.img, self.rect)
                

def main():
    global world, screen_shake
    world = World()
    while True:
        display.fill(COLOR_BG)
        world.draw()

        for group in group_group:
            for element in group:
                element.update()


        if player.rect.y < ((len(world.game_map) - 5) * 16): 
            scroll[0] +=  (player.rect.x - scroll[0] - 141) / 15
            scroll[1] += (player.rect.y - scroll[1] - 75) / 15
        elif player.rect.y > (len(world.game_map) * 16):
            world.loadLevel(level)

        if screen_shake:
            scroll[0] += random.randint(-3, 3)
            scroll[1] += random.randint(-3, 3)                
            screen_shake -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

main()