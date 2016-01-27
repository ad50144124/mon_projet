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

class FoncerStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Foncer")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction((state.ball.position-state.player(1,0).position),
                            Vector2D(150,45)-state.ball.position)

class Strategy1(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Foncer")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction((state.ball.position-state.player(2,0).position),
                            Vector2D(0,45)-state.ball.position)


team1=SoccerTeam("team1",[Player("t1j1",FoncerStrategy())])
team2=SoccerTeam("team2",[Player("t2j2",Strategy1())])
match=SoccerMatch(team1,team2)
match.play()
soccersimulator.show(match)

tournoi = SoccerTournament(1)
tournoi.add_team(team1)
tournoi.add_team(team2)

tournoi.play()
soccersimulator.show(tournoi)
