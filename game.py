import pygame,sys
from random import *
from pygame.locals import *
import time

pygame.init()

wall_l = 0
wall_r = 800
wall_u = 0
wall_d = 640
life = 2
stop_watch=False
stop_watch_start=None
prop_num=0

prop_old_time=None

weight=False
weight_start=None

pig_days=1

#create a new screen
screen=pygame.display.set_caption("Crazy Piggy")
screen = pygame.display.set_mode((800,640),0,32)

#load the pictures that will be needed
start_logo1= pygame.image.load('CrazyPiggy1.png').convert_alpha()
start_logo2= pygame.image.load('CrazyPiggy2.png').convert_alpha()
start_logo3= pygame.image.load('CrazyPiggy3.png').convert_alpha()
start_logo4= pygame.image.load('CrazyPiggy4.png').convert_alpha()
death_logo= pygame.image.load('GameOver.png').convert_alpha()
pig1 = pygame.image.load('pig1.png').convert_alpha()
pig2 = pygame.image.load('pig2.png').convert_alpha()
pig3 = pygame.image.load('pig3.png').convert_alpha()
pig4 = pygame.image.load('pig4.png').convert_alpha()
pig5 = pygame.image.load('pig5.png').convert_alpha()
pig6 = pygame.image.load('pig6.png').convert_alpha()
pig7 = pygame.image.load('pig7.png').convert_alpha()
life1 = pygame.image.load('life1.png').convert_alpha()
life2 = pygame.image.load('life2.png').convert_alpha()
life3 = pygame.image.load('life3.png').convert_alpha()
direction = pygame.image.load('direction.png')
background = pygame.image.load('map.png')
pig_image = [pig1,pig2,pig3,pig4,pig5,pig6,pig7]
propspic = ["clock","medicine","sweet","fire","heart","weight"]

#create a pig class
class Pig(pygame.sprite.Sprite):
    def __init__(self,pig_type,location,speed):
        pygame.sprite.Sprite.__init__(self)
        self.type = pig_type
        self.image=pig_image[self.type-1]
        self.rect=self.image.get_rect()
        self.rect.topleft=location
        self.speed=speed

    #define a function that makes the pigs move randomly    
    def move(self):
        #object of Rect, move(offsetx,offsety)
        self.rect=self.rect.move(self.speed[0],self.speed[1])
        
        if self.rect.bottom>635:
            self.rect.top=5
        if self.rect.right>785:
            self.rect.left=5
        if self.rect.left<5:
            self.rect.right=785
        if self.rect.top<5:
            self.rect.bottom=635

#create a prop class
class Prop(pygame.sprite.Sprite):
    def __init__(self,prop_type,prolo):
        pygame.sprite.Sprite.__init__(self)
        if prop_type == "fire":
            filename = "fire.png"
        elif prop_type == "clock":
            filename = "clock.png"
        elif prop_type == "sweet":
            filename = "sweet.png"
        elif prop_type == "medicine":
            filename = "medicine.png"
        elif prop_type == "heart":
            filename = "heart.png"
        elif prop_type=="weight":
            filename = "weight.png"
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = prolo
        self.type=prop_type
        
#create a piggy class.Piggy is the picture which you control with.
class Piggy(pygame.sprite.Sprite):        
    def __init__ (self,piggy_type,speed,location):
        pygame.sprite.Sprite.__init__(self)
        self.type = piggy_type 
        self.image = pig_image[self.type-1]         
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = location
        self.speed = speed
        
    #change the type
    def inflate(self):
        self.image = pig_image[self.type-1]
        #also need to update the rect
        left = self.rect.left
        top = self.rect.top
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = left,top

    #restart
    def restart(self):
        self.type = 1
        self.image = pig_image[self.type-1]
        left = 400
        top = 320
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = left,top
        
    #start again
    def again(self):
        if self.type == 7:
            global pig_days
            pig_days+=1  #new day
            self.type = 1
            self.image = pig_image[self.type-1]
            #also need to update the rect
            left = self.rect.left
            top = self.rect.top
            self.rect = self.image.get_rect()
            self.rect.left,self.rect.top = left,top

    def death(self):
        if self.type <= 1:
            self.type = 1
            global life
            life -= 1

#collide check
def update_pig(piggy, piggroup):
    collided_pig = pygame.sprite.spritecollide(piggy,piggroup,True)
    #check if there is a collision
    if len(collided_pig)!=0:
        #check if the piggy collides with a pig with a smaller type or not
        if collided_pig[0].type<=piggy.type:
            piggy.type+=1
            piggy.inflate()
            #add the collided pig to the group again
            location = [choice(range(5,320)) , choice(range(5,240))]
            speed = [choice([-3, 3]), choice([-3, 3])]
            pig_type = collided_pig[0].type
            pig=Pig(pig_type,location,speed)
            piggroup.add(pig)
            piggy.again()

        #if not, reduce the life, and change the type of the piggy to 1            
        else:
            global life
            life -= 1
            piggy.restart()
            #add the removed pig to the group
            piggroup.add(collided_pig[0])
       
        
