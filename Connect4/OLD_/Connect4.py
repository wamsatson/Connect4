import numpy as np
import os
from time import sleep



#class that creates the connect4 environment
class Connect4():

    def __init__(self,p1='HUMAN',p2='HUMAN',ROWS=6,COLUMNS=7,CONNECT=4):
        self.p1=p1
        self.p2=p2
        self.ROWS = ROWS
        self.COLUMNS = COLUMNS
        self.CONNECT = CONNECT
        self.BOARD = np.zeros((ROWS,COLUMNS))
        self.prev = np.zeros((ROWS,COLUMNS))

    def Add_Piece(self,PLAYER,spot,BOARD):
        self.prev2 = self.prev.copy()
        self.prev = self.BOARD.copy()
        #check if valid move
        if spot>=self.COLUMNS or BOARD[:, spot][0] !=0:
            print('invalid move')
            return BOARD
        #getting column in reverse order
        col = BOARD[:, spot][::-1]
        #find the first value not filled and fill it
        for i in range(len(col)):
            if col[i] ==0:
                col[i]=PLAYER
                break
        BOARD[:, spot] = col[::-1]
        return BOARD

    def undo(self):
        self.BOARD = self.prev.copy()

    def undo2(self):
        self.BOARD = self.prev2.copy()


    #helper function to get score of the Board
    def Get_Row_Score(self,row,p):
        score=0
        max_combo = 0
        for i in range(len(row)):
            #print(i)
            window=row[i:i+self.CONNECT]
            if len(window)<self.CONNECT:
                continue
            win_combo=0
            #checking for possible places to score for the player
            for cell in window:
                if cell==0:
                    continue
                elif cell!=p:
                    win_combo=0
                    break
                elif cell==p:
                    win_combo +=1
            score += win_combo/self.CONNECT
            if win_combo>max_combo:
                max_combo=win_combo
        return max_combo,score*100

    #helper function
    #return a list of all possible places where there can be a conenct4
    def Get_Rows(self,BOARD):
        #GETTING DIAGONALS:
        diagonals1=[]
        diagonals2=[]
        for i in range(-self.COLUMNS,self.COLUMNS):
            d1=BOARD.diagonal(i)
            d2=np.fliplr(BOARD).diagonal(i)
            if len(d1)>=self.CONNECT:
                diagonals1.append(d1)
            if len(d2)>=self.CONNECT:
                diagonals2.append(d2)
        #GETTING ROWS
        rows=[]
        for i in range(BOARD.shape[1]):
            rows.append((BOARD[::,i]))
        #GETTING COLUMNS
        cols=[]
        for i in range(BOARD.shape[0]):
            cols.append(BOARD[i])
        #RETURN ERTHANG
        return diagonals1+diagonals2+rows+cols

    #outputs the score of the Board for a given player
    def Get_Score(self,p,BOARD):
        rows = self.Get_Rows(BOARD)
        score = 0
        max_combo = 0
        for row in rows:
            check_max,check_score = self.Get_Row_Score(row,p)
            score += check_score
        if self.Check_Goal(BOARD)=='TIE':
            score=1000
        if self.Check_Goal(BOARD)=='Player 1 wins!':
            if p==1:    score = 5000
            if p==2:    score = -5000
        if self.Check_Goal(BOARD)=='Player 2 wins!':
            if p==1:    score = -5000
            if p==2:    score = 5000
        return score

    #outputs the highest combination for a given player
    def Get_Max_Combo(self,p,BOARD):
        rows = self.Get_Rows(BOARD)
        score = 0
        max_combo = 0
        for row in rows:
            check_max,check_score = self.Get_Row_Score(row,p)
            if check_max>max_combo:
                max_combo=check_max
        return max_combo

    #checks if goal state or not
    def Check_Goal(self,BOARD):
        p1max=self.Get_Max_Combo(1,BOARD)
        p2max=self.Get_Max_Combo(2,BOARD)
        if p1max>=self.CONNECT:
            return 'Player 1 wins!'
        if p2max>=self.CONNECT:
            return 'Player 2 wins!'
        if 0 not in BOARD[0]:
            return 'TIE'
        else:
            return 'Keep Playing!'

    #get the legal moves
    def Get_Legal_Moves(self,BOARD):
        moves=[]
        toprow=BOARD[0]
        for i in range(len(toprow)):
            if toprow[i]==0:
                moves.append(int(i))
        return moves

    def Display_BOARD(self,turn,BOARD):
        os.system('cls')
        print('Play Connect 4!')
        print('Player 1 Score: {}. Player 2 Score: {}'.format(self.Get_Score(1,BOARD),self.Get_Score(2,BOARD)))
        print("Player {}'s turn!".format((turn % 2)+1))
        print('Legal Moves:')
        print(self.Get_Legal_Moves(BOARD))
        print('')
        for row in BOARD:
            print(row)

