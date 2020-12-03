import numpy as np
import os
import math
import pygame

from time import sleep
from Robots import Robots
from GamePlay import GamePlay


#class that creates the connect4 environment
class Connect4():

    def __init__(self,p1='HUMAN',p2='HUMAN',depth=3,spacing=100,controler=0):
        self.gameplay=GamePlay()
        self.bots = Robots()
        self.p1=p1
        self.p2=p2

        self.depth = depth
        self.bots.depth = self.depth

        self.ROWS = self.gameplay.ROWS
        self.COLUMNS = self.gameplay.COLUMNS
        self.CONNECT = self.gameplay.CONNECT
        self.BOARD = self.gameplay.BOARD
        self.prev = self.gameplay.prev

        #pygame shit
        self.spacing = spacing
        self.controler = controler
        self.windowx=self.COLUMNS*self.spacing+self.controler
        self.windowy=(self.ROWS+1)*spacing

        #colors for the board!
        self.BG_COLOR = (28, 170, 156)
        self.BLUE = (0,0,225)
        self.RED = (255, 0 ,50)
        self.YELLOW = (255,200,0)
        self.BLACK = (0, 0, 0)
        self.coffee_brown =((200,190,140))
        #dictionary to assign circle colors
        self.color_dict={0:self.BLACK,1: self.RED,2: self.YELLOW}

    def load_model(self,name=None):
        if name==None:
            self.bots.load_model()
        else:
            self.bots.load_model(name)

    def Set_Depth(self,depth):
        self.depth = depth
        self.bots.depth = depth

#display board!
    def Display_BOARD(self,turn,BOARD):
        os.system('cls')
        print('Play Connect 4!')
        print('Player 1 Score: {}. Player 2 Score: {}'.format(self.gameplay.Get_Score(1,BOARD),self.gameplay.Get_Score(2,BOARD)))
        print("Player {}'s turn!".format((turn % 2)+1))
        print('Legal Moves:')
        print(self.gameplay.Get_Legal_Moves(BOARD))
        print('')
        for row in BOARD:
            print(row)

#Function to play the game in CMD
    def play(self):
        turn = 0
        status=self.gameplay.Check_Goal(self.gameplay.BOARD)
        self.Display_BOARD(turn,self.gameplay.BOARD)
        while status == 'Keep Playing!':
            actions = self.gameplay.Get_Legal_Moves(self.gameplay.BOARD)
            print('')
            if turn % 2 ==0:
                if self.p1 !='HUMAN': #if it's not a human do the robot moves
                    m = self.bots.ROBOT(1,self.p1,self.gameplay.BOARD)
                else:
                    m = input('Where would you like to go? ')
                try:
                    self.gameplay.Add_Piece(1,int(m),self.gameplay.BOARD)
                    turn +=1
                except:
                    print('Invalid Move')
            elif turn % 2 ==1:
                if self.p2 !='HUMAN':
                    m = self.bots.ROBOT(2,self.p2,self.gameplay.BOARD)
                else:
                    m = input('Where would you like to go? ')
                try:
                    self.gameplay.Add_Piece(2,int(m),self.gameplay.BOARD)
                    turn +=1
                except:
                    print('Invalid Move')

            self.Display_BOARD(turn,self.gameplay.BOARD)
            status=self.gameplay.Check_Goal(self.gameplay.BOARD)
        print(status)

    #helper functions
    def Draw_Section(self,x,y,width,item):
        pygame.draw.rect(self.window,self.BLUE, [x,y,width,width])
        pygame.draw.circle(self.window, self.color_dict[item], (math.floor(x+width/2),
        math.floor(y+width/2)), math.floor(width/2)-3)

    def Draw_Board(self):
        for j,row in enumerate(self.gameplay.BOARD):
            for i,cell in enumerate(row):
                self.Draw_Section(self.spacing*i,self.spacing+self.spacing*j,self.spacing,cell)

    def Get_Col(self,x):
        floor=0
        ceiling = self.spacing
        for i in range(self.COLUMNS):
            if floor<x<ceiling:
                return i
            floor = floor + self.spacing
            ceiling = ceiling + self.spacing

#play with pygame
    def play_Graphics(self):
        self.window = pygame.display.set_mode((self.windowx,self.windowy))
        pygame.init()
        pygame.display.set_caption('Connect 4')
        self.window.fill(self.BG_COLOR)
        run = True
        turn = 0
        while run:
            status=self.gameplay.Check_Goal(self.gameplay.BOARD)
            actions = self.gameplay.Get_Legal_Moves(self.gameplay.BOARD)

            if turn % 2 ==0 and self.p1!='HUMAN':
                m = self.bots.ROBOT(1,self.p1,self.gameplay.BOARD)
                self.gameplay.Add_Piece(1,int(m),self.gameplay.BOARD)
                turn +=1
            if turn % 2 ==1 and self.p2!='HUMAN':
                m = self.bots.ROBOT(2,self.p2,self.gameplay.BOARD)
                self.gameplay.Add_Piece(2,int(m),self.gameplay.BOARD)
                turn +=1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if turn % 2 ==0 and self.p1 =='HUMAN':
                        m = self.Get_Col(mx)
                        try:
                            self.gameplay.Add_Piece(1,int(m),self.gameplay.BOARD)
                        except:
                            print('Invalid Move')
                    if turn % 2 ==1 and self.p2=='HUMAN':
                        m = self.Get_Col(mx)
                        try:
                            self.gameplay.Add_Piece(2,int(m),self.gameplay.BOARD)
                        except:
                            print('Invalid Move')
                    turn +=1
                    print('Player 1 Score: {}. Player 2 Score: {}'.format(self.gameplay.Get_Score(1,self.gameplay.BOARD),self.gameplay.Get_Score(2,self.gameplay.BOARD)))
            #self.gameplay.Display_BOARD(turn)
            status=self.gameplay.Check_Goal(self.gameplay.BOARD)
            self.Draw_Board()
            pygame.display.update()
            if status !='Keep Playing!':
                print(status)
                run = False


#FmoveBot, Rando, MiniMax, AlphaBeta
if __name__=="__main__":
    #from tensorflow.keras.models import Sequential, save_model, load_model
    game=Connect4()
    game.Set_Depth(4)
    game.p2='AlphaBeta'#'AlphaBeta'
    #game.p2='MiniMax'
    #game.load_model('mymodel_20000.h5')#'mymodel_30794.h5')
    #game.p1='DNN'
    #game.p2='Rando'
    #game.play()
    game.play_Graphics()