def update_prop(piggy, propgroup):
    cur_type=None
    cur_prop=propgroup.sprites()
    if cur_prop:
        cur_type=cur_prop[0].type
        
    collided_prop = pygame.sprite.spritecollide(piggy,propgroup,True)
    #piggy is the current pig
    #propgroup is the prop


    if len(collided_prop)!=0:
        if cur_type=="medicine":
            if piggy.type >2:
                piggy.type -= 2
            else :
                piggy.type = 1
                
        elif cur_type == "fire":
            global life
            life -= 1
            
        elif cur_type == "clock":
            global stop_watch,stop_watch_start
            stop_watch=True
            stop_watch_start=time.time()
            
        elif cur_type == "sweet":
            piggy.type+=2
            if piggy.type>=7:
                global pig_days
                pig_days+=1
                piggy.type=1
       
        elif cur_type == "heart":
            life+=1
            
        elif cur_type =="weight":
            global weight,weight_start
            weight=True
            weight_start=time.time()
                
        piggy.inflate()
        global prop_num
        prop_num=0

def backgrounddraw():
    screen.blit(background,(0,0))

def terminate():
   pygame.quit()
   sys.exit()

#define the game
def game(running):
    #init 
    global life,stop_watch,stop_watch_start,prop_num,prop_old_time,weight_start,weight,pig_days
    life =2
    stop_watch=False
    stop_watch_start=None
    prop_num=0
    prop_old_time=None
    weight=False
    weight_start=None
    pig_days=1

    screen.fill((255,255,255))
    piggy = Piggy(1,[0,0],[400,320])
    prolo = [randint(200,640) , randint(100,480)]
    ppic = propspic[randint(0,5)]
    prop_type = ppic
    propgroup = pygame.sprite.Group()
    propgroup.add(Prop(prop_type,prolo))
    prop_num = 1
    piggroup = pygame.sprite.Group()
    key_event = None

    #initially, you must create at least one pig that is of the same or
    #smaller type with the piggy
    location = [choice(range(0,800)) , choice(range(0,640))]
    speed = [choice([-3, 3]), choice([-3, 3])]
    pig_type = 1             
    pig=Pig(pig_type,location,speed)
    piggroup.add(pig)

    #create the other four pigs
    for row in range(0, 4):
        location = [choice(range(0,800)) , choice(range(0,640))]
        speed = [choice([-3, 3]), choice([-3, 3])]
        pig_type = randrange(1,7)
        pig=Pig(pig_type,location,speed)
        piggroup.add(pig)
       
    #global prop_old_time
    prop_old_time=time.time()

    point_font=pygame.font.Font("KirstyBold.ttf",40)

    start_time=time.time()
        
    while running:
        # for each loop, test if life is 0 first
        # if not, continue game
        # otherwise, stop the game
        if life <= 0:
            break              
        else:
            backgrounddraw()
            if life >= 3:
                life = 3
                screen.blit(life3,(0, 0))            
            if life == 2:
                screen.blit(life2,(0, 0))
            elif life == 1:
                screen.blit(life1,(0, 0))

            #this function will draw all the pigs in piggroup
            piggroup.draw(screen)

            #the fuction of prop
         
            if not stop_watch:
                for pig in piggroup:
                    pig.move()
                    
            cur_time=time.time()
            
            if stop_watch_start and (cur_time-stop_watch_start)>5:#5s
                    stop_watch=False
                    stop_watch_start=None
            if (cur_time-prop_old_time)>10:
                prop_old_time=cur_time
                propgroup.empty()
                prop_num=0
                prolo = [randint(200,640) , randint(100,480)]
                ppic = propspic[randint(0,4)]
                prop_type = ppic
                propgroup = pygame.sprite.Group()
                propgroup.add(Prop(prop_type,prolo))
                prop_num=1
                          
            propgroup.draw(screen)
            update_pig(piggy,piggroup)
            update_prop(piggy,propgroup)

            #control piggy to move
            for event in pygame.event.get():
                if event.type==QUIT:
                    terminate()
                if event.type==KEYDOWN:
                    if event.key==K_LEFT:
                        piggy.speed[0] = -10
                                              
                    elif event.key==K_RIGHT:
                        piggy.speed[0] = 10
                                   
                    elif event.key==K_UP:
                        piggy.speed[1] = -10
                                               
                    elif event.key==K_DOWN:
                        piggy.speed[1] = 10
                    
                if event.type==KEYUP:
                    piggy.speed[0] = 0
                    piggy.speed[1] = 0
                    
            #test if the piggy hit the boundaries
            #if so, then test if the user wants to move the piggy
            #away from the boundary
            #if not, then set the corresponding speed to 0
                    
            if piggy.rect.left < wall_l:
                if event.key==K_RIGHT:
                    piggy.speed[0]= 10
                else:
                    piggy.speed[0] = 0
            if piggy.rect.right > wall_r:
                if event.key == K_LEFT:
                    piggy.speed[0]= -10
                else:
                    piggy.speed[0] = 0
            if piggy.rect.top < wall_u:
                if event.key == K_DOWN:
                    piggy.speed[1]= 10
                else:
                    piggy.speed[1] = 0
            if piggy.rect.bottom > wall_d:
                if event.key == K_UP:
                    piggy.speed[1]= -10
                else:
                    piggy.speed[1] = 0

            if weight:
                piggy.rect.left += piggy.speed[0]*0.2
                piggy.rect.top += piggy.speed[1]*0.2
            else:
                piggy.rect.left += piggy.speed[0]
                piggy.rect.top += piggy.speed[1]
            if weight_start and (cur_time-weight_start)>5:# over than 5s
                weight=False
                weight_start=None
         
            point_word=point_font.render(str("Days:%d"%pig_days),True,(100,200,100))
            screen.blit(point_word,(620,550))
    
            pygame.time.delay (20)
            screen.blit(piggy.image, piggy.rect)

        pygame.display.update()
        
  
