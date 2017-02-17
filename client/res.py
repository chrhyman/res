VERSION = '0.0.4'
# A Python (pygame) implementation of The Resistance
# github.com/chrhyman/res

import sys, os.path
import pygame, requests
import draw, check
from pygame.locals import *
from constants import *

FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
MARGIN = 25
PADDING = 10
BODYWIDTH = WINDOWWIDTH - MARGIN*2

FILE = os.path.abspath(__file__)
ROOTDIR = os.path.dirname(os.path.dirname(FILE))
RESOURCES = os.path.join(ROOTDIR, 'resources')

BASEURL = 'http://wugs.pythonanywhere.com/games/res'

CONSOLASPATH = os.path.join(RESOURCES, 'font', 'consolas.ttf')

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
    ICON = pygame.image.load(os.path.join(RESOURCES, 'img', 'icon.png'))
    pygame.display.set_icon(ICON)   # sets taskbar logo/icon
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    MAINFONT = pygame.font.Font(CONSOLASPATH, 18)
    BIGFONT = pygame.font.Font(CONSOLASPATH, 80)
    pygame.display.set_caption('The Resistance - v. ' + VERSION)

    showStartScreen()
    checkVer()
    while True:
        lobbyLoop()

def lobbyLoop():
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        titleSurf, titleRect = draw.lineText('Lobby', RESBLUE, BIGFONT, MARGIN, MARGIN)
        DISPLAYSURF.blit(titleSurf, titleRect)
        bodyRect = (MARGIN, titleRect.bottom + PADDING, BODYWIDTH, WINDOWHEIGHT - MARGIN - PADDING - titleRect.bottom)
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, bodyRect, 2)

        draw.makeButton('newroom', DISPLAYSURF, top=MARGIN, right=WINDOWWIDTH - MARGIN)

        displayLobbies(bodyRect)

        check.forQuit()
        pygame.event.clear()    # possibly solves 'freezing' issue in 0.0.1 where QUIT/ESC fail to terminate the program
        updateDisplay()

def displayLobbies(enclosure):
    enclosure = Rect(enclosure)
    BOXCOLS = 4
    BOXROWS = 2
    box_width = int((enclosure.width - PADDING*(BOXCOLS+1))/BOXCOLS)
    box_height = int((enclosure.height - PADDING*(BOXROWS+1))/BOXROWS)
    # nest for loops to iterate over area of boxes
    for row in range(BOXROWS):
        for col in range(BOXCOLS):
            x = enclosure.left + PADDING + col*(box_width+PADDING)
            y = enclosure.top + PADDING + row*(box_height+PADDING)
            pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, (x, y, box_width, box_height)) # placeholder rectangles; will become boxes representing each open library, fetched from BASEURL/lobby/data

# gets version from server (json data, which requests decodes)
# interrupts code if version mismatch
def checkVer():
    get_ver = requests.get(BASEURL + '/ver')
    ver_data = get_ver.json()
    server_ver = ver_data['version']
    beta_ver = ver_data['beta']
    old_vers = ver_data['old dates']   # old_dates['0.0.1'] -> '2017-02-14'
    if VERSION != server_ver:    # old or beta version
        beta, old = None, None
        if VERSION == beta_ver:
            beta = True
        elif VERSION in old_vers:
            old = True
        else:   # if it isn't beta, current, or old, it doesn't exist
            assert False, 'Version Error: Version does not exist. Visit github.com/chrhyman/res/issues and submit a bug report.'
        verSurf = pygame.Surface((int(WINDOWWIDTH * 0.5), int(WINDOWHEIGHT * 0.5)))
        verRect = verSurf.get_rect()
        verSurf.fill(BGCOLOR)
        pygame.draw.rect(verSurf, LIGHTGRAY, verRect, 4)
        ts, tr = draw.lineText('Bad Version', SPYRED, BIGFONT, PADDING, PADDING)
        verSurf.blit(ts, tr)
        textRect = (PADDING, tr.bottom + PADDING, verRect.width - PADDING*2, verRect.height - tr.bottom - PADDING)
        verText = 'You are running version ' + VERSION + '. The current version is ' + server_ver + '. '
        if beta:
            verText = verText + BETATEXT
        if old:
            verText = verText + OLDTEXT
        draw.textBox(verSurf, verText, TEXTCOLOR, textRect, MAINFONT, spacing=0)
        verRect.center = (int(WINDOWWIDTH * 0.5), int(WINDOWHEIGHT * 0.5))
        DISPLAYSURF.blit(verSurf, verRect)
        updateDisplay()
        while True:
            check.forQuit()
            if check.backdoor():
                return
            pygame.event.clear()
            FPSCLOCK.tick(FPS)
    else:   # up to date
        return

def showStartScreen():
    titleSurf, titleRect = draw.lineText('The Resistance', RESBLUE, BIGFONT, MARGIN, MARGIN)
    footerSurf, footerRect = draw.lineText('Press any key to continue.', SPYRED, MAINFONT)
    footerRect.midbottom = (int(WINDOWWIDTH / 2), WINDOWHEIGHT - MARGIN)

    descRect = (MARGIN, titleRect.bottom + PADDING, BODYWIDTH, WINDOWHEIGHT - titleRect.height - footerRect.height - MARGIN*2 - PADDING*2)
    while True:
        if check.forKeyPress() != None:
            return
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(titleSurf, titleRect)
        draw.textBox(DISPLAYSURF, DESC, TEXTCOLOR, descRect, MAINFONT, 1)
        if pygame.time.get_ticks() % 1500 < 900:
            DISPLAYSURF.blit(footerSurf, footerRect)
        updateDisplay()

def updateDisplay():
    verFont = pygame.font.Font(CONSOLASPATH, 11)
    verSurf, verRect = draw.lineText('(c) Chris Hyman v.' + VERSION, VERCOLOR, verFont)
    verRect.bottomright = (WINDOWWIDTH-2, WINDOWHEIGHT-2)
    pygame.draw.rect(DISPLAYSURF, WHITE, verRect)
    DISPLAYSURF.blit(verSurf, verRect)
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def terminate():
    # send POST request that removes user from games/lobbies
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
