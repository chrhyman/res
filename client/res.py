VERSION = '0.0.5'
# A Python (pygame) implementation of The Resistance
# github.com/chrhyman/res

import sys, os.path
import pygame, requests
import draw, check
from pygame.locals import *
from constants import *

FILE = os.path.abspath(__file__)
ROOTDIR = os.path.dirname(os.path.dirname(FILE))
RESOURCES = os.path.join(ROOTDIR, 'resources')

BASEURL = 'http://wugs.pythonanywhere.com/games/res'

CONSOLASPATH = os.path.join(RESOURCES, 'font', 'consolas.ttf')

GETUPDATE = 4000 # frequency of GETting data in loops, in milliseconds

def main():
    global FPSCLOCK, DISPLAYSURF, MAINFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    ICON = pygame.image.load(os.path.join(RESOURCES, 'img', 'icon.png'))
    pygame.display.set_icon(ICON)   # sets taskbar logo/icon
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    MAINFONT = getFont(18)
    BIGFONT = getFont(80)
    pygame.display.set_caption('The Resistance - v. ' + VERSION)

    showStartScreen()
    checkVer()
    while True:
        lobbyLoop()

def lobbyLoop():
    DISPLAYSURF.fill(BGCOLOR)
    loadSurf, loadRect = draw.lineText('Loading ...', LIGHTGRAY, MAINFONT)
    loadRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    DISPLAYSURF.blit(loadSurf, loadRect)
    while True:
        titleSurf, titleRect = draw.lineText('Lobby', RESBLUE, BIGFONT, MARGIN, MARGIN)
        bodyRect = Rect(MARGIN, titleRect.bottom + PADDING, BODYWIDTH, WINDOWHEIGHT - MARGIN - PADDING - titleRect.bottom)
        overlay = pygame.Surface((bodyRect.width, bodyRect.height))
        overlay.blit(DISPLAYSURF, (0, 0), bodyRect) # gets current main window
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(overlay, bodyRect.topleft) # keeps last version of  lobby window consistent
        if pygame.time.get_ticks() % GETUPDATE < 100: # check lobby updates
            displayLobbies(bodyRect)    # lags game if run constantly
        DISPLAYSURF.blit(titleSurf, titleRect)
        try:
            if boxlist:
                for row in range(len(boxlist)):
                    for col in range(len(boxlist[row])):
                        boxRect = Rect(boxlist[row][col])
                        midbottom = (boxRect.width/2, boxRect.height - PADDING)
                        draw.makeButton('enterroom', DISPLAYSURF, midbottom=(boxRect.centerx, boxRect.y+boxRect.height-PADDING))
        except NameError:
            pass
        pygame.draw.rect(DISPLAYSURF, LIGHTGRAY, bodyRect, 2)
        draw.makeButton('newroom', DISPLAYSURF, top=MARGIN, right=WINDOWWIDTH - MARGIN)

        check.forQuit()
        pygame.event.clear()    # possibly solves 'freezing' issue in 0.0.1 where QUIT/ESC fail to terminate the program
        updateDisplay()

def displayLobbies(enclosure):
    global boxlist
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, enclosure) # clears body rect area
    BOXCOLS = 4
    BOXROWS = 2
    box_width = int((enclosure.width - PADDING*(BOXCOLS+1))/BOXCOLS)
    box_height = int((enclosure.height - PADDING*(BOXROWS+1))/BOXROWS)
    # nest for loops to iterate over area of boxes
    boxlist = [] # boxes found by boxlist[row][col]
    for row in range(BOXROWS):
        boxlist.append([])
        for col in range(BOXCOLS):
            x = enclosure.left + PADDING + col*(box_width+PADDING)
            y = enclosure.top + PADDING + row*(box_height+PADDING)
            boxlist[row].append((x, y, box_width, box_height))
    l = requests.get(BASEURL + '/lobby/data')
    lobbydata = l.json()    # lobbydata["roomnum"] returns dict defining room
# keys: description (str), leader (str), players (list), spectators (list), room (int), private (bool), password (str if private=True, else None)
    i = 0   # only show first ROWS*COLS active lobbies
    temp = []
    for key, value in lobbydata.items():
        r = value['room']
        if len(lobbydata) > BOXCOLS * BOXROWS:
            assert False, 'Too many lobbies! Ask Chris to fix this.'
        else:
            temp.append(value)
        assert len(temp) <= BOXCOLS * BOXROWS, 'ERROR: Too many lobbies to display'
    lobbydata = temp    # Dict > List
    if len(lobbydata) == 0:
        noneSurf, noneRect = draw.lineText('No lobbies!', DARKGRAY, MAINFONT)
        loadRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        DISPLAYSURF.blit(loadSurf, loadRect)
    else:
        for item in range(len(lobbydata)):
            lobbydata[item]['lobbySurf'] = makeLobbySurf(lobbydata[item], box_width, box_height)
            assert item/BOXCOLS < BOXROWS, 'Too many items in list!'
            DISPLAYSURF.blit(lobbydata[item]['lobbySurf'], boxlist[item/BOXCOLS][item % BOXCOLS])

def makeLobbySurf(dict, width, height):
    lobSurf = pygame.Surface((width, height))
    lobSurf.fill(BGCOLOR)
    tFont = getFont(40)
    ts, tr = draw.lineText('Room ' + str(dict['room']), RESBLUE, tFont, PADDING, PADDING)
    lobSurf.blit(ts, tr)
    pygame.draw.line(lobSurf, LIGHTRED, (0, tr.bottom), (width, tr.bottom), 2)
    if dict['private']:
        ps, pr = draw.lineText('PRIV', SPYRED, getFont(14))
        pr.topright = (width-PADDING, PADDING)
        lobSurf.blit(ps, pr)
    draw.textBox(lobSurf, dict['description'], TEXTCOLOR, (PADDING, PADDING + tr.bottom, width-PADDING*2, height), MAINFONT)
    players_text = 'Players: '
    for player in range(len(dict['players'])):
        players_text = players_text + dict['players'][player]
        if player != len(dict['players']) - 1:
            players_text = players_text + ', '
    draw.textBox(lobSurf, players_text, TEXTCOLOR, (PADDING, PADDING + tr.bottom + MAINFONT.size('Tg')[1]*3, width-PADDING*2, height), MAINFONT)
    return lobSurf

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

def getFont(size):
    return pygame.font.Font(CONSOLASPATH, size)

def updateDisplay():
    verFont = getFont(11)
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
