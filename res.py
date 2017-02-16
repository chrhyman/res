VERSION = '0.0.3'
# A Python (pygame) implementation of The Resistance
# github.com/chrhyman/res

import sys, os
import pygame, requests
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
    checkVer()
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

# gets version from server (json data, which requests decodes)
# interrupts code if version mismatch
def checkVer():
    get_ver = requests.get('http://wugs.pythonanywhere.com/games/res/ver')
    ver_data = get_ver.json()
    server_ver = ver_data['version']
    beta_ver = ver_data['beta']
    old_dates = ver_data['old dates']   # old_dates['0.0.1'] -> '2017-02-14'
    if VERSION != server_ver:    # old or beta version
        beta, old = None, None
        if VERSION == beta_ver:
            beta = True
        elif VERSION in old_dates:
            old = True
        else:   # if it isn't beta, current, or old, it doesn't exist
            assert False, 'Version Error: Version does not exist. Visit github.com/chrhyman/res/issues and submit a bug report.'
        verSurf = pygame.Surface((int(WINDOWWIDTH * 0.5), int(WINDOWHEIGHT * 0.5)))
        verRect = verSurf.get_rect()
        verSurf.fill(BGCOLOR)
        pygame.draw.rect(verSurf, LIGHTGRAY, verRect, 4)
        ts, tr = titleText('Bad Version', SPYRED, PADDING, PADDING)
        verSurf.blit(ts, tr)
        textRect = (PADDING, tr.bottom + PADDING, verRect.width - PADDING*2, verRect.height - tr.bottom - PADDING)
        verText = 'You are running version ' + VERSION + '. The current version is ' + server_ver + '. '
        if beta:
            verText = verText + 'This beta version may not interact correctly with the main server due to version differences. It is recommended that beta versions be used on test servers, not on the main server. Please use ESC to quit this application and make the necessary changes. If you believe you are getting this message in error, please contact Chris (chrhyman@gmail.com).'
        if old:
            verText = verText + 'This old version will not interact with the server correctly. Please use ESC to quit this application and visit github.com/chrhyman/res to download v. ' + server_ver + '. If you are getting this message in error (for instance, you do have the current version), please create a bug report under "Issues" at the Github linked above.'
        drawText(verSurf, verText, TEXTCOLOR, textRect, MAINFONT, spacing=2)
        verRect.center = (int(WINDOWWIDTH * 0.5), int(WINDOWHEIGHT * 0.5))
        DISPLAYSURF.blit(verSurf, verRect)
        updateDisplay()
        while True:
            checkForQuit()
            pygame.event.clear()
    else:   # up to date
        return
    assert False, ('Error. Version verification failure.')

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
# returns non-blitted text (if any didn't fit)
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
    pygame.draw.rect(DISPLAYSURF, WHITE, verRect)
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
