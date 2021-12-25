from typing import Tuple
import numpy as np
import math
from ChessBots import *
from Board import *

"""
Inputs:
Number of each unique piece (6*2)

X - Number Of Legal King Moves (2)

X - Number Of LegalMoves (2)

X - Own Pieces Being Attacked (6)

X -Opponent Pieces Being Attacked (6)

"""

def ActivationFunction(x):
    sig = 1 - 2*(1/(1+np.exp(x)))
    return sig

def RandomMatrix(Layout = tuple or list,Min = int,Max=int):
    Range = Max-Min
    NewMatrix = []
    for _ in range(Layout[0]):
        Matrix = np.random.rand(Layout[1])
        NewMatrix.append(np.array(list(map((lambda x: Min + Range*x),Matrix))))
    
    return np.array(NewMatrix)

class NeuralNetwork():
    def __init__(self,Layout = [12,24,48,48,24,1]):
        self.Layout = Layout
        self.Weights = [RandomMatrix((Layout[i-1],Layout[i]),-1,1) for i in range(1,len(self.Layout))]
        self.PreviousChanges = [np.zeros((Layout[i-1],Layout[i])) for i in range(1,len(self.Layout))]
        self.BiasList = [random.random() for _ in range(len(Layout)-1)]


    def Output(self,InputLayer):
        CurrentLayer = np.matrix(InputLayer)

        for Weight,Bias in zip(self.Weights,self.BiasList):
            CurrentLayer = np.dot(CurrentLayer,Weight)

            for i in range(len(CurrentLayer)):
                CurrentLayer[i] = ActivationFunction(CurrentLayer[i]+Bias)
            
        return CurrentLayer

    def MakingAnEvolvedNetwork(self):
        NewNetwork = NeuralNetwork(self.Layout)
        NewNetwork.PreviousChanges = []
        NewNetwork.Weights = []

        Changes = [RandomMatrix((self.Layout[i-1],self.Layout[i]),-1,1) for i in range(1,len(self.Layout))]

        for i in range(len(self.Layout)-1):

            Changes[i] += self.PreviousChanges[i]

            Changes[i] = list(map(ActivationFunction,Changes[i]))
            NewNetwork.PreviousChanges.append(Changes[i])
            Changes[i] += self.Weights[i]
            NewNetwork.Weights.append(Changes[i])

        return NewNetwork
        