from Robots import Robots
from GamePlay import GamePlay
from Connect4 import Connect4

game=Connect4()

game.Set_Depth(4)
game.p2='AlphaBeta'
game.play_Graphics()












'''
game.Set_Depth(4)
game.p2='AlphaBeta'
'''

#game.Set_Depth(3)
#game.p2='AlphaBeta'
#game.load_model('mymodel.h5')
#game.p1='DNN'