#----------------------------------------------------
#----------------------------------------------------
#----MY ROBOTS!!
#----------------------------------------------------
#----------------------------------------------------
#There is a function below that controls all of these bad boys.
    def First_Move_bot(self,BOARD):
        actions = self.Get_Legal_Moves(BOARD)
        return actions[0]

    #minimax agent
    def MiniMax(self,state, depth,player, maximizingPlayer=True):
        if depth == 0 or self.Check_Goal(state) !='Keep Playing!':
            if player==1:    score=self.Get_Score(1,state)-self.Get_Score(2,state)
            if player==2:    score=self.Get_Score(2,state)-self.Get_Score(1,state)
            return score
        if maximizingPlayer:
            return self.getMax(state,depth-1,player,maximizingPlayer)
        else:
            return self.getMin(state,depth-1,player,maximizingPlayer)

    def getMax(self,state,depth,player,maximizingPlayer):
        actions = self.Get_Legal_Moves(state)
        out=['placeholder',float('-inf')]
        for action in actions:
            board=state.copy()
            child = self.Add_Piece(player,action,board)
            val = self.MiniMax(child,depth,player,False) # next turn is the minimizer
            if type(val)==list:
                val=val[1]
            if val > out[1]: #if value is greater, than replace output with this value/action
                out[0]=action
                out[1]=val
        return out

    def getMin(self,state,depth,player,maximizingPlayer):
        actions = self.Get_Legal_Moves(state)
        out=['placeholder',float('inf')]
        for action in actions:
            board=state.copy()
            if player == 1: ##other player's turn
                p=2
            else:
                p=1
            child = self.Add_Piece(p,action,board)
            val = self.MiniMax(child,depth,player,True) # next turn is the maximizer
            if type(val)==list:
                val=val[1]
            if val < out[1]: #if value is smaller, than replace output with this value/action
                out[0]=action
                out[1]=val
        return out

    def Get_MiniMax(self,state,player):
        return self.MiniMax(state,4,player,True)[0]


    def MiniMaxAlphaBeta(self,state, depth,player,alpha,beta, maximizingPlayer=True):
        if depth == 0 or self.Check_Goal(state) !='Keep Playing!':
            if player==1:    score=self.Get_Score(1,state)-self.Get_Score(2,state)
            if player==2:    score=self.Get_Score(2,state)-self.Get_Score(1,state)
            return score
        if maximizingPlayer:
            return self.getMaxAlphaBeta(state,depth-1,player,alpha,beta, maximizingPlayer)
        else:
            return self.getMinAlphaBeta(state,depth-1,player,alpha,beta, maximizingPlayer)

    def getMaxAlphaBeta(self,state,depth,player,alpha,beta, maximizingPlayer):
        actions = self.Get_Legal_Moves(state)
        out=['placeholder',float('-inf')]
        for action in actions:
            board=state.copy()
            child = self.Add_Piece(player,action,board)
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
        actions = self.Get_Legal_Moves(state)
        out=['placeholder',float('inf')]
        for action in actions:
            board=state.copy()
            if player == 1: ##other player's turn
                p=2
            else:
                p=1
            child = self.Add_Piece(p,action,board)
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

    def Get_MiniMaxAlphaBeta(self,state,player):
        return self.MiniMaxAlphaBeta(state,4,player,-float("inf"),float("inf"),True)[0]



    #used to control the robot being used
    def ROBOT(self,player,bottype,BOARD):
        if bottype=='FmoveBot':
            return self.First_Move_bot(BOARD)
        if bottype=='MiniMax':
            return self.Get_MiniMax(BOARD,player)
        if bottype=='AlphaBeta':
            return self.Get_MiniMaxAlphaBeta(BOARD,player)

#Function to play the game in CMD

    def play(self):
        turn = 0
        status=self.Check_Goal(self.BOARD)
        self.Display_BOARD(turn,self.BOARD)
        while status == 'Keep Playing!':
            actions = self.Get_Legal_Moves(self.BOARD)
            print('')
            if turn % 2 ==0:
                if self.p1 !='HUMAN': #if it's not a human do the robot moves
                    m = self.ROBOT(1,self.p1,self.BOARD)
                else:
                    m = input('Where would you like to go? ')
                try:
                    self.Add_Piece(1,int(m),self.BOARD)
                except:
                    print('Invalid Move')
            elif turn % 2 ==1:
                if self.p2 !='HUMAN':
                    m = self.ROBOT(2,self.p2,self.BOARD)
                else:
                    m = input('Where would you like to go? ')
                try:
                    self.Add_Piece(2,int(m),self.BOARD)
                except:
                    print('Invalid Move')

            turn +=1
            self.Display_BOARD(turn,self.BOARD)
            status=self.Check_Goal(self.BOARD)
        print(status)



if __name__=="__main__":
    game=Connect4()
    game.p2='MiniMax'
    game.play()
