# github.com/chrhyman/res

import os.path
import pygame
from res import RESOURCES

def makeButton(name, surface, top=None, left=None, bottom=None, right=None):
    button = name + '.png'
    pressed = name + '_pressed.png'
    imgSurf = pygame.image.load(os.path.join(RESOURCES, 'button', button))
    imgRect = imgSurf.get_rect()
    if top: imgRect.top = top
    if left: imgRect.left = left
    if bottom: imgRect.bottom = bottom
    if right: imgRect.right = right
    if pygame.mouse.get_pressed()[0] and imgRect.collidepoint(pygame.mouse.get_pos()):
        imgSurf = pygame.image.load(os.path.join(RESOURCES, 'button', pressed))

    surface.blit(imgSurf, imgRect)

def lineText(text, color, font, left=0, top=0):
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.topleft = (left, top)
    return textSurf, textRect

# text wrap for boxes of text
# returns non-blitted text (if any didn't fit)
def textBox(surface, text, color, rect, font, spacing=-2, aa=True):
    rect = pygame.locals.Rect(rect)
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
