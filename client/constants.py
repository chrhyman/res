# github.com/chrhyman/res

FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
MARGIN = 25
PADDING = 10
BODYWIDTH = WINDOWWIDTH - MARGIN*2

# colors            R    G    B
WHITE           = (255, 255, 255)
BLACK           = (  0,   0,   0)
RESBLUE         = ( 60, 160, 220)
SPYRED          = (195,  60,  60)
LIGHTRED        = (210, 130, 130)
DARKGRAY        = ( 65,  65,  65)
LIGHTGRAY       = (190, 190, 190)

BGCOLOR = WHITE
TEXTCOLOR = BLACK
VERCOLOR = DARKGRAY

VANRES = 'vanilla resistance'
MERLIN = 'Merlin'
PERCIVAL = 'Percival'
RESROLES = (VANRES, MERLIN, PERCIVAL)
VANSPY = 'vanilla spy'
ASSASSIN = 'assassin'
MORGANA = 'Morgana'
MORDRED = 'Mordred'
MORDASS = 'Mordred/Assassin'
OBERON = 'Oberon'
SPYROLES = (VANSPY, ASSASSIN, MORGANA, MORDRED, MORDASS, OBERON)

UP = 'up'
DOWN = 'down'

BETATEXT = 'This beta version may not interact correctly with the main server due to version differences. It is recommended that beta versions be used on test servers, not on the main server. Please use ESC to quit this application and make the necessary changes. If you believe you are getting this message in error, please contact Chris (chrhyman@gmail.com).'

OLDTEXT = 'This old version will not interact with the server correctly. Please use ESC to quit this application and visit github.com/chrhyman/res to download the current version. If you are getting this message in error (for instance, you do have the current version), please create a bug report under "Issues" at the Github linked above.'

NEWLINE = '''                                                                                                 ''' # 97 characters
DESC = ('''     The Resistance is a simple, fun, and exciting secret identity game designed by Don Eskridge in the style of games like Mafia and Werewolf. The important difference between those games and this one is that The Resistance does not require a narrator or non-player to moderate the game. When played in person, this game self-moderates. However, the trade-off is that this is less simple to do digitally with friends online.                                                         ''' +
NEWLINE * 2 +
'''     Due to the limited space offered by this application and the clunkiness of text in pygame, I will not be explaining the game in full within the GUI/user interface. For an explanation of how The Resistance works and for a guide on using this application when it feels unintuitive, please visit wugs.pythonanywhere.com/games/res/ or look at the repo on Github at github.com/chrhyman/res   ''' +
NEWLINE * 2 +
'''     This application is a Python (pygame) implementation of The Resistance which uses a small amount of JSON to interface with a "server". For the coders among you, I recommend looking at the source on Github, as it's much simpler than you might think. For the non-coders among you, it is all extremely complex and I am a very, very smart person.                                           ''' +
NEWLINE * 2 +
'''     You can quit at any time by closing this window or by pressing ESC. You may not be able to rejoin your game.''')
