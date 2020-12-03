from Connect4 import Connect4
import numpy as np
import math
import pygame

#class Connect4_Board():
#game=Connect4()
#game.play()


class Play_Connect4():

    def __init__(self,game=Connect4(),spacing=100,controler=0):
        self.game=game
        self.spacing = spacing
        self.controler = controler
        self.windowx=self.game.COLUMNS*self.spacing+self.controler
        self.windowy=(game.ROWS+1)*spacing
        self.window = pygame.display.set_mode((self.windowx,self.windowy))

        #colors for the board!
        self.BG_COLOR = (28, 170, 156)
        self.BLUE = (0,0,225)
        self.RED = (255, 0 ,50)
        self.YELLOW = (255,200,0)
        self.BLACK = (0, 0, 0)
        self.coffee_brown =((200,190,140))
        #dictionary to assign circle colors
        self.color_dict={0:self.BLACK,1: self.RED,2: self.YELLOW}
        pygame.init()
        pygame.display.set_caption('Connect 4')
        self.window.fill(self.BG_COLOR)

    def Draw_Section(self,x,y,width,item):
        pygame.draw.rect(self.window,self.BLUE, [x,y,width,width])
        pygame.draw.circle(self.window, self.color_dict[item], (math.floor(x+width/2),
        math.floor(y+width/2)), math.floor(width/2)-3)

    def Draw_Board(self):
        for j,row in enumerate(self.game.BOARD):
            for i,cell in enumerate(row):
                self.Draw_Section(self.spacing*i,self.spacing+self.spacing*j,self.spacing,cell)

    def Get_Col(self,x):
        floor=0
        ceiling = self.spacing
        for i in range(self.game.COLUMNS):
            if floor<x<ceiling:
                return i
            floor = floor + self.spacing
            ceiling = ceiling + self.spacing

    def play(self):
        run = True
        turn = 0
        while run:
            status=self.game.Check_Goal(self.game.BOARD)
            actions = self.game.Get_Legal_Moves(self.game.BOARD)

            if turn % 2 ==0 and self.game.p1!='HUMAN':
                m = self.game.ROBOT(1,self.game.p1,self.game.BOARD)
                self.game.Add_Piece(1,int(m),self.game.BOARD)
                turn +=1
            if turn % 2 ==1 and self.game.p2!='HUMAN':
                m = self.game.ROBOT(2,self.game.p2,self.game.BOARD)
                self.game.Add_Piece(2,int(m),self.game.BOARD)
                turn +=1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if turn % 2 ==0 and self.game.p1=='HUMAN':
                        m = self.Get_Col(mx)
                        try:
                            self.game.Add_Piece(1,int(m),self.game.BOARD)
                        except:
                            print('Invalid Move')
                    if turn % 2 ==1 and self.game.p2=='HUMAN':
                        m = self.Get_Col(mx)
                        try:
                            self.game.Add_Piece(2,int(m),self.game.BOARD)
                        except:
                            print('Invalid Move')
                    turn +=1
                    print('Player 1 Score: {}. Player 2 Score: {}'.format(self.game.Get_Score(1,self.game.BOARD),self.game.Get_Score(2,self.game.BOARD)))
            #self.game.Display_BOARD(turn)
            status=self.game.Check_Goal(self.game.BOARD)
            self.Draw_Board()
            pygame.display.update()
            if status !='Keep Playing!':
                print(status)
                run = False
game=Connect4()
game.p2='AlphaBeta' #MiniMax,FmoveBot, AlphaBeta
g=Play_Connect4(game=game)
g.play()
