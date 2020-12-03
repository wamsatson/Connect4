
import numpy as np

'''
Class that builds the structure of the connect4 game. it builds the board,
and has functions that let you get scores, get legal moves,
add a piece, and check if it is a goal state
'''

#class that creates the connect4 environment
class GamePlay():

    def __init__(self,ROWS=6,COLUMNS=7,CONNECT=4):
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
            #print('invalid move')
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

    def reset(self):
        self.BOARD = np.zeros((self.ROWS,self.COLUMNS))
        self.prev = np.zeros((self.ROWS,self.COLUMNS))


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
        return max_combo,score

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
            score=10
        if self.Check_Goal(BOARD)=='Player 1 wins!':
            if p==1:    score = 50
            if p==2:    score = -50
        if self.Check_Goal(BOARD)=='Player 2 wins!':
            if p==1:    score = -50
            if p==2:    score = 50
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

    def get_reward(self,p,BOARD):
        status = self.Check_Goal(BOARD)
        if status == 'Keep Playing!':
            if p==1:
                return self.Get_Score(1,BOARD)-self.Get_Score(2,BOARD)
            if p==2:
                return self.Get_Score(2,BOARD)-self.Get_Score(1,BOARD)
        else:
            return self.Get_Score(p,BOARD)


    #get the legal moves
    def Get_Legal_Moves(self,BOARD):
        moves=[]
        toprow=BOARD[0]
        for i in range(len(toprow)):
            if toprow[i]==0:
                moves.append(int(i))
        return moves
