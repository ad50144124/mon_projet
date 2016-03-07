# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.

"""

import soccersimulator,soccersimulator.settings
from decorator import *
from strategy import *
from decisiontree import *
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import KeyboardStrategy,show

import sys
sys.path.append("./sem6/")
import luluperet
from luluperet import team1




import numpy as np


"""
============================main===================================
"""


class StateLessStrategy(BaseStrategy):
    def __init__(self, decid):
        BaseStrategy.__init__(self,decid.__name__)
        self.decideur = decid
        self.info = dict()        
    def compute_strategy(self,state,id_team,id_player):
        aa = self.decideur(SoccerStateDecorator(state,id_team,id_player,self.info))
        return aa


class DTreeStrategy(BaseStrategy):
    def __init__(self,tree,dic,gen_feat):
        BaseStrategy.__init__(self,"Tree Strategy")
        self.dic = dic
        self.tree = tree
        self.gen_feat= gen_feat
    def compute_strategy(self, state, id_team, id_player):
        label = self.tree.predict([self.gen_feat(state,id_team,id_player)])[0]
        if label not in self.dic:
            print("Erreur : strategie %s non trouve" %(label,))
            return SoccerAction()
        return self.dic[label].compute_strategy(state,id_team,id_player)

dic = {"fonceur":StateLessStrategy(fonceur),"reflexion":StateLessStrategy(reflexion),"defent":StateLessStrategy(defent),"defent_l":StateLessStrategy(defent_l), "shooter":StateLessStrategy(shooter)}
st=DTreeStrategy(tree,dic,gen_features)


#team1=SoccerTeam("team1",[Player("t1j1",StateLessStrategy(random))])
#team2=SoccerTeam("team2",[Player("t2j1",StateLessStrategy(Smart1v1))])

team1m=SoccerTeam("team1",[Player("t1j1",StateLessStrategy(random)),Player("t1j2",StateLessStrategy(Smart1v1))])
team2m=SoccerTeam("team1",[Player("t2j1",StateLessStrategy(Smart2v2)),Player("t2j2",StateLessStrategy(Smart2v2))])

#team1=SoccerTeam("team1",[Player("t1j1",StateLessStrategy(fonceur)),Player("t1j2",StateLessStrategy(fonceur)),Player("t1j3",StateLessStrategy(fonceur)),Player("t1j4",StateLessStrategy(fonceur))])
#team2=SoccerTeam("team1",[Player("t1j1",StateLessStrategy(Smart1v1)),Player("t1j2",StateLessStrategy(Smart1v1)),Player("t1j3",StateLessStrategy(Smart1v1)),Player("t1j4",StateLessStrategy(Smart1v1))])

strat = KeyboardStrategy() #ou pour une sauvegarde automatique
#KeyboardStrategy(fn="monfichier.exp")
FS = StateLessStrategy(fonceur)
RF = StateLessStrategy(reflexion)
DF = StateLessStrategy(defent)
DL = StateLessStrategy(defent_l)
SH = StateLessStrategy(shooter)

strat.add("d",FS)
strat.add("q",RF)
strat.add("s",DF)
strat.add("z",DL)
strat.add("f",SH)






player1 = Player("j1",strat)
player2 = Player("j2",st)


team1m=SoccerTeam("team1",[player1])
team2m=SoccerTeam("team2",[player2])
match=SoccerMatch(team1m,team1)

show(match)
strat.write("monfichier.exp")



#match=SoccerMatch(team1,team2)
#soccersimulator.show(match)

#tournoi = SoccerTournament(1)
#tournoi.add_team(team1)
#tournoi.add_team(team2)

#tournoi.play()
#soccersimulator.show(tournoi)
