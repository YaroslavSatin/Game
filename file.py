from pygame import *
import pygame
from random import randint
from time import *
global game
game = 'menu'

font.init()
font = font.SysFont('Aral',20)



def menu():
    global game
    global wX
    global wY
    wX = 620 
    wY = 480
    button = 'left'

    window = display.set_mode((wX, wY))
    display.set_caption('SpaceShooter')

    mixer.init()
    mixer.music.load('space.ogg')
    #mixer.music.play()

    background = transform.scale(image.load('galaxy.jpg'), (wX, wY))
    buttonL1 = transform.scale(image.load('buttonL1.png'), (250, 120))
    buttonL2 = transform.scale(image.load('buttonL2.png'), (250, 120))
    buttonL1LH = transform.scale(image.load('buttonL1LH.png'), (250, 120))
    buttonL2LH = transform.scale(image.load('buttonL2LH.png'), (250, 120))

    clock = pygame.time.Clock()
    FPS = 60


    while game == 'menu':
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game = 'exit'
            if e.type == KEYDOWN:
                if e.key == K_LEFT:
                    button = 'left'
                    
            if e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    button = 'right'
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    game = 'exit'

            if button == 'right':
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        game = 'level2'


            if button == 'left':
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        game = 'level1'

        window.blit(background,(0,0))

        if button == 'right':
            window.blit(buttonL1,(50,50))
            window.blit(buttonL2LH,(300,50))
        
        if button == 'left':
            window.blit(buttonL2,(300,50))
            window.blit(buttonL1LH,(50,50))
        


        clock.tick(FPS)
        display.update()
