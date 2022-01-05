from Board import *
from Game import *
from ChessBots import *
from EvaluatorBots import *
from NeuralNetworkTournament import *
from KylesWeightings import *


#random.seed(2)
#FindingEloOfABot(KylesWeighting())
#EternalTournament(CulledListOfBots())
EternalNeuralNetworkTournament(AIPerGen = 20,NumberOfGamesPerMatch = 3,NumberOfMatches=5)
#EternalTournamentWithAI(CulledListOfBots())
#EternalSmallSavedTournament(ListOfPlayers =  [WarmongerBot(BountyHunter),WarmongerBot(Bully),KylesWeighting()] ,NumberOfGamesPerMatch = 3)
#DisplayGame(PawnPusher(),ChampionBot(),0.5)
