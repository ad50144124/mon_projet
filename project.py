# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.

"""

import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament

class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(Vector2D.create_random()-0.5,
                            Vector2D.create_random())
"""
==========================1V1=====================================
"""
class FoncerStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Foncer")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction((state.ball.position-state.player(id_team,id_player).position),
                            Vector2D(150,45)-state.ball.position)

class QuickCatchStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Foncer")
    def compute_strategy(self,state,id_team,id_player):
        d=state.ball.position-state.player(id_team,id_player).position
        #print state.ball.position-state.player(2,0).position
        if state.ball.vitesse._x==0 and ((d.x**2+d.y**2)**(1/2))<1:
            d.scale(0.009)
        return SoccerAction(d,
                            Vector2D(0,45)-state.ball.position)
"""
=========================2V2=======================================
"""                            
class QuickCatchStrategy2v2(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Foncer")
    def compute_strategy(self,state,id_team,id_player):
        d=state.ball.position-state.player(id_team,id_player).position
        #print state.ball.position-state.player(2,0).position
        if state.ball.vitesse._x<0.1 and ((d.x**2+d.y**2)**(1/2))<0:
            d.scale(0.09)
        #print state.ball.vitesse
        return SoccerAction(d,
                            Vector2D(0,45)-state.ball.position)
                            
class QuickFollowStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Foncer")
    def compute_strategy(self,state,id_team,id_player):
        d=state.ball.position-state.player(id_team,id_player).position
        #print state.ball.position-state.player(2,0).position
        if ((d.x**2+d.y**2)**(1/2))>5 and state.ball.vitesse._x<1:
            d+=Vector2D(-50,20)
        elif state.ball.vitesse._x!=0 or state.ball.vitesse._y!=0 :
            v=(state.ball.vitesse.x**2+state.ball.vitesse.y**2)**(1/2)
            p=0
            while(v>=0.00001):
                p+=v
                v-=v*0.06-(v**2)*0.01
                #print v
            v=(state.ball.vitesse.x**2+state.ball.vitesse.y**2)**(1/2)
            vb=state.ball.vitesse 
            vb.scale(p/v)
            d+=vb
        elif (d.x**2+d.y**2)**(1/2)<1:
            d.scale(0.09)
        return SoccerAction(d,
                            Vector2D(0,45)-state.ball.position)
                            
    

"""
============================main===================================
"""

#team1=SoccerTeam("team1",[Player("t1j1",RandomStrategy())])
#team2=SoccerTeam("team2",[Player("t2j1",QuickCatchStrategy2v2())])
team1=SoccerTeam("team1",[Player("t1j1",RandomStrategy()),Player("t1j2",RandomStrategy())])
team2=SoccerTeam("team2",[Player("t2j1",QuickCatchStrategy2v2()),Player("t2j2",RandomStrategy())])
match=SoccerMatch(team1,team2)
match.play()
soccersimulator.show(match)

tournoi = SoccerTournament(1)
tournoi.add_team(team1)
tournoi.add_team(team2)

tournoi.play()
soccersimulator.show(tournoi)

