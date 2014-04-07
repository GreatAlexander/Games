import pygame
import numpy as np
from Global import *
 
class Display(object):
    #  fpsClock = pygame.time.Clock()
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Res), 0)
        pygame.display.set_caption(TITLE_TEXT)
        pygame.mouse.set_visible(1)
    
    def initializeEverything(self):
        return self
        
    def drawBackground(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(WALL)
        return background
    
    def drawPitch(self, background):
        outlinebox = pygame.Rect(WALL_WIDTH, WALL_WIDTH, PITCH[0] - 2*WALL_WIDTH, PITCH[1] - 2*WALL_WIDTH)
        pitchbox = pygame.Rect(Edge, Edge, PITCH[0] - 2*Edge, PITCH[1] - 2*Edge)
        titlebox = pygame.Rect(0, PITCH[1], Xres, Yres)
        line1box = pygame.Rect(PITCH[0]*1/4-Linewidth/2, WALL_WIDTH, Linewidth, PITCH[1]-2*WALL_WIDTH)
        line2box = pygame.Rect(PITCH[0]*2/4-Linewidth/2, WALL_WIDTH, Linewidth, PITCH[1]-2*WALL_WIDTH)
        line3box = pygame.Rect(PITCH[0]*3/4-Linewidth/2, WALL_WIDTH, Linewidth, PITCH[1]-2*WALL_WIDTH)
        goalyellow=pygame.Rect(WALL_WIDTH/2, PITCH[1]/2 - Goalwidth/2, Goaldepth, Goalwidth)
        goalblue=pygame.Rect(PITCH[0] - WALL_WIDTH, PITCH[1]/2 - Goalwidth/2, Goaldepth, Goalwidth)
    
        pygame.draw.rect(background, TAPE, outlinebox, 0)
        pygame.draw.rect(background, GRASS, pitchbox, 0)
        pygame.draw.rect(background, TITLEBACK, titlebox, 0)
        pygame.draw.rect(background, TAPE, line1box, 0)
        pygame.draw.rect(background, TAPE, line2box, 0)
        pygame.draw.rect(background, TAPE, line3box, 0)
        pygame.draw.rect(background, YELLOW, goalyellow, 0)
        pygame.draw.rect(background, BLUE, goalblue, 0)
        pygame.draw.line(background, LINE, (PITCH[0]*1/4, WALL_WIDTH), (PITCH[0]*1/4, PITCH[1]-WALL_WIDTH))
        pygame.draw.line(background, LINE, (PITCH[0]*2/4, WALL_WIDTH), (PITCH[0]*2/4, PITCH[1]-WALL_WIDTH))
        pygame.draw.line(background, LINE, (PITCH[0]*3/4, WALL_WIDTH), (PITCH[0]*3/4, PITCH[1]-WALL_WIDTH))
    
    def centreTitleOnBackground(self, background):
        if pygame.font:
            font = pygame.font.Font(None, Fntsize)
            text = font.render(TITLE_TEXT, 1, TITLE)
            textpos = text.get_rect(centerx=Xres/2, centery=Yres - Fntsize/2)
            background.blit(text, textpos)
    
    def showFeatureOnScreen(self, name, x, fr=None):
        ''' Show current frame on self 
        '''
        myfont = pygame.font.SysFont("monospace", 15)
        if fr != None:
            text = myfont.render(name + ':' + str(fr), 1, (255, 255, 0))
            self.screen.blit(text, (x * 15, PITCH[1] - WALL_WIDTH + 10))
        else:
            text = myfont.render(name, 1, (255, 255, 0))
            self.screen.blit(text, (x * 15, PITCH[1] - WALL_WIDTH + 10))
            
    def updateFeaturesOnScreen(self, frame, ball):
        self.showFeatureOnScreen('Frame', 5, "%02d" % frame)
        self.showFeatureOnScreen('Pos', 15, ball.rect.center)
        self.showFeatureOnScreen('Speed', 25, np.around(ball.speed, 3))
        self.showFeatureOnScreen('Theta', 35, np.around(ball.orientation, 2))
    
    def drawEverything(self, background, ballSprite):
        self.screen.blit(background, (0, 0))
        ballSprite.draw(self.screen)