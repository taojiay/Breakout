# Rachel, Rumsha Khan, Jiayi Tao

# Extended Feature 1: New Brick Arrangements
# Extended Feature 2: Three game themes
# Extended Feature 3: Sound Effect and Background Music

#BUGS
#When ball hits the side it sometimes goes straight down
#When typing initials, capital A shows up as lowercase-changed unicode values for checking in getmod
#Not able to press 1,2,or 3 to continue during gameover screen-fixed moved outside while loop and added additional boolean

import pygame,sys,random,math
from Highscoremodule import highscore
from Highscoremodule import top10

# colors 
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)


x = 580
y = 500



class brick(pygame.sprite.Sprite):
    def __init__(self,theme,x,y):
        super().__init__()
        self.theme = theme
        self.image = pygame.image.load("{0}brick{1}.png".format(self.theme,random.randint(1,4)))
        self.image = pygame.transform.scale(self.image,(50,30))
        self.rect = self.image.get_rect()
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.rect.x = x
        self.rect.y = y

class paddle(pygame.sprite.Sprite):
    def __init__(self,theme):
        super().__init__()
        self.theme = theme
        self.image = pygame.image.load("{0}paddle.png".format(self.theme))
        self.image = pygame.transform.scale(self.image,(90,15))
        self.rect = self.image.get_rect()
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]

        
        # initial position of paddle
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = self.screenwidth/2
        self.rect.y = self.screenheight - (self.height*4)

    #positioning of mouse for paddle
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.right > self.screenwidth:
            self.rect.right = self.screenwidth
        elif self. rect.left < 0:
            self.rect.left = 0
    
    def reset(self):
        self.rect.x = self.screenwidth/2
        self.rect.y = self.screenheight - (self.height*4)


class ball(pygame.sprite.Sprite):
    def __init__(self,theme):
        super().__init__()
        self.theme = theme
        self.screenwidth = pygame.display.get_surface().get_width()
        self.image = pygame.image.load("{0}ball.png".format(self.theme))
        self.image = pygame.transform.scale(self.image,(20,20))
        self.rect = self.image.get_rect()
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.topedge = 295
        self.bottomedge = 305
        self.leftedge = 10
        self.rightedge = self.screenwidth-10
        self.rect.x = random.randint(self.leftedge,self.rightedge)
        self.rect.y = random.randint(self.topedge,self.bottomedge)
        self.dx = random.randrange(-3,4,6)
        self.dy = 3
        self.angle = random.randrange(15,46)
    
    def update(self):
        radians = math.radians(self.angle)
        self.rect.x += float(self.dx * math.sin(radians))
        self.rect.y += float(self.dy * math.cos(radians))

    def reset(self):
        self.rect.x = random.randint(self.leftedge,self.rightedge)
        self.rect.y = random.randint(self.topedge,self.bottomedge)
        self.dx = random.randrange(-3,4,6)
        self.dy = 3
        self.angle = random.randrange(15,46)
   
    def hitpaddle(self,position):
        self.dy = -self.dy
        if self.dx > 0 and position > 0 and self.rect.x > 50:
            self.dx = -self.dx
        elif self.dx < 0 and position < 0 and self.rect.x < 750:
            self.dx = -self.dx

    def hitbrick(self):
        self.dy = -self.dy

