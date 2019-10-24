import sys, pygame, random
from ww import *
from pygame.locals import *
pygame.init()

ww=Stage(20, 20, 24)
wu=Stage(20, 20, 24)
ww.set_player(KeyboardPlayer("icons/face-cool-24.png", ww))

ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 0, 3, 1))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 7, 4, 5))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 4, 10, 3))
ww.add_actor(Monster("icons/face-devil-grin-24.png", ww, 5, 20, 2))

num_walls=0
while num_walls<10:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(Wall("icons/wall.jpg", ww, x, y))
        num_walls+=1

num_sticky_boxes=0
while num_sticky_boxes<10:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(Sticky_Box("icons/emblem-package-sticky-2-24.png", ww, x, y))
        num_sticky_boxes+=1

def game_over(msg):
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((600, 500))
    pygame.display.set_caption('Game Over!')

    WHITE = (255, 255, 255)
    BLUE = (0, 0, 128)

    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render(msg, True, BLUE, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 250)

    while True:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

# YOUR COMMENT GOES HERE. BRIEFLY DESCRIBE WHAT THE FOLLOWING LOOP DOES.
num_boxes=0
while num_boxes<100: #As long as the num_boxes is less than 100
    x=random.randrange(ww.get_width()) #generates a random number from 0 to the width of the playing field and stores in x-coordinate
    y=random.randrange(ww.get_height()) #generates a random number from 0 to the height of the playing field ans stores in y-coordinate
    if ww.get_actor(x,y) is None: #if no actor in the random position
        ww.add_actor(Box("icons/emblem-package-2-24.png", ww, x, y)) #add actor in the free space
        num_boxes+=1 #add 1 to num_boxes counter

# YOUR COMMENT GOES HERE. BRIEFLY DESCRIBE WHAT THE FOLLOWING LOOP DOES.
while True:
    pygame.time.wait(100)
    for event in pygame.event.get(): #for every event that occurs in the game
        if event.type == pygame.QUIT or ww.game_over_lose() or ww.game_over_win():  #if the event is either to QUIT, player LOST, or player WON, then proceed
            if ww.game_over_win(): #if the player WON
                game_over('All monsters died, You WIN!') #Send game over for winner message
            if ww.game_over_lose(): #if the player LOST
                game_over('Game Over, you DIED!') # Send game over for loser message
            pygame.quit() #if the game is QUIT
            sys.exit(0) #Exit
        if event.type == pygame.KEYDOWN:
            ww.player_event(event.key)
    ww.step()
    ww.draw()
