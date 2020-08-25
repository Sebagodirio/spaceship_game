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



    def shoot(self):
        print("Disparo")

    def draw(self,superfice):
        superfice.blit(self.ImageSpaceship,self.rect)

    def movement(self):
        if self.Life == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > 870:
                self.rect.right = 840

def SpaceInvader():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Space Invader")

    background = pygame.image.load("images/fondo.jpg")
    player = spaceship()

    inGame = True
    while True:

        player.movement()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if inGame == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        player.rect.left -= player.velocity
                    elif event.key == K_RIGHT:
                        player.rect.right += player.velocity
                    elif event.key == K_SPACE:
                         player.shoot()
        screen.blit(background,(0,0))
        player.draw(screen)
        pygame.display.update()

SpaceInvader()