def level1():
    global wX
    global wY
    global game
    global bull_minigan
    global scoreGO 
    global scoreW 
    global health
    global DW
    
    wX = 620 
    wY = 480
    xxx = 0
    window = display.set_mode((wX, wY))
    display.set_caption('level1')

    mixer.init()
    mixer.music.load('space.ogg')
    #mixer.music.play()

    background = transform.scale(
        image.load('galaxy.jpg'), (wX, wY)
    )

    bulletSound = mixer.Sound('fire.ogg')
    lazer = mixer.Sound('lazer.ogg')




    clock = pygame.time.Clock()
    FPS = 60
    game = 'level1'
    bull_minigan = 0
    leftMove = False
    rightMove = False
    shotTime = 0
    scoreGO = 0
    scoreW = 0
    DW = 'L'
    health = 3


    class GameSprite(sprite.Sprite):
        
        def __init__ (self, picture, x, y, hight, wight, speed):
            super().__init__ ()
            self.speed = speed
            self.hight = hight
            self.wight = wight
            self.image =  transform.scale(image.load(picture), (hight, wight))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        
        def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))
        
        def colliderect(self, rect):
            return self.rect.colliderect(rect)

    
    class Player(GameSprite):
        
        def update(self):
            global bull_minigan
            keys = key.get_pressed()
            leftMove = False
            rightMove = False
            if keys[K_a] and self.rect.x > 0:
                leftMove = True

            else:
                leftMove = False


            if keys[K_d] and self.rect.x < (wX - self.hight):
                rightMove = True

            else:
                rightMove = False

            if leftMove == True:
                self.rect.x -= self.speed
            if rightMove == True:
                self.rect.x += self.speed

            if bull_minigan > 0:
                if keys[K_m]:
                    #bulletSound.play()
                    player1.fire()
                    bull_minigan -= 1
                else:
                    pass

        def fire(self):
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 10, 10)
            bullets.add(bullet)
        
        def fire2(self):
            bullet2 = Bullet('bullet2.png', self.rect.centerx, self.rect.top, 15, 30, 10)
            bullets2.add(bullet2)



    class Enemy(GameSprite):

        def update(self):
            global wY
            global wX
            global health
            global scoreGO
            self.rect.y += self.speed
            if self.rect.y > wY:
                self.speed = randint(1, 3)
                self.rect.x = randint(100, wX-100)
                self.rect.y = -40
                scoreGO += 1
                health -= 1
            


    class EnemyM(GameSprite):
        
        def __init__ (self, picture, x, y, hight, wight, speed, healthM):
            super().__init__ (picture, x, y, hight, wight, speed)
            self.healthM = healthM

        def update(self):
            global wX
            global wY
            global DW
            global bullet
            if self.rect.y < 0:
                self.rect.y += self.speed
            if self.rect.y >= 0:
                rspedM = randint(7, 17)
                if DW == 'L':
                    self.rect.x -= rspedM
                if DW == 'R':
                    self.rect.x += rspedM

                if self.rect.x <= 0:
                    DW = 'R'
                if self.rect.x >= wX - 200:
                    DW = 'L'
            if self.healthM <= 0:
                self.kill()
            
            

        def fireM(self):
            yB = self.rect.bottom - 75
            bulletM = Bullet2('bullet2.png', self.rect.centerx, yB, 10, 60, 20)
            bulletsM.add(bulletM)
            
            


    class Bullet(GameSprite):
        def update(self):
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.kill()
            
    class Bullet2(GameSprite):
        def update(self):
            self.rect.y += self.speed
            if self.rect.y  > 480:
                self.kill()

             



    #    x   = Class(picture, x, y, hight, wight, speed)
    player1 = Player('rocket.png', 20, 400, 35, 70, 6)
    health1 = GameSprite('rocket.png', 20, 75, 17, 35, 5)
    health2 = GameSprite('rocket.png', 40, 75, 17, 35, 5)
    health3 = GameSprite('rocket.png', 60, 75, 17, 35, 5)
    monsterM = EnemyM('monster.png', 200, -250, 200, 200, 4, 150)

    bullets = sprite.Group()
    bullets2 = sprite.Group()
    bulletsM = sprite.Group()
    enemys = sprite.Group()
    for x in range(6):
        xK = randint(100, wX-100)
        SpeedE = randint(1, 3)
        ufo = Enemy('ufo.png', xK, -40, 70, 35, SpeedE)
        enemys.add(ufo)
    logg = False
    logg2 = False
    skvozShot = False
    finish = False
    stop = False
    PX = 0



    while game == 'level1':
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game = 'menu'
            if e.type == KEYDOWN:
                if e.key == K_v:
                    
                    if skvozShot == False:
                        player1.fire()
                        #bulletSound.play()
                    if skvozShot == True:
                        lazer.play()
                        player1.fire2()


                        
                        

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    game = 'menu'

        
        window.blit(background,(0,0))


        scoreG = font.render('Пропущено кораблей:' + str(scoreGO), 1, (255, 255, 255))
        window.blit(scoreG,(20, 20))
        scoreWin = font.render('Уничтожено кораблей:' + str(scoreW), 1, (255, 255, 255))
        window.blit(scoreWin,(20, 42))
        scoreBul = font.render('Патроны для минигана ' + str(bull_minigan) + 'шт.', 1, (255, 255, 255))
        window.blit(scoreBul,(20, 64))

        if scoreW >= 400:
            finish = True
            stop = True

        player1.reset()
        enemys.draw(window)
        bullets.draw(window)
        bullets2.draw(window)
        bulletsM.draw(window)
        
        
        if scoreW >= 10:
            
            for en in listEnemys:
                en.kill()

            if monsterM.healthM > 0:
                monsterM.update()
                monsterM.reset()
            
                if xxx == 20:
                    lazer.play()
                    monsterM.fireM()
                    xxx = 0
                if monsterM.rect.y >= 0:
                    xxx += 1
            else:
                finish = True

            for bull in listBullet:
                if monsterM.rect.colliderect(bull):
                    bull.kill()
                    monsterM.healthM -= 1
                    
            for bull in listBulletM:
                if player1.rect.colliderect(bull):
                    bull.kill()
                    health -= 1

            
                
            
        else:
            enemys.update()

        if stop == False:
            bullets2.update()
            bullets.update()  
            player1.update()
            bulletsM.update() 
            


        if finish == True:
            win = font.render('YOU WIN', 1, (0, 255, 0))
            window.blit(win,(300, 200))
            PX += 1
            if PX == 180:
                game = 'menu'

        if health == 3:
            health1.reset()
            health2.reset()
            health3.reset()
        elif health == 2:
            health1.reset()
            health2.reset()
        elif health == 1:
            health1.reset()
        elif health <= 0:
            
            GO = font.render('GAME OVER', 1, (255, 0, 0))
            window.blit(GO,(300, 200))
            PX += 1
            stop = True
            if PX == 180:
                game = 'menu'

        listEnemys = enemys.sprites()
        listBullet = bullets.sprites()
        listBulletM = bulletsM.sprites()
        listBullet2 = bullets2.sprites()
        for en in listEnemys:
            for bull in listBullet:
                if en.rect.colliderect(bull):
                    rando = randint(1,20)
                    if logg == False:
                        if rando == 20:
                            puzyr1 = GameSprite('puzyr.png', en.rect.x, en.rect.y, 35, 35, 6)
                            logg = True
                        if rando == 19:
                            puzyr2 = GameSprite('puzyr2.png', en.rect.x, en.rect.y, 35, 35, 6)
                            logg2 = True
                    en.rect.x = randint(100, wX-100)
                    en.rect.y = -40
                    if skvozShot == False:
                        bull.kill()
                    scoreW += 1

        for en2 in listEnemys:
            for bull2 in listBullet2:
                if en2.rect.colliderect(bull2):
                    rando = randint(1,20)
                    if logg == False:
                        if rando == 20:
                            puzyr1 = GameSprite('puzyr.png', en2.rect.x, en2.rect.y, 35, 35, 6)
                            logg = True
                        if rando == 19:
                            puzyr2 = GameSprite('puzyr2.png', en2.rect.x, en2.rect.y, 35, 35, 6)
                            logg2 = True
                    en2.rect.x = randint(100, wX-100)
                    en2.rect.y = -40
                    scoreW += 1
        
        
        if logg == True:
            puzyr1.reset()
            puzyr1.rect.y += puzyr1.speed
            if puzyr1.rect.colliderect(player1):
                puzyr1.kill()
                logg = False
                bull_minigan += 30
            if puzyr1.rect.y > wY:
                puzyr1.kill()
                logg = False

        if logg2 == True:
            puzyr2.reset()
            puzyr2.rect.y += puzyr2.speed
            if puzyr2.rect.colliderect(player1):
                puzyr2.kill()
                logg2 = False
                skvozShot = True
                shotTime += 180

            if puzyr2.rect.y > wY:
                puzyr2.kill()
                logg2 = False

        if skvozShot == True:
            if shotTime > 0:
                shotTime -= 1
            if shotTime == 0:
                skvozShot = False
        
        


        clock.tick(FPS)
        display.update()