#define the main
def main1():
    counter = 1
    g = 1
    yspeed = 0
    yspeed2 = 0
    yspeed3 = 0
    yspeed4 = 0
    y = -150
    y2 = -150
    y3 = -150
    y4 = -150
    running = True
    begin0 = True
    
    while running:        
        #how to quit
        for event in pygame.event.get():
                if event.type==QUIT:
                    terminate()                    

        yspeed += g
        counter += 1
        if counter < 400:
            if y < 200 and counter < 100:
                y += yspeed
            elif counter < 100:
                yspeed = -0.7*yspeed
                y += yspeed
            elif counter > 100 and counter < 300:
                yspeed = 0
            elif counter > 300 :
                yspeed = -10
                y += yspeed
            screen.fill((241,242,197))
            screen.blit(start_logo1,(150, y))

        if counter > 400 :
            yspeed2 += g
            if y2 < 200 and counter < 500:
                y2 += yspeed2
            elif counter < 500:
                yspeed2 = -0.7*yspeed2
                y2 += yspeed2
            elif counter > 500 and counter < 700:
                yspeed2 = 0
            elif counter > 700 :
                yspeed2 = -20
                y2 += yspeed2
            screen.fill((241,242,197))
            screen.blit(start_logo2,(170, y2))
        
        if counter > 800 :
            yspeed3 += g
            if y3 < 200 and counter < 900:
                y3 += yspeed3
            elif counter < 900:
                yspeed3 = -0.7*yspeed3
                y3 += yspeed3
            elif counter > 900 and counter < 1100:
                yspeed3 = 0
            elif counter > 1100 :
                yspeed3 = -20
                y3 += yspeed3
            screen.fill((241,242,197))
            screen.blit(start_logo3,(130, y3))
            
        if counter > 1200 :
            yspeed4 += g
            if y4 < 200 and counter < 1300:
                y4 += yspeed4
            elif counter < 1300:
                yspeed4 = -0.7*yspeed4
                y4 += yspeed4
            elif counter > 1300 and counter < 1500:
                yspeed4 = 0
            elif counter > 1500 :
                yspeed4 = -20
                y4 += yspeed4
            screen.fill((241,242,197))
            screen.blit(start_logo4,(120, y4))
            pygame.display.update()

        if counter > 1600:
            screen.fill((241,242,197))
            screen.blit(direction,(150, 50))
            pygame.display.update()
            while begin0:
                for event in pygame.event.get():
                    if event.type==QUIT:
                        terminate()
                    if event.type==KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            begin0=False
            main2()

        pygame.display.update()

def main2():
    running = True
    begin1 = True

    #the game start
    pygame.mixer.init()
    pygame.mixer.music.load("game.mp3")
    pygame.mixer.music.play(-1,0)
 
    game(running)

    counter2 = 1
    g2 = 1
    yspeed5 = 0
    yspeed6 = 0
    y5 = -150
    y6 = -150
    running2 = True
    
    #game over
    pygame.mixer.music.stop()
    pygame.mixer.init()
    pygame.mixer.music.load("gameover.mp3")
    pygame.mixer.music.play()
    
    while running2:
        #how to quit
        for event in pygame.event.get():
                if event.type==QUIT:
                    terminate()

        yspeed5 += g2
        counter2 += 1
        
        if counter2 < 600:
            if y5 < 200 and counter2 < 100:
                y5 += yspeed5
            elif counter2 < 100:
                yspeed5 = -0.7*yspeed5
                y5 += yspeed5
            elif counter2 > 100 :
                yspeed5 = 0
            screen.fill((241,242,197))
            screen.blit(death_logo,(220, y5))

        if counter2 > 100 :
            while begin1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        terminate()
                    if event.type==KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            begin1 = False
            #restart
            main2()
            
        pygame.display.update()

    pygame.quit()

main1()
