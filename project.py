# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.

class terrain(object):
    def __init__(self,x,y):
        self.x = 0
        self.y = 0
    def get_max(self):
        return self.x; self.y

class agent(object):
    def __init__(self,nom):
        self.nom=nom
        self.x = 0
        self.y = 0
    def agir(self,etat):
        action = None
        return action
    def get_position(self):
        return self.x; self.y
    def safficher(self):
        print("Je suis %s en %d, %d"%(self.nom,self.x,self.y))
        
        
class ballon(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def get_position(self):
        returnself.x; self.y
        
class equipe(object):
    def __init__(self,nom):
         self.nom=nom
         self.l=[]
    def ajouter_agent(ag):
        self.l.append(ag)
        
"""

import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament

class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(),
                            Vector2D.create_random())

class FoncerStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Foncer")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random(),
                            Vector2D.create_random())



team1=SoccerTeam("team1",[Player("t1j1",FoncerStrategy())])
team2=SoccerTeam("team2",[Player("t2j2",FoncerStrategy())])
team3=SoccerTeam("team3",[Player("t3j3",FoncerStrategy())])
match=SoccerMatch(team1,team2)
match.play()
soccersimulator.show(match)

tournoi = SoccerTournament(1)
tournoi.add_team(team1)
tournoi.add_team(team2)
tournoi.add_team(team3)

tournoi.play()
soccersimulator.show(tournoi)

