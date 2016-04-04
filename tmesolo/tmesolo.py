from soccersimulator import *
from strategies import *
import soccersimulator,soccersimulator.settings
from decorator import *
from strategy import *
from decisiontree import *
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import KeyboardStrategy,show

class PADState(SoccerState):
    """ Etat d'un tour du jeu. Contient la balle (MobileMixin), l'ensemble des configurations des joueurs, le score et
    le numero de l'etat.
    """
    def __init__(self, **kwargs):
        SoccerState.__init__(self,**kwargs)
        self.cur_score = 0

    def apply_actions(self, actions=None):
        sum_of_shoots = Vector2D()
        if actions:
            for k, c in self._configs.items():
                if k in actions:
                    act = actions[k].copy()
                    if k[0] == 1 and self.player_state(k[0],k[1]).vitesse.norm>0.01:
                        act.shoot = Vector2D()
                    sum_of_shoots += c.next(self.ball, act)
        self.ball.next(sum_of_shoots)
        self.step += 1
        dball = [(it,ip) for it,ip in self.players
                 if self.player_state(it,ip).position.distance(self.ball.position)<settings.BALL_RADIUS+settings.PLAYER_RADIUS]
        mines = [(it,ip) for it,ip in dball if it ==1 ]
        others = [(it,ip) for it,ip in dball if it==2 ]
        if len(others)==0 or len(mines)>0 or self.ball.vitesse.norm>1:
            self.cur_score += 1
        else:
            self._score[1]=max(self._score[1],self.cur_score)
            self.cur_score=0
            self._score[2]+=1
            self._winning_team = 2
        if self.ball.position.x < 0:
            self.ball.position.x = -self.ball.position.x
            self.ball.vitesse.x = -self.ball.vitesse.x
        if self.ball.position.y < 0:
            self.ball.position.y = -self.ball.position.y
            self.ball.vitesse.y = -self.ball.vitesse.y
        if self.ball.position.x > settings.GAME_WIDTH:
            self.ball.position.x = 2 * settings.GAME_WIDTH - self.ball.position.x
            self.ball.vitesse.x = -self.ball.vitesse.x
        if self.ball.position.y > settings.GAME_HEIGHT:
            self.ball.position.y = 2 * settings.GAME_HEIGHT - self.ball.position.y
            self.ball.vitesse.y = -self.ball.vitesse.y

    def reset_state(self, nb_players_1=0, nb_players_2=0):
        SoccerState.reset_state(self,nb_players_1,nb_players_2)
        self.ball = Ball.from_position(self.player(1,0).position.x,self.player(1,0).position.y)
        self.cur_score = 0

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

strat = KeyboardStrategy() #ou pour une sauvegarde automatique
#KeyboardStrategy(fn="monfichier.exp")
FS = StateLessStrategy(demarque2v1)
RF = StateLessStrategy(reflexion)
PA = StateLessStrategy(passage2v1)
RI = StateLessStrategy(rien)

strat.add("d",FS)
strat.add("q",RF)
strat.add("a",PA)
strat.add("r",RI)

player1 = Player("j1",strat)
player2 = Player("j2",strat)



team2= SoccerTeam("T1",[player1,Player("1",  StateLessStrategy(random))])
#team4= SoccerTeam("T1",[Player("1", PasseStrategy()),Player("2",PasseStrategy()),Player("3",PasseStrategy()),                             Player("4",PasseStrategy())])
team1 = SoccerTeam("T2",[Player("1", FonceurStrategy())])
#team3 = SoccerTeam("T2",[Player("1", FonceurStrategy()),Player("2", FonceurStrategy()),                         Player("3",FonceurStrategy())])
match = SoccerMatch(team2,team1,init_state=PADState.create_initial_state(2,1))
show(match)
#match = SoccerMatch(team4,team3,init_state=PADState.create_initial_state(4,3))
#show(match)