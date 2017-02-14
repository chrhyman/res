VERSION = '0.0.1'
# A Python (pygame) implementation of The Resistance
# github.com/chrhyman/res

import pygame, sys
from pygame.locals import *
from constants import *

FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
MARGIN = 25

# colors            R    G    B
WHITE           = (255, 255, 255)
BLACK           = (  0,   0,   0)
RESBLUE         = ( 80, 180, 210)
SPYRED          = (195,  60,  60)
DARKGRAY        = ( 65,  65,  65)

BGCOLOR = WHITE
TEXTCOLOR = BLACK

def main():
    global FPSCLOCK, DISPLAYSURF, MAINFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    MAINFONT = pygame.font.Font('resources/consolas.ttf', 18)
    BIGFONT = pygame.font.Font('resources/consolas.ttf', 100)
    pygame.display.set_caption('The Resistance')

    showStartScreen()
    while True:
        # lobby loop that sends user to a game loop function
        DISPLAYSURF.fill(BGCOLOR)
        checkForQuit()
        updateDisplay()

def showStartScreen():
    titleSurf = BIGFONT.render('The Resistance', True, RESBLUE)
    titleRect = titleSurf.get_rect()
    titleRect.midtop = (int(WINDOWWIDTH / 2), MARGIN)

    footerSurf = MAINFONT.render('Press any key to continue.', True, SPYRED)
    footerRect = footerSurf.get_rect()
    footerRect.midbottom = (int(WINDOWWIDTH / 2), WINDOWHEIGHT - MARGIN)

    descRect = (MARGIN, titleRect.bottom + MARGIN, WINDOWWIDTH - MARGIN*2, WINDOWHEIGHT - titleRect.height - footerRect.height - MARGIN*4)
    while True:
        if checkForKeyPress() != None:
            return
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(titleSurf, titleRect)
        drawText(DISPLAYSURF, DESC, TEXTCOLOR, descRect, MAINFONT, 1)
        if pygame.time.get_ticks() % 1500 < 900:
            DISPLAYSURF.blit(footerSurf, footerRect)
        updateDisplay()

# text wrap for boxes of text
# returns non-blitted text
def drawText(surface, text, color, rect, font, spacing=-2, aa=True):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = spacing
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
    return text


def checkForKeyPress():
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue # removes keydowns from queue
        return event.key
    return None

def updateDisplay():
    verFont = pygame.font.Font('resources/consolas.ttf', 11)
    verSurf = verFont.render('(c) Chris Hyman v.' + VERSION, True, DARKGRAY)
    verRect = verSurf.get_rect()
    verRect.bottomright = (WINDOWWIDTH-2, WINDOWHEIGHT-2)
    DISPLAYSURF.blit(verSurf, verRect)
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event) # put other KEYUPs back if not ESC

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
