import pygame as pg
from settings import *
from collections import deque
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        # self.image = game.player_img
        self.image = pg.transform.scale(game.player_img, (TILESIZE, TILESIZE)) #increase sprite size to tilesize
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE

    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x!=0 and self.vel.y!=0:
            self.vel *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits:
                if self.vel.x>0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x<0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits:
                if self.vel.y>0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y<0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # self.path = deque([vec(300,300), vec(200,400),vec(400,400),vec(400,200)])
        # self.nextpos = self.path.popleft()
        # self.nextpos = (300,300)
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.mob_img, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(-MOB_SPEED, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.target = game.player


    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(pg.transform.scale(self.game.mob_img, (TILESIZE, TILESIZE)), self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(MOB_SPEED).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.rect.center = self.pos
        # else:
        #     if self.pos != self.nextpos:
        #         move_dist = self.nextpos - self.pos
        #         self.rot = move_dist.angle_to(vec(1, 0))
        #         self.image = pg.transform.rotate(pg.transform.scale(self.game.mob_img, (TILESIZE, TILESIZE)), self.rot)
        #         self.rect = self.image.get_rect()
        #         self.rect.center = self.pos
        #         self.acc = vec(MOB_SPEED).rotate(-self.rot)
        #         self.acc += self.vel * -1
        #         self.vel += self.acc * self.game.dt
        #         self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        #         self.rect.center = self.pos
                # print("Entered")
                # self.dist = self.nextpos - self.pos
                # print(self.pos)
                # print(self.dist)
                # if (self.dist.x) < 0 :
                #     self.vel.x = -MOB_SPEED
                #     print("1")
                # elif (self.dist.x) > 0:
                #     self.vel.x = MOB_SPEED
                #     print("2")

                # if (self.dist.y) < 0 :
                #     self.vel.y = -MOB_SPEED
                #     print(self.dist.y)
                # elif (self.dist.y) > 0:
                #     self.vel.y = MOB_SPEED
                #     print(self.dist.y)
                # print(self.dist.y)
                # self.vel *= 0.7071
                # self.pos += self.vel * self.game.dt
                # self.rect.center = self.pos
            # else:
            #     # print("Else")
            #     self.path.append(self.nextpos)
            #     self.nextpos = self.popleft()

                # self.direction = self.nextpos - self.pos
                # self.acc = vec(MOB_SPEED).rotate(-1)
                # self.acc += self.vel * -1
                # self.vel += self.acc * self.game.dt
                # self.pos += self.vel
                # self.rect.center = self.pos
            # else:
                # self.path.append(self.nextpos)
                # self.nextpos = self.popleft()
            # if self.rect.center[0]>= 150 and self.rect.center[1] :
            #     self.vel.x =


        # enemy_time = pg.time.get_ticks()
        # if enemy_time % 3000 == 0:
        #     t = rand(2000,4000)

        # if enemy_time % t*2 <= t:
        #     self.vel.x = -MOB_SPEED
        #     self.pos += self.vel * self.game.dt
        #     self.rect.center = self.pos

        # elif enemy_time % t*2 >= t:
        #     self.vel.x = MOB_SPEED
        #     self.pos += self.vel * self.game.dt
        #     self.rect.center = self.pos

        #     #print(enemy_time)
        #     # if(self.rect.center[0] <= 100):
        #     #     self.vel.x = MOB_SPEED
        #     #     self.repgct.center += self.vel * self.game.dt

        #     #Can be bound to area by giving x and y a limit



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
