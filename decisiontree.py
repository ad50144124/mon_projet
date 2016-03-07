from soccersimulator import SoccerMatch, SoccerTournament,KeyboardStrategy
from soccersimulator import SoccerTeam, Player, show
from strategies import RandomStrategy,FonceurStrategy,DefenseStrategy
from soccersimulator import settings, Vector2D,DecisionTreeClassifier
from soccersimulator import export_graphviz
import cPickle
from decorator import *
from strategy import *
import sys
"""
strat_key = KeyboardStrategy()
strat_key.add("a",RandomStrategy())
strat_key.add("z",FonceurStrategy())
strat_key.add("e",DefenseStrategy())

team_noob = SoccerTeam("keyb",[Player("KBs", strat_key),Player("Defense",DefenseStrategy())])
team_bad = SoccerTeam("foncteam",[Player("Fonceur",FonceurStrategy()),Player("Defense", DefenseStrategy())])
"""

## Fonction de generation de descripteurs
def gen_features(state,idteam,idplayer):
    mystate = SoccerStateDecorator(state,idteam,idplayer,None)
    
    e_t = 3 - mystate.id_team
    #enemy team (int)
        
    b_p = mystate.state.ball.position
    #ball position (vector)
    b_v =mystate.state.ball.vitesse
    #ball vitesse (vector) 
    
    p = mystate.p
    #position player (vector)
    d = mystate.d
    #distance player to ball (float)  
    d_vec = mystate.d_vec
    #distance player to ball (vector)
    goal = mystate.goal
    #position goal (vector)
    
    e_p = mystate.state.player(e_t,mystate.id_player).position
    #position enemie (vector)
    e_d = (b_p-e_p).norm
    #distance enemie player to ball (float)
    e_d_vec = b_p-e_p
    #distance enemie player to ball (vector)
    e_goal = Vector2D(150-(e_t-1)*150,45)
    #goal enemie (vector)
    return [d, e_d, b_v.norm, (goal-p).norm, (goal-e_p).norm, (e_goal-p).norm, (e_goal-e_p).norm, abs(p.y-45), (e_p-p).norm]
    
gen_features.names = ["distance","e_distance","b_v.norm","(goal-p).norm","(goal-e_p).norm","(e_goal-p).norm","(e_goal-e_p).norm","abs(p.y-45)","(e_p-p).norm"]


def build_apprentissage(fn,generator):
    ex_raw = KeyboardStrategy.read(fn)
    exemples = []
    labels = []
    for x in ex_raw:
        exemples.append(generator(x[1],x[0][0],x[0][1]))
        labels.append(x[0][2])
    return exemples,labels

def apprendre_arbre(train,labels,depth=5,min_samples_leaf=2,min_samples_split=2):
    tree= DecisionTreeClassifier(max_depth=depth,min_samples_leaf=min_samples_leaf,min_samples_split=min_samples_split)
    tree.fit(train,labels)
    return tree

def affiche_arbre(tree):
    long = 10
    sep1="|"+"-"*(long-1)
    sepl="|"+" "*(long-1)
    sepr=" "*long
    def aux(node,sep):
        if tree.tree_.children_left[node]<0:
            ls ="(%s)" % (", ".join( "%s: %d" %(tree.classes_[i],int(x)) for i,x in enumerate(tree.tree_.value[node].flat)))
            return sep+sep1+"%s\n" % (ls,)
        return (sep+sep1+"X%d<=%0.2f\n"+"%s"+sep+sep1+"X%d>%0.2f\n"+"%s" )% \
                (tree.tree_.feature[node],tree.tree_.threshold[node],aux(tree.tree_.children_left[node],sep+sepl),
                tree.tree_.feature[node],tree.tree_.threshold[node],aux(tree.tree_.children_right[node],sep+sepr))
    return aux(0,"")



exemples = KeyboardStrategy.read("./monfichier.exp")
train,labels = build_apprentissage("./monfichier.exp",gen_features)
tree = apprendre_arbre(train,labels)
print(affiche_arbre(tree))


if __name__=="__main__":
    prefix = "./test"
    if len(sys.argv)>1:
        prefix = sys.argv[1]
    ## constitution de la base d'entrainement et des labels
    train,labels = build_apprentissage(prefix+".exp",gen_features)
    ## apprentissage de l'arbre
    tree = apprendre_arbre(train,labels)
    ## sauvegarde de l'arbre
    cPickle.dump(tree,file(prefix+".pkl","w"))
    ## exporter l'arbre en .dot
    with file(prefix+".dot","w") as fn:
        export_graphviz(tree,fn,class_names = tree.classes_,feature_names=getattr(gen_features,"names",None),
                        filled = True,rounded=True)