# running the game
class game:
    def __init__(self):
        self.running = False
        self.screenwidth = 800 # window size
        self.screenheight = 500 
        self.screen = pygame.display.set_mode((self.screenwidth,self.screenheight)) 
        self.caption = pygame.display.set_caption("Breakout") # window caption
        self.mouse = pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()
        self.gamespeed = 60
        self.startingtime = 0
        self.seconds = 0

        self.score = 0
        self.level = 1
        self.life = 3
        self.pause = False
        self.highscores = False

        self.themelist = ["christmas","food","pets"]
        self.theme = self.themelist[random.randint(0,2)]
        
        # create sprites groups
        self.spritesgroup = pygame.sprite.Group()
        self.ballgroup = pygame.sprite.Group()
        self.brickgroup = pygame.sprite.Group()

        # create paddle
        self.paddle = paddle(self.theme)
        self.spritesgroup.add(self.paddle)

        # create ball
        self.ball = ball(self.theme)
        self.spritesgroup.add(self.ball)
        self.ballgroup.add(self.ball)
        
        # create bricks
        self.bricks = [brick(self.theme,0,0)]
        for row in range(0,2):
            for column in range(0,14):
                b = brick(self.theme,50 + self.bricks[-1].rect.width*column, 75 + self.bricks[-1].rect.height*row)
                #b.image.get_rect()
                self.spritesgroup.add(b)
                self.brickgroup.add(b)
                self.bricks.append(b)
        # add sound and background music
        self.crashsound = pygame.mixer.Sound("{0}brick.wav".format(self.theme))
        self.losealifesound = pygame.mixer.Sound("losealife.wav")
        self.levelupsound = pygame.mixer.Sound("levelup.wav")
        self.bgm = pygame.mixer.music.load("{0}bgm.wav".format(self.theme))

    
    def startscreen(self):
        startS = True
        breakout = pygame.image.load("breakout.png")
        breakout = pygame.transform.scale(breakout,(750,130))
        bigfont = pygame.font.Font("RepriseTitleStd.otf",35)
        smallfont = pygame.font.Font("RepriseTitleStd.otf",30)
        label0 = bigfont.render("Press a number key 1-3 to make a selection", 0, white)
        label1 = smallfont.render("1. Start",0,white)
        label2 = smallfont.render("2. View scores", 0, white)
        label3 = smallfont.render("3. Help / Instructions", 0, white)
        self.screen.fill(black)
        self.screen.blit(breakout,(25,75))
        self.screen.blit(label0,(90,260))
        self.screen.blit(label1,(350,320))
        self.screen.blit(label2,(300,360))
        self.screen.blit(label3,(250,400))
        pygame.display.flip()

        while startS == True:
            for event in pygame.event.get():
                #pressing 1 to start game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        startS = False
                        self.startingtime = pygame.time.get_ticks()
                        pygame.mixer.music.play(-1)
              
                #pressing 3 to see rules
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        breakout = pygame.transform.scale(breakout,(100,25))
                        bigfont = pygame.font.Font("RepriseTitleStd.otf",40)
                        smallfont = pygame.font.Font("ERASDEMI.TTF",25)
                        label0 = bigfont.render("Instructions",0,white)
                        label1 = smallfont.render("Move the mouse left and right to move paddle",0,white)
                        label2 = smallfont.render("Use ball to break bricks",0,white)
                        label3 = smallfont.render("Lose a life if the ball hits the bottom of the screen", 0, white)
                        label4 = smallfont.render("Reach the top of the screen to go to the next level",0,white)
                        label5 = smallfont.render("Try reaching the top ASAP",0,white)
                        label6 = smallfont.render("Less bricks broken and time consumed = Higher score",0,white)
                        label7 = smallfont.render("GOOD LUCK!",0,white)
                        label8 = smallfont.render("Press 1 to start",0,white)
                        label9 = smallfont.render("Press 2 to view scores",0,white)
                        self.screen.fill(black)
                        self.screen.blit(breakout,(675,450))
                        self.screen.blit(label0,(310,50))
                        self.screen.blit(label1,(50,110))
                        self.screen.blit(label2,(50,140))
                        self.screen.blit(label3,(50,170))
                        self.screen.blit(label4,(50,200))
                        self.screen.blit(label5,(50,260))
                        self.screen.blit(label6,(50,290))
                        self.screen.blit(label7,(50,320))
                        self.screen.blit(label8,(50,380))
                        self.screen.blit(label9,(50,410))
                        pygame.display.flip()

                #pressing 2 to view high scores
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        breakout = pygame.transform.scale(breakout,(100,25))
                        bigfont = pygame.font.Font("RepriseTitleStd.otf",40)
                        smallfont = pygame.font.Font("ERASDEMI.TTF",25)
                        label0 = bigfont.render("High Scores",0,white)
                        label1 = smallfont.render("Press 1 to start",0,white)
                        label2 = smallfont.render("Press 3 for help",0,white)
                        self.screen.fill(black)
                        self.screen.blit(breakout,(675,450))
                        self.screen.blit(label0,(300,50))
                        self.screen.blit(label1,(50,380))
                        self.screen.blit(label2,(50,410))
                        top10(self.screen, 'HighScores.txt')
                        pygame.display.flip()
                  
                        

    def run(self):
        if self.life == 3 and self.level == 1: 
            self.startscreen()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            if not self.pause:
                self.seconds = (pygame.time.get_ticks()-self.startingtime)//1000
            self.update()
            self.render()
            self.clock.tick(self.gamespeed)

    def reset(self):
        pygame.mixer.music.play(-1)
        self.startingtime = pygame.time.get_ticks()
        self.ball.reset()
        self.paddle.reset()
        self.spritesgroup.empty()
        self.spritesgroup.add(self.paddle)
        self.spritesgroup.add(self.ball)
        self.ballgroup.empty()
        self.ballgroup.add(self.ball)
        self.brickgroup.empty()
        
        #set new bricks arrangement 
        self.bricks = [brick(self.theme,0,0)]
        if self.level == 1: 
            for row in range(0,2):
                for column in range(0,14):
                    b = brick(self.theme,50 + self.bricks[-1].rect.width*column, 75 + self.bricks[-1].rect.height*row)
                    self.spritesgroup.add(b)
                    self.brickgroup.add(b)
                    self.bricks.append(b)

        elif self.level == 2:
            for row in range(0,5):
                for column in range(0,8):
                    if row % 2:
                        b = brick(self.theme,self.bricks[-1].rect.width*2*column, 50 + self.bricks[-1].rect.height*row)
                    else:
                        b = brick(self.theme,self.bricks[-1].rect.width + self.bricks[-1].rect.width*2*column, 50 + self.bricks[-1].rect.height*row)
                    self.spritesgroup.add(b)
                    self.brickgroup.add(b)
                    self.bricks.append(b)

        elif self.level == 3:
            for row in range(0,4):
                for column in range(0,16):
                    b = brick(self.theme,self.bricks[-1].rect.width*column, 50 + self.bricks[-1].rect.height*2*row)
                    self.spritesgroup.add(b)
                    self.brickgroup.add(b)
                    self.bricks.append(b)

        elif self.level == 4:
            for row in range(0,6):
                for column in range(0,8):
                    if row % 2:
                        b = brick(self.theme,self.bricks[-1].rect.width*column, 50 + self.bricks[-1].rect.height*row)
                    else:
                        b = brick(self.theme,400+self.bricks[-1].rect.width*column, 50 + self.bricks[-1].rect.height*row)
                    self.spritesgroup.add(b)
                    self.brickgroup.add(b)
                    self.bricks.append(b)

        elif self.level == 5: 
            for row in range(0,6):
                for column in range(0,15):
                    b = brick(self.theme,25 + self.bricks[-1].rect.width*column, 50 + self.bricks[-1].rect.height*row)
                    self.spritesgroup.add(b)
                    self.brickgroup.add(b)
                    self.bricks.append(b)

        else:
             for row in range(0,7):
                for column in range(0,16):
                    b = brick(self.theme,self.bricks[-1].rect.width*column, 30 + self.bricks[-1].rect.height*row)
                    self.spritesgroup.add(b)
                    self.brickgroup.add(b)
                    self.bricks.append(b)         

    def update(self):
        self.paddle.update()
        self.ball.update()

        # when ball hits the paddle
        if pygame.sprite.spritecollide(self.paddle,self.ballgroup,False):
            position = (self.paddle.rect.x + self.paddle.width/2) - (self.ball.rect.x + self.ball.width/2)
            self.ball.hitpaddle(position)

        # when ball hits the bricks
        brickamount1 = len(self.brickgroup)
        if pygame.sprite.spritecollide(self.ball,self.brickgroup,True):
            pygame.mixer.Sound.play(self.crashsound)
            self.ball.hitbrick() 
            brickamount2 = len(self.brickgroup)
            self.score -= 10*(brickamount1-brickamount2)
            brickamount1 = brickamount2

        # when ball hits the edges
        if self.ball.rect.right >= self.screenwidth:
            self.ball.dx = -self.ball.dx


        if self.ball.rect.left <= 0:
            self.ball.dx = -self.ball.dx     
        
        #when ball hits top
        if self.ball.rect.top <= 0:
            originalscore = self.score
            if self.seconds < 60:
                self.score += (12-(self.seconds//5))*100*self.level
            else:
                self.score += 50*self.level
            self.pause = True
            pygame.mixer.Sound.play(self.levelupsound)
            while self.pause == True:
                levelup = pygame.image.load("levelup.png")
                levelup = pygame.transform.scale(levelup,(200,150))
                breakout = pygame.image.load("breakout.png")
                breakout = pygame.transform.scale(breakout,(100,25))
                bigfont = pygame.font.Font("RepriseTitleStd.otf",35)
                smallfont = pygame.font.Font("ERASDEMI.TTF",20)
                time = bigfont.render("Time: {0:02}".format(self.seconds) + " s",0,white)
                bonus = self.score - originalscore
                bonus = bigfont.render("Bonus: + " +str(bonus),0,white)
                instruction = smallfont.render("Press 1 to continue.",0,white)
                self.screen.fill(black)
                self.screen.blit(levelup,(300,50))
                self.screen.blit(time,(300,250))
                self.screen.blit(bonus,(300,300))
                self.screen.blit(instruction,(300,350))
                self.screen.blit(breakout,(675,450))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.pause = False
                            self.level += 1
                            if self.level <= 7:
                                self.gamespeed += 10
                            self.reset()
                            self.ball.dy +=1
                            self.run
                            
        #when ball hits bottom
        if self.ball.rect.bottom >= self.screenheight:
            self.pause = True
            breakout = pygame.image.load("breakout.png")
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(self.losealifesound)
            if self.life > 1:
                while self.pause == True:
                    breakout = pygame.transform.scale(breakout,(100,25))
                    bigfont = pygame.font.Font("RepriseTitleStd.otf",40)
                    smallfont = pygame.font.Font("ERASDEMI.TTF",20)
                    loselife = bigfont.render("Rats! You have lost a life.",0,red)
                    instruction = smallfont.render("Press 1 to continue.",0,white)
                    self.screen.fill(black)
                    self.screen.blit(loselife,(160,150))
                    self.screen.blit(instruction,(300,200))
                    self.screen.blit(breakout,(675,450))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                self.pause = False  
                                self.life -= 1
                                self.reset()
                                self.run
            else:
                if self.score > 0: 
                    highscore(self.screen,'HighScores.txt',self.score)
                while self.pause == True:
                    
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                self.pause = False
                                self.level = 1
                                self.life = 3
                                self.score = 0
                                self.gamespeed = 60
                                self.reset()
                                self.run
                        #if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_3:
                                self.running = False
                                pygame.quit()
                                sys.exit()
                        #if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_2:
                                print("here")
                                self.highscores = not self.highscores
                    if self.highscores == True:
                        # print("yo")
                        breakout = pygame.transform.scale(breakout,(100,25))
                        bigfont = pygame.font.Font("RepriseTitleStd.otf",40)
                        smallfont = pygame.font.Font("ERASDEMI.TTF",25)
                        label0 = bigfont.render("High Scores",0,white)
                        label1 = smallfont.render("Press 1 to start",0,white)
                        label2 = smallfont.render("Press 3 to quit",0,white)
                        self.screen.fill(black)
                        self.screen.blit(breakout,(675,450))
                        self.screen.blit(label0,(300,50))
                        self.screen.blit(label1,(50,380))
                        self.screen.blit(label2,(50,410))
                        top10(self.screen, 'HighScores.txt')
                        pygame.display.flip()
                    else:
                        gameover = pygame.image.load("gameover.png")
                        smallfont = pygame.font.Font('ERASDEMI.TTF',20)
                        endscore = smallfont.render("Your score was " + str(self.score),0,white)
                        restartinst = smallfont.render("Press 1 to restart the game", 0, white)
                        vscores = smallfont.render("Press 2 to view all highscores", 0, white)
                        quittxt = smallfont.render("Press 3 to quit", 0, white)
                        self.screen.fill(black)
                        self.screen.blit(gameover,(100,100))
                        self.screen.blit(endscore,(300,200))
                        self.screen.blit(restartinst,(300,250))
                        self.screen.blit(vscores,(300,300))
                        self.screen.blit(quittxt,(300,350))
                        pygame.display.flip()


           



    def render(self):
        self.screen.fill(black)
        self.spritesgroup.draw(self.screen)
        smallfont = pygame.font.Font("ERASDEMI.TTF",20)
        self.screen.blit(smallfont.render("Time: {0:02}".format(self.seconds) + "s",0,blue),(20,0))
        self.screen.blit(smallfont.render("Life: " + str(self.life),0,red),(140,0))
        self.screen.blit(smallfont.render("Level: " + str(self.level),0,white),(560,0))
        self.screen.blit(smallfont.render("Score: " +str(self.score),0,white),(660,0))   
        
        pygame.display.flip()

      
game().run()

