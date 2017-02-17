# github.com/chrhyman/res

import pygame
from pygame.locals import *
import res
from constants import BETATEXT, OLDTEXT

def backdoor(): # bypass version check error (debug & testing only!)
    a, b, c = None, None, None
    for event in pygame.event.get(KEYUP):
        if event.key == K_w:
            a = True
        elif event.key == K_u:
            b = True
        elif event.key == K_g:
            c = True
    if a and b and c:
        return True     # W, U, and G released on same frame
    return False

def forKeyPress():
    forQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue # removes keydowns from queue
        return event.key    # returns keyup key
    return None # returns a None object if no keydown or keyup events

def forQuit():
    for event in pygame.event.get(QUIT):
        res.terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            res.terminate()
        pygame.event.post(event) # put other KEYUPs back if not ESC
