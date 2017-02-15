# github.com/chrhyman/res

import math
from constants import *

# class to handle number of players and quantities of them in game
class Numbers:
    def __init__(self, players):
        assert 5 <= players <= 10, 'Error: Must have 5-10 players.'
        self.players = players

    def getSpies(self):     # 1/3 of all players are spies (round up)
        return int(math.ceil(self.players * 0.33))

    def getRes(self):       # all players that aren't spies are res
        return self.players - self.getSpies()

    def getTeamSize(self, mission):     # static from game rules
        if mission == 1:
            if self.players <= 7:   return 2
            else:                   return 3
        elif mission == 2:
            if self.players <= 7:   return 3
            else:                   return 4
        elif mission == 3:
            if self.players == 5:   return 2
            elif self.players == 7: return 3
            else:                   return 4
        elif mission == 4:
            if self.players <= 6:   return 3
            elif self.players == 7: return 4
            else:                   return 5
        elif mission == 5:
            if self.players == 5:   return 3
            elif self.players <= 7: return 4
            else:                   return 5
        else:
            assert False, 'Error: Mission number %s does not exist' % mission

    def getFailsNeeded(self, mission):  # mission 4 needs two fails with 7+
        if mission == 4 and self.players >= 7:
            return 2
        else:
            return 1

# Role object sets appropriate flags when initialized with role type
class Role:
    ROLELIST = (VANRES, MERLIN, PERCIVAL, VANSPY, ASSASSIN, MORGANA, MORDRED, MORDASS, OBERON)
    def __init__(self, type):
        assert role in ROLELIST, 'Error: Role "%s" does not exist.' % type
        self.type = type
        if self.type in RESROLES:
            self.isRes = True           # flag True for Res only
            self.canShoot = False       # flag True for Assassin
            self.spySeenBySpies = False # flag True for non-Oberon spies
            self.spySeenByMerl = False  # flag True for non-Mordred spies
            self.canSeeSpies = False # flag True for Merlin and non-Oberon spies
            self.looksLikeMerl = False  # flag True for Merlin and Morgana
            self.canSeeMerl = False     # flag True for Percival
            if self.type == MERLIN:
                self.canSeeSpies = True
                self.looksLikeMerl = True
            if self.type == PERCIVAL:
                self.canSeeMerl = True
        if self.type in SPYROLES:
            self.isRes = False
            self.canShoot = False
            self.spySeenBySpies = True
            self.spySeenByMerl = True
            self.canSeeSpies = True
            self.looksLikeMerl = False
            self.canSeeMerl = False
            if self.type in (ASSASSIN, MORDASS):
                self.canShoot = True
            if self.type == MORGANA:
                self.looksLikeMerl = True
            if self.type in (MORDRED, MORDASS):
                self.spySeenByMerl = False
            if self.type == OBERON:
                self.spySeenBySpies = False
                self.canSeeSpies = False
class Team:
class Vote:
