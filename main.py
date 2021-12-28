from Board import *
from Game import *
from ChessBots import *
from EvaluatorBots import *
from NeuralNetworkTournament import *
from KylesWeightings import *

random.seed(2)
DisplayGame(KylesWeighting(),BasicBot())
#FindingEloOfABot(KylesWeighting())
EternalTournament(CulledListOfBots())
#EternalNeuralNetworkTournament()
