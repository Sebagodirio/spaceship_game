import pygame,sys
from pygame.locals import *

#globlas
width = 900
height = 480

class spaceship(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImageSpaceship = pygame.image.load("images/nave.jpg")

        self.rect = self.ImageSpaceship.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = height-30

        self.shootList = []
        self.Life = True

        self.velocity = 20

    def leftMovement(self):
        self.rect.left -=self.velocity
        self.__movement()
        
    def rightMovement(self):
        self.rect.right += self.velocity
        self.__movement()

    def shoot(self,x,y):
        myProy = Proyectil(x,y)
        self.shootList.append(myProy)

    def draw(self,superfice):
        superfice.blit(self.ImageSpaceship,self.rect)

    def __movement(self):
        if self.Life == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > 870:
                self.rect.right = 840

class Proyectil(pygame.sprite.Sprite):
    def __init__(self,posx,posy):
        pygame.sprite.Sprite.__init__(self)

        self.imageProyectil = pygame.image.load("images/disparoa.jpg")
        self.rect = self.imageProyectil.get_rect()
        self.velocityShoot = 4

        self.rect.top = posy
        self.rect.left = posx

    def trayectory(self):
        self.rect.top = self.rect.top - self.velocityShoot

    def draw(self,surface):
        surface.blit(self.imageProyectil,self.rect)

class invader(pygame.sprite.Sprite):
    def __init__(self,posx,posy):
        pygame.sprite.Sprite.__init__(self)

        self.imageA = pygame.image.load("images/MarcianoA.jpg")
        self.imageB = pygame.image.load("images/MarcianoB.jpg")

        self.imageList = [self.imageA,self.imageB]
        self.posImage = 0

        self.invaderImage = self.imageList[self.posImage]
        self.rect = self.invaderImage.get_rect()
        self.shootList = []
        self.velocity = 20

        self.rect.top = posy
        self.rect.left = posx

        self.timeChange = 1

    def draw(self,surface):
        self.invaderImage = self.imageList[self.posImage]
        surface.blit(self.invaderImage,self.rect)
    def behavior(self,time):
        if self.timeChange == time:
            self.posImage += 1 
            self.timeChange += 1

            if self.posImage > len(self.imageList):
                self.posImage = 0

def SpaceInvader():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Space Invader")

    background = pygame.image.load("images/fondo.jpg")

    enemy = invader(100,100)
    player = spaceship()

    demoProy = Proyectil(width/2,height-30)
    inGame = True

    clock = pygame.time.Clock()
    while True:

        clock.tick(60)

        tiempo = pygame.time.get_ticks()/1000
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if inGame == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        player.leftMovement()
                    elif event.key == K_RIGHT:
                        player.rightMovement()
                    elif event.key == K_SPACE:
                         x,y = player.rect.center
                         player.shoot(x,y)
        screen.blit(background,(0,0))
        

        enemy.behavior(tiempo)

        player.draw(screen)
        enemy.draw(screen)

        if len(player.shootList)>0:
            for x in player.shootList:
                x.draw(screen)
                x.trayectory()

                if x.rect.top < -10:
                    player.shootList.remove(x)


        pygame.display.update()

SpaceInvader()