import numpy as np

from GamePlay import GamePlay




'''
Below is a class specifically for the robots. I wanted to separate this out
from the actual game rules and play in an effort to stay organized. There
will be another class that takes the gameplay and the robots classes
together to make the game happen/playable.

Robots:
First_Move_bot - > returns the first available move.
MiniMax -> does the minimax algorithm to find the best move.
MiniMaxAlphaBeta -> does the minimax algorithm with alphabeta pruning to find the best move.

Code names:
FmoveBot, Rando, MiniMax, AlphaBeta

'''
#mymodel_30794

#class for my Robots
class Robots():

    def __init__(self,p1='HUMAN',p2='HUMAN',gameplay=GamePlay(),depth=3,name='mymodel_5000.h5'):
        self.depth = depth
        self.p1=p1
        self.p2=p2
        self.gameplay = gameplay
        self.name=name
        #self.model=self.load_model(name)

#There is a function below that controls all of these bad boys.

#only return the first action available
    def First_Move_bot(self,BOARD):
        actions = self.gameplay.Get_Legal_Moves(BOARD)
        return actions[0]

#randomly chose an action for legal moves
    def Rando_bot(self,BOARD):
        actions = self.gameplay.Get_Legal_Moves(BOARD)
        return np.random.choice(actions,1)

#function to load the model
    def load_model(self, file=None):
        from tensorflow.keras.models import load_model
        if file==None:
            self.model = load_model(self.name)
        else:
            self.model = load_model(file)

    def DNN_bot(self,BOARD):
        state=np.expand_dims(np.expand_dims(BOARD, axis=3),axis=0)
        #pred=self.model.predict(state)
        #legal=self.gameplay.Get_Legal_Moves(BOARD)
        return np.argmax(self.model.predict(state))

    #minimax agent
    def MiniMax(self,state, depth,player, maximizingPlayer=True):
        if depth == 0 or self.gameplay.Check_Goal(state) !='Keep Playing!':
            if player==1:    score=self.gameplay.Get_Score(1,state)-self.gameplay.Get_Score(2,state)
            if player==2:    score=self.gameplay.Get_Score(2,state)-self.gameplay.Get_Score(1,state)
            return score
        if maximizingPlayer:
            return self.getMax(state,depth-1,player,maximizingPlayer)
        else:
            return self.getMin(state,depth-1,player,maximizingPlayer)

    def getMax(self,state,depth,player,maximizingPlayer):
        actions = self.gameplay.Get_Legal_Moves(state)
        out=['placeholder',float('-inf')]
        for action in actions:
            board=state.copy()
            child = self.gameplay.Add_Piece(player,action,board)
            val = self.MiniMax(child,depth,player,False) # next turn is the minimizer
            if type(val)==list:
                val=val[1]
            if val > out[1]: #if value is greater, than replace output with this value/action
                out[0]=action
                out[1]=val
        return out

    def getMin(self,state,depth,player,maximizingPlayer):
        actions = self.gameplay.Get_Legal_Moves(state)
        out=['placeholder',float('inf')]
        for action in actions:
            board=state.copy()
            if player == 1: ##other player's turn
                p=2
            else:
                p=1
            child = self.gameplay.Add_Piece(p,action,board)
            val = self.MiniMax(child,depth,player,True) # next turn is the maximizer
            if type(val)==list:
                val=val[1]
            if val < out[1]: #if value is smaller, than replace output with this value/action
                out[0]=action
                out[1]=val
        return out

    def MiniMax_bot(self,state,player):
        try:
            return self.MiniMax(state,self.depth,player,True)[0]
        except:
            return self.MiniMax(state,self.depth,player,True)

    def MiniMaxAlphaBeta(self,state, depth,player,alpha,beta, maximizingPlayer=True):
        if depth == 0 or self.gameplay.Check_Goal(state) !='Keep Playing!':
            if player==1:    score=self.gameplay.Get_Score(1,state)-self.gameplay.Get_Score(2,state)
            if player==2:    score=self.gameplay.Get_Score(2,state)-self.gameplay.Get_Score(1,state)
            return score
        if maximizingPlayer:
            return self.getMaxAlphaBeta(state,depth-1,player,alpha,beta, maximizingPlayer)
        else:
            return self.getMinAlphaBeta(state,depth-1,player,alpha,beta, maximizingPlayer)

    def getMaxAlphaBeta(self,state,depth,player,alpha,beta, maximizingPlayer):
        actions = self.gameplay.Get_Legal_Moves(state)
        out=['placeholder',float('-inf')]
        for action in actions:
            board=state.copy()
            child = self.gameplay.Add_Piece(player,action,board)
            val = self.MiniMaxAlphaBeta(child,depth,player,alpha,beta,False) # next turn is the minimizer
            if type(val)==list:
                val=val[1]
            if val > out[1]: #if value is greater, than replace output with this value/action
                out[0]=action
                out[1]=val
            #alphabeta portion of code:
            if val > beta:
                return [action, val]
            alpha =max(alpha,val)
        return out

    def getMinAlphaBeta(self,state,depth,player,alpha,beta,maximizingPlayer):
        actions = self.gameplay.Get_Legal_Moves(state)
        out=['placeholder',float('inf')]
        for action in actions:
            board=state.copy()
            if player == 1: ##other player's turn
                p=2
            else:
                p=1
            child = self.gameplay.Add_Piece(p,action,board)
            val = self.MiniMaxAlphaBeta(child,depth,player,alpha,beta,True) # next turn is the maximizer
            if type(val)==list:
                val=val[1]
            if val < out[1]: #if value is smaller, than replace output with this value/action
                out[0]=action
                out[1]=val
            #alphabeta portion of code:
            if val < alpha:
                return [action, val]
            beta = min(beta,val)
        return out

    def MiniMaxAlphaBeta_bot(self,state,player):
        return self.MiniMaxAlphaBeta(state,self.depth,player,-float("inf"),float("inf"),True)[0]

    #used to control the robot being used
    def ROBOT(self,player,bottype,BOARD):
        if bottype=='FmoveBot':
            return self.First_Move_bot(BOARD)
        if bottype=='Rando':
            return self.Rando_bot(BOARD)
        if bottype=='MiniMax':
            return self.MiniMax_bot(BOARD,player)
        if bottype=='AlphaBeta':
            return self.MiniMaxAlphaBeta_bot(BOARD,player)
        if bottype=='DNN':
            return self.DNN_bot(BOARD)
