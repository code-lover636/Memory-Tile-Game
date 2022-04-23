import pygame, os, random

pygame.init()

# Declaring variables
WIDTH, HEIGHT = 800, 600
running = True
tiles = {}
asset = {}
icons = []
backdrops = {}
eventlist = []
lasttile = []
currenttile = []
removedtiles = []
count = 0
score = 1000
cor = None
ROW, COL = 6,9
originX, originY = 100,100

# Setting up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Remember it!")
FONT = pygame.font.Font('freesansbold.ttf', 17)
FINALSCORE = pygame.font.Font('freesansbold.ttf', 40)
correct = pygame.mixer.Sound("assets/correct.wav")
applause = pygame.mixer.Sound("assets/applause.wav")


# Loading images
for bg in os.listdir("assets/backdrops"):
    img = pygame.image.load("assets/backdrops/"+bg)
    backdrops[bg] = pygame.transform.scale(img, (WIDTH, HEIGHT))
bg = random.choice(list(backdrops.values()))

for im in os.listdir("assets"): 
    if im.endswith(".png"):  asset[im] = pygame.image.load("assets/"+im)

for im in os.listdir("assets/icons"): icons.append( pygame.image.load("assets/icons/"+im) )

icons *= 6
for t1 in range(ROW):
    for t2 in range(COL):
        tiles[originX+(70*t2), originY+(70*t1)] = random.choice(list(icons)) 
        icons.remove(tiles[originX+(70*t2), originY+(70*t1)])
        
# Functions
def wait_and_run(time):
    global count
    event = pygame.USEREVENT+count
    eventlist.append(event)
    count += 1
    pygame.time.set_timer(event ,time) 
    return event

def checkwin(last,seclast):
    global score, currenttile
    if tiles[last] == tiles[seclast]:
        removedtiles.append(last)
        removedtiles.append(seclast)
        pygame.mixer.Sound.play(correct)
        pygame.mixer.music.stop()
    elif [last,seclast] != currenttile: 
        score -= 5
        currenttile = [last,seclast]
    
    if len(removedtiles) == ROW*COL:         
        pygame.mixer.Sound.play(applause)
        pygame.mixer.music.stop()

def clicked(pos):
    global cor, lasttile
    for t1 in range(ROW):
        for t2 in range(COL):
            if  originX+(70*t2) < pos[0] < originX+(70*t2)+50 \
            and originY+(70*t1) < pos[1] < originY+(70*t1)+50:
                if cor == (originX+(70*t2),originY+(70*t1)): cor=None; lasttile=[]
                else: cor = (originX+(70*t2),originY+(70*t1))
                return
    cor=None; lasttile=[]
            
def draw_screen():
    global lasttile
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))

    factorX, factorY = 0,0
    for i in range(ROW):
        for j in range(COL):
            if (originX+factorX,originY+factorY) not in removedtiles:
                screen.blit(asset["tile.png"],(originX+factorX,originY+factorY))
            factorX+=70
        factorY+=70; factorX=0

    if cor:
        if len(lasttile) != 0:
            if lasttile[-1] != cor: 
                if len(lasttile) == 2: lasttile = [cor]
                else: lasttile.append(cor)        
        else: 
            lasttile.append(cor)
        if len(removedtiles) != ROW*COL:
            if lasttile[-1] not in removedtiles or lasttile[-2] not in removedtiles:
                if len(lasttile) >= 1: screen.blit(tiles[lasttile[-1]],lasttile[-1])
                if len(lasttile) >= 2: 
                    screen.blit(tiles[lasttile[-2]],lasttile[-2]) 
                    checkwin(lasttile[-1],lasttile[-2])            
        
    text = FONT.render(f'Score:{score}', True, (0,255,0))
    screen.blit(text,(10,10)) 
    if len(removedtiles) == ROW*COL: 
        screen.blit(asset["bingo.png"],(25,25)) 
        screen.blit(FINALSCORE.render(str(score), True, (0,255,0)),(420,440)) 
    pygame.display.update()

# Declaring userevents
BgEvent = wait_and_run(20 * 1000)

# Main loop
while running:
    for event in pygame.event.get():
        if   event.type == pygame.QUIT:  running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            clicked(event.pos)
        elif event.type == BgEvent: 
            bg = random.choice(list(backdrops.values()))            
            
    draw_screen()
     
    
pygame.quit()