def level2():
    global wX
    global wY
    global game
    global bull_minigan
    global scoreGO 
    global scoreW 
    global health
    wX = 620 
    wY = 480

    window = display.set_mode((wX, wY))
    display.set_caption('level2')

    mixer.init()
    mixer.music.load('space.ogg')
    #mixer.music.play()

    background = transform.scale(
        image.load('galaxy.jpg'), (wX, wY)
    )







    clock = pygame.time.Clock()
    FPS = 60
    game = 'level1'
    bull_minigan = 0
    leftMove = False
    rightMove = False
    bulletSound = mixer.Sound('fire.ogg')
    bullets = sprite.Group()
    bullets2 = sprite.Group()
    scoreGO = 0
    scoreW = 0
    health = 3

    class GameSprite(sprite.Sprite):
        
        def __init__ (self, picture, x, y, hight, wight, speed):
            super().__init__ ()
            self.speed = speed
            self.hight = hight
            self.wight = wight
            self.image =  transform.scale(image.load(picture), (hight, wight))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        
        def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))
        
        def colliderect(self, rect):
            return self.rect.colliderect(rect)

    
    class Player(GameSprite):
        
        def update(self):
            global bull_minigan
            keys = key.get_pressed()
            leftMove = False
            rightMove = False
            if keys[K_a] and self.rect.x > 0:
                leftMove = True

            else:
                leftMove = False


            if keys[K_d] and self.rect.x < (wX - self.hight):
                rightMove = True

            else:
                rightMove = False

            if leftMove == True:
                self.rect.x -= self.speed
            if rightMove == True:
                self.rect.x += self.speed

            if bull_minigan > 0:
                if keys[K_m]:
                    #bulletSound.play()
                    player1.fire()
                    bull_minigan -= 1
                else:
                    pass

        def fire(self):
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 10, 10)
            bullets.add(bullet)
        
        def fire2(self):
            bullet2 = Bullet('bullet2.png', self.rect.centerx, self.rect.top, 15, 30, 10)
            bullets2.add(bullet2)



    class Enemy(GameSprite):
        def __init__ (self, picture, x, y, hight, wight, speed, healthE):
            super().__init__ (picture, x, y, hight, wight, speed)
            self.healthE = healthE
            
        def update(self):
            global wY
            global wX
            global health
            global scoreGO
            global scoreW
            self.rect.y += self.speed
            if self.rect.y > wY:
                self.speed = randint(1, 3)
                self.rect.x = randint(100, wX-100)
                self.rect.y = -40
                scoreGO += 1
                health -= 1

            if self.healthE <= 0:
                self.healthE = 2
                scoreW += 1
                self.speed = randint(1, 3)
                self.rect.x = randint(100, wX-100)
                self.rect.y = -40

    class Bullet(GameSprite):
        def update(self):
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.kill()

            
                



    #    x   = Class(picture, x, y, hight, wight, speed)
    player1 = Player('rocket.png', 20, 400, 35, 70, 6)
    health1 = GameSprite('rocket.png', 20, 75, 17, 35, 5)
    health2 = GameSprite('rocket.png', 40, 75, 17, 35, 5)
    health3 = GameSprite('rocket.png', 60, 75, 17, 35, 5)

    monsterM = Player('monster.png', 200, 100, 250, 250, 6)

    enemys = sprite.Group()
    for x in range(6):
        xK = randint(100, wX-100)
        SpeedE = randint(1, 3)
        ufo = Enemy('ufo.png', xK, -40, 70, 35, SpeedE, 2)
        enemys.add(ufo)  

    logg = False
    logg2 = False
    skvozShot = False
    finish = False
    stop = False
    PX = 0


    while game == 'level1':
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game = 'menu'
            if e.type == KEYDOWN:
                if e.key == K_v:
                    #bulletSound.play()
                    if skvozShot == False:
                        player1.fire()
                    if skvozShot == True:
                        player1.fire2()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    game = 'menu'

        
        window.blit(background,(0,0))


        scoreG = font.render('Пропущено кораблей:' + str(scoreGO), 1, (255, 255, 255))
        window.blit(scoreG,(20, 20))
        scoreWin = font.render('Уничтожено кораблей:' + str(scoreW), 1, (255, 255, 255))
        window.blit(scoreWin,(20, 42))
        scoreBul = font.render('Патроны для минигана ' + str(bull_minigan) + 'шт.', 1, (255, 255, 255))
        window.blit(scoreBul,(20, 64))

        if scoreW >= 40:
            finish = True
            stop = True
        
        player1.reset()
        enemys.draw(window)
        bullets.draw(window)
        bullets2.draw(window)
        listEnemys = enemys.sprites()
        listBullet = bullets.sprites()
        listBullet2 = bullets2.sprites()


        if stop == False:
            bullets2.update()
            bullets.update()  
            player1.update()
            enemys.update()

            for en in listEnemys:
                for bull in listBullet:
                    if en.rect.colliderect(bull):
                        en.healthE -= 1
                        rando = randint(1,20)
                        if logg == False:
                            if rando == 20:
                                puzyr1 = GameSprite('puzyr.png', en.rect.x, en.rect.y, 35, 35, 6)
                                logg = True
                            if rando == 19:
                                puzyr2 = GameSprite('puzyr2.png', en.rect.x, en.rect.y, 35, 35, 6)
                                logg2 = True
                        if skvozShot == False:
                            bull.kill()
                            
            for en2 in listEnemys:
                for bull2 in listBullet2:
                    if en2.rect.colliderect(bull2):
                        en2.healthE -= 1
                        rando = randint(1,20)
                        if logg == False:
                            if rando == 20:
                                puzyr1 = GameSprite('puzyr.png', en2.rect.x, en2.rect.y, 35, 35, 6)
                                logg = True
                            if rando == 19:
                                puzyr2 = GameSprite('puzyr2.png', en2.rect.x, en2.rect.y, 35, 35, 6)
                                logg2 = True
                    

            if logg == True:
                puzyr1.reset()
                puzyr1.rect.y += puzyr1.speed
                if puzyr1.rect.colliderect(player1):
                    puzyr1.kill()
                    logg = False
                    bull_minigan += 30
                if puzyr1.rect.y > wY:
                    puzyr1.kill()
                    logg = False

            if logg2 == True:
                puzyr2.reset()
                puzyr2.rect.y += puzyr2.speed
                if puzyr2.rect.colliderect(player1):
                    puzyr2.kill()
                    logg2 = False
                    skvozShot = True

                if puzyr2.rect.y > wY:
                    puzyr2.kill()
                    logg2 = False
                



        if finish == True:
            win = font.render('YOU WIN', 1, (0, 255, 0))
            window.blit(win,(300, 200))

        if health == 3:
            health1.reset()
            health2.reset()
            health3.reset()
        elif health == 2:
            health1.reset()
            health2.reset()
        elif health == 1:
            health1.reset()
        elif health <= 0:
            GO = font.render('GAME OVER', 1, (255, 0, 0))
            window.blit(GO,(300, 200))
            PX += 1
            stop = True
            if PX == 180:
                game = 'menu'



        

        
        





        clock.tick(FPS)
        display.update()

while game != 'exit':
    if game == 'menu':
        menu()

    if game == 'level1':
        level1()

    if game == 'level2':
        level2()

