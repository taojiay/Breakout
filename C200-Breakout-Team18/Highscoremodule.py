import pygame, sys
pygame.font.init()
pygame.init()

grey = (150,150,150)
white = (255,255,255)
black = (0,0,0)
myfont = pygame.font.Font("ERASDEMI.TTF",25)


def readHscore(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close

    Hscore = 0
    

    for line in lines:
        name, score = line.strip().split(",")
        score = int(score)
        if score>Hscore:
            Hscore = score
            Hname = name
    return Hname,Hscore

def write(fileName, playerName, playerScore):
    scoreFile = open(fileName, 'a')
    print(playerName + ",", playerScore, file = scoreFile)
    scoreFile.close()


def top10(screen, fileName):
    x = 400
    y = 400
    file = open(fileName, 'r')
    lines = file.readlines()
    scores = []
    for line in lines:
        seperate = line.index(',')
        name = line[:seperate]
        score = int(line[seperate+1:-1])
        scores.append((score,name))
    file.close
    scores.sort(reverse = True)
    highest = scores[:10]
    
    box = pygame.surface.Surface((250,330))
    box.fill(white)

    for i, scoreent in enumerate(highest):
        label10 = myfont.render(scoreent[1] + " " + str(scoreent[0]), True, black) 
        label11 = label10.get_rect(center = (x//3.3,30*i+30))#spacing between rows and positioning of high scores from top of box
        box.blit(label10, label11)
    screen.blit(box,(270,100))
    pygame.display.flip()


def inputbox(screen, text):
    name = ""
    def giveName(screen, name):
        pygame.draw.rect(box, white,(50,60,x-100,20),0)
        label10 = myfont.render(name,True,black)
        label11 = label10.get_rect(center = (x//2, int(y*.7)))
        box.blit(label10, label11)
        screen.blit(box,(50,y//2))
        pygame.display.flip()

    x = 680
    y = 100

    box = pygame.surface.Surface((x,y))
    pygame.draw.rect(box, black,(0,0,x,y),1)
    box.fill(grey)
    label10 = myfont.render(text, True, black)
    label11 = label10.get_rect(center=(x//2,int(y*.3)))
    box.blit(label10, label11)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                inputK = event.key #returns name when pressing enter or return
                if inputK in [13,271]:
                    return name
                elif inputK == 8:  #for backspace
                    name = name[:-1]
                elif inputK <= 300:
                    if pygame.key.get_mods() and pygame.KMOD_SHIFT and 126 >+ inputK >+ 32:#the numbers are unicode for the letters
                        inputK -= 32
                    name += chr(inputK)
        giveName(screen, name)

def highscore(screen, fileName, playerScore):
    Hname, Hscore = readHscore(fileName)
    if playerScore > Hscore:
        playerName = inputbox(screen, "You have beaten the High Score! Please enter your intials")
    elif playerScore == Hscore:
        playerName = inputbox(screen, "You have tied the High Score! Please enter your intials")
    elif playerScore < Hscore:
        playerName = inputbox(screen, "High Score! Please enter you initials")
    if playerName == None or len(playerName) == 0:
        return #no update

    write(fileName, playerName, playerScore)
    screen.fill(black)
    return
    




