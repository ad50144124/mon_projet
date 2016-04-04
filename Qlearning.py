# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:20:48 2016

@author: 3407585
"""

import soccersimulator,soccersimulator.settings
from decorator import *
from strategy import *
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import KeyboardStrategy,show
import numpy as np


class st_state:
    def __init__(self,mystate):
        self.m=mystate
    
    @property
    def distance_a_la_ball(self):#int [1;3]
        d=self.m.state.ball.position.distance(self.m.p)
        if d<2:
            return 1
        elif d<10:
            return 2
        else:
            return 3
        
    @property
    def distance_a_enemie_plus_proche(self):#int [1;3]
        etid=3-self.m.id_team
        nb=self.m.state.nb_players(etid)
        d=inf
        for i in range nb:
            if d>self.m.state.player_state(etid,i).position.distance(self.m.p):
                d=self.m.state.player_state(etid,i).position.distance(self.m.p)
        if d<2:
            return 1
        elif d<10 :
            return 2
        else:
            return 3
            
    @property
    def distance_a_goal(self):#int [1;2]
        d=self.m.goal.distance(self.m.p)
        if d<20:
            return 1
        else:
            return 2
            
    @property
    def vitesse_ball(self):
        v=self.m.v_b.norm
        if v<1.5:
            return 1
        else:
            return 2

    @property
    def angle_ball_moi_et_moi_goal(self):
        a=(self.m.b_p-self.m.p).angle-(self.m.goal-self.m.p).angle
        if abs(a)<(pi/3):
            return 1
        elif abs(a)<(2pi/3):
            return 2
        else:
            return 3
        
            


def evaluer(m,st,tab):#SoccerStateDecorator,strategy,tableau-> string
    etat = [m.distance_a_la_ball,
            m.distance_a_enemie_plus_proche, 
            m.distance_a_goal, 
            m.vitesse_ball, 
            m.angle_ball_moi_et_moi_goal]    
    
    if type(tab[m.distance_a_la_ball][m.distance_a_enemie_plus_proche][m.distance_a_goal][m.vitesse_ball][m.angle_ball_moi_et_moi_goal])    
    
    
    