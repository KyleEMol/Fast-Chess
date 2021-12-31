from Board import *
from Game import *
from ChessBots import *
from EvaluatorBots import *
from NeuralNetworkTournament import *
from KylesWeightings import *

#random.seed(2)
#FindingEloOfABot(KylesWeighting())
#EternalTournament(CulledListOfBots())
EternalNeuralNetworkTournament(AIPerGen = 20)
#EternalTournamentWithAI(CulledListOfBots())
