import pygame,sys
from pygame.locals import *

from random import randint

#globlas
width = 900
height = 480
enemyList = []

class SpaceShip(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImageSpaceship = pygame.image.load("images/nave.jpg")

        self.rect = self.ImageSpaceship.get_rect()
        self.rect.centerx = width/2
        self.rect.centery = height-30

        self.shootList = []
        self.Life = True

        self.velocity = 40

    def leftMovement(self):
        self.rect.left -=self.velocity
        self.__movement()
    
    def destruct():

        self.Life = False
        self.velocity = 0


    def rightMovement(self):
        self.rect.right += self.velocity
        self.__movement()

    def shoot(self,x,y):
        myProy = Proyectil(x,y,"images/disparoa.jpg",True)
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
    def __init__(self,posx,posy,ruta,personaje):
        pygame.sprite.Sprite.__init__(self)

        self.imageProyectil = pygame.image.load("images/disparoa.jpg")
        self.rect = self.imageProyectil.get_rect()
        self.velocityShoot = 4

        self.rect.top = posy
        self.rect.left = posx

        self.disparoPersonaje = personaje

    def trayectory(self):
        if self.disparoPersonaje == True:
            self.rect.top = self.rect.top - self.velocityShoot
        else:
            self.rect.top = self.rect.top + self.velocityShoot
        

    def draw(self,surface):
        surface.blit(self.imageProyectil,self.rect)

class Invader(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distance,image1,image2):
        pygame.sprite.Sprite.__init__(self)

        self.imageA = pygame.image.load(image1)
        self.imageB = pygame.image.load(image2)

        self.imageList = [self.imageA,self.imageB]
        self.posImage = 0

        self.invaderImage = self.imageList[self.posImage]
        self.rect = self.invaderImage.get_rect()

        self.shootList = []
        self.velocity = 3

        self.rect.top = posy
        self.rect.left = posx

        self.shootRange = 5
        self.timeChange = 1

        self.conquest = False

        self.right = True
        self.cont = 0
        self.maxDown = self.rect.top + 40

        self.limitRight = posx + distance
        self.limitLeft = posx - distance


    def draw(self,surface):
        self.invaderImage = self.imageList[self.posImage]
        surface.blit(self.invaderImage,self.rect)
    def behavior(self,time):

        if self.conquest == False:

            self.__movement()

            self.__attack()
            if self.timeChange == time:
                self.posImage += 1 
                self.timeChange += 1

                if self.posImage > len(self.imageList)-1:
                    self.posImage = 0

    def __movement(self):
        if self.cont < 3:
            self.__movement_aside()
        else:
            self.__down()
        
    def __down(self):

        if self.maxDown == self.rect.top:
            self.cont = 0
            self.maxDown = self.rect.top + 40
        else:
            self.rect.top += 1

    def __movement_aside(self):
        if self.right == True:
            self.rect.left = self.rect.left + self.velocity
            if self.rect.left > self.limitRight:
                self.right = False
                
        else:
            self.rect.left = self.rect.left - self.velocity
            if self.rect.left < self.limitLeft:
                self.right = True
                self.cont += 1

    def __attack(self):
        if(randint(0,100)<self.shootRange):
            self.__shoot()
    def __shoot(self):
        x,y = self.rect.center
        myProy = Proyectil(x,y,"images/disparob.jpg",False)
        self.shootList.append(myProy)

def stopEverything():
    for enemy in enemyList:
        for shoot in enemy.shootList:
            enemy.shootList.remove(shoot)
        enemy.conquest = True

def enemyCharge():
    posx = 100
    for x in range(1,5):
        enemy = Invader(posx,100,40,'images/MarcianoA.jpg','images/MarcianoB.jpg')
        enemyList.append(enemy)
        posx = posx + 200

    posx = 100
    for x in range(1,5):
        enemy = Invader(posx,0,40,'images/Marciano2A.jpg','images/Marciano2B.jpg')
        enemyList.append(enemy)
        posx = posx + 200
    
    posx = 100
    for x in range(1,5):
        enemy = Invader(posx,-100,40,'images/Marciano3A.jpg','images/Marciano3B.jpg')
        enemyList.append(enemy)
        posx = posx + 200
    

def SpaceInvader():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Space Invader")

    background = pygame.image.load("images/fondo.jpg")

    pygame.mixer.music.load('sounds/008702013_prev.mp3')
    pygame.mixer.music.play(20)

    mySysFont = pygame.font.SysFont("Arial",30)
    Text = mySysFont.render("Fin del juego",0,(120,105,60))

    
    player = SpaceShip()
    enemyCharge()

   
    inGame = True

    reloj = pygame.time.Clock()
    while True:

        reloj.tick(60)

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
        

       

        player.draw(screen)
        

        if len(player.shootList)>0:
            for x in player.shootList:
                x.draw(screen)
                x.trayectory()

                if x.rect.top < -10:
                    player.shootList.remove(x)
                else:
                    for enemy in enemyList:
                        if x.rect.colliderect(enemy.rect):
                            enemyList.remove(enemy)
                            player.shootList.remove(x)


        if len(enemyList) > 0:
            for enemy in enemyList:
                enemy.behavior(tiempo)
                enemy.draw(screen)

                if enemy.rect.colliderect(player.rect):
                    player.destruct()
                    inGame == False
                    stopEverything()
                if len(enemy.shootList)>0:
                    for x in enemy.shootList:
                        x.draw(screen)
                        x.trayectory()
                        if x.rect.colliderect(player.rect):
                            
                            inGame = False
                            stopEverything()
                        if x.rect.top > 900:
                            enemy.shootList.remove(x)
                        else:
                            for shoot in player.shootList:
                                if x.rect.colliderect(shoot.rect):
                                    player.shootList.remove(shoot)
                                    enemy.shootList.remove(x)



        if inGame == False:
            pygame.mixer.music.fadeout(3000)
            screen.blit(Text,(300,300))
        pygame.display.update()

SpaceInvader()