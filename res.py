VERSION = '0.0.2'
# A Python (pygame) implementation of The Resistance
# github.com/chrhyman/res

import sys, os
import pygame
from pygame.locals import *
from constants import *

FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
MARGIN = 25
PADDING = 10
BODYWIDTH = WINDOWWIDTH - MARGIN*2

CONSOLASPATH = os.path.join('resources', 'font', 'consolas.ttf')

# colors            R    G    B
WHITE           = (255, 255, 255)
BLACK           = (  0,   0,   0)
RESBLUE         = ( 60, 160, 220)
SPYRED          = (195,  60,  60)
DARKGRAY        = ( 65,  65,  65)
LIGHTGRAY       = (190, 190, 190)

BGCOLOR = WHITE
TEXTCOLOR = BLACK
VERCOLOR = DARKGRAY

def main():
    global FPSCLOCK, DISPLAYSURF, MAINFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    ICON = pygame.image.load(os.path.join('resources', 'img', 'icon.png'))
    pygame.display.set_icon(ICON)   # sets taskbar logo/icon
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    MAINFONT = pygame.font.Font(CONSOLASPATH, 18)
    BIGFONT = pygame.font.Font(CONSOLASPATH, 80)
    pygame.display.set_caption('The Resistance - v. ' + VERSION)

    showStartScreen()
    while True:
        lobbyLoop()

def lobbyLoop():
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        titleSurf, titleRect = titleText('Lobby', RESBLUE, MARGIN, MARGIN)
        DISPLAYSURF.blit(titleSurf, titleRect)
        bodyRect = (MARGIN, titleRect.bottom + PADDING, BODYWIDTH, WINDOWHEIGHT - MARGIN - PADDING - titleRect.bottom)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, bodyRect, 2)

        makeButton('newroom', top=MARGIN, right=WINDOWWIDTH - MARGIN)

        checkForQuit()
        pygame.event.clear()    # possibly solves 'freezing' issue in 0.0.1 where QUIT/ESC fail to terminate the program
        updateDisplay()

def makeButton(name, top=None, left=None, bottom=None, right=None):
    button = name + '.png'
    pressed = name + '_pressed.png'
    imgSurf = pygame.image.load(os.path.join('resources', 'button', button))
    imgRect = imgSurf.get_rect()
    if top: imgRect.top = top
    if left: imgRect.left = left
    if bottom: imgRect.bottom = bottom
    if right: imgRect.right = right
    if pygame.mouse.get_pressed()[0] and imgRect.collidepoint(pygame.mouse.get_pos()):
        imgSurf = pygame.image.load(os.path.join('resources', 'button', pressed))

    DISPLAYSURF.blit(imgSurf, imgRect)

def showStartScreen():
    titleSurf, titleRect = titleText('The Resistance', RESBLUE, MARGIN, MARGIN)

    footerSurf = MAINFONT.render('Press any key to continue.', True, SPYRED)
    footerRect = footerSurf.get_rect()
    footerRect.midbottom = (int(WINDOWWIDTH / 2), WINDOWHEIGHT - MARGIN)

    descRect = (MARGIN, titleRect.bottom + PADDING, BODYWIDTH, WINDOWHEIGHT - titleRect.height - footerRect.height - MARGIN*2 - PADDING*2)
    while True:
        if checkForKeyPress() != None:
            return
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(titleSurf, titleRect)
        drawText(DISPLAYSURF, DESC, TEXTCOLOR, descRect, MAINFONT, 1)
        if pygame.time.get_ticks() % 1500 < 900:
            DISPLAYSURF.blit(footerSurf, footerRect)
        updateDisplay()

def titleText(text, color, left, top):
    titleSurf = BIGFONT.render(text, True, color)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (left, top)
    return titleSurf, titleRect

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
    verFont = pygame.font.Font(CONSOLASPATH, 11)
    verSurf = verFont.render('(c) Chris Hyman v.' + VERSION, True, VERCOLOR)
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
    # send POST request that removes user from games/lobbies
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
