from NeuralNetworkTournament import *

def UpdatingTheAI():
    with open('ListOfAI', 'rb') as f:
        ListOfAI = pickle.load(f)
    NewListOfAI = []

    for AI in ListOfAI:
        NewAI = NeuralNetworkPlayer(FilterBot = AI.FilterBot,Name = AI.Name)
        NewAI.NeuralNetwork = AI.NeuralNetwork
        NewAI.Rating = AI.Rating
        NewListOfAI.append(NewAI)

    with open('ListOfAI', 'wb') as f:
        pickle.dump(NewListOfAI,f)  

UpdatingTheAI()
