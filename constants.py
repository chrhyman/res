# github.com/chrhyman/res

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

NEWLINE = '''                                                                                                 ''' # 97 characters
DESC = ('''     The Resistance is a simple, fun, and exciting secret identity game designed by Don Eskridge in the style of games like Mafia and Werewolf. The important difference between those games and this one is that The Resistance does not require a narrator or non-player to moderate the game. When played in person, this game self-moderates. However, the trade-off is that this is less simple to do digitally with friends online.                                                         ''' +
NEWLINE * 2 +
'''     Due to the limited space offered by this application and the clunkiness of text in pygame, I will not be explaining the game in full within the GUI/user interface. For an explanation of how The Resistance works and for a guide on using this application when it feels unintuitive, please visit wugs.pythonanywhere.com/games/res/ or look at the repo on Github at github.com/chrhyman/res   ''' +
NEWLINE * 2 +
'''     This application is a Python (pygame) implementation of The Resistance which uses a small amount of JSON to interface with a "server". For the coders among you, I recommend looking at the source on Github, as it's much simpler than you might think. For the non-coders among you, it is all extremely complex and I am a very, very smart person.''')
