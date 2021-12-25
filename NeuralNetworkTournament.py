from Game import *
from NeuralNetworkPlayer import *

def EternalNeuralNetworkTournament(AIPerGen=20,NumberOfGamesPerMatch = 2,NumberOfMatches = 3):
    
    ListOfHardCodedBots = GettingBotEloForList([WarmongerBot(BountyHunter),BishopBudger(BountyHunter),WarmongerBot(ComparingCollectorBot),NoFilter(BountyHunter),BasicBot()])
    
    try:
        with open('ListOfAIDict', 'rb') as f:
            ListOfAI = pickle.read(f)
    except FileNotFoundError:
        ListOfAI = []    

    NumberOfRounds = 0
    NumberOfAI = 0

    try :
        with open('AITournamentResults.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')

            for row in reader:
                if len(row) == 0:continue
                
                if row[0] == "NumberOfRounds":
                    NumberOfRounds = int(row[1])
                if row[0] == "NumberOfAI":
                    NumberOfAI = int(row[1])
                    break

    except FileNotFoundError:
        NumberOfAI = 0
        NumberOfRounds = 0

    if len(ListOfAI) == 0:
        for _ in range(AIPerGen):
            ListOfAI.append(NeuralNetworkPlayer(Name = "NeuralNetwork" + str(NumberOfAI)))
            NumberOfAI += 1 

    elif len(ListOfAI) < AIPerGen:
        original = ListOfAI[:]
        while len(ListOfAI) < AIPerGen:
            NewAI = random.choice(original).Evolve()
            NewAI.Name = "NeuralNetwork" + str(NumberOfAI)
            ListOfAI.append()
            NumberOfAI += 1 

    ListOfPlayers = ListOfAI + ListOfHardCodedBots[:]

    while True:
        while len(ListOfAI) < AIPerGen:
            NewAI = random.choice(original).Evolve()
            NewAI.Name = "NeuralNetwork" + str(NumberOfAI)
            ListOfAI.append()
            NumberOfAI += 1 
        
        ListOfPlayers = ListOfAI + ListOfHardCodedBots[:]

        for _ in range(NumberOfMatches):
            for Player1 in ListOfPlayers:
                Player2 = random.choice(ListOfPlayers)
                for _ in range(NumberOfGamesPerMatch):
                    RatedGame(Player1, Player2)

        NumberOfRounds += 1
        print(f"Round Number : {NumberOfRounds}")
        ListOfAI.sort(key=(lambda x:x.Rating), reverse=True)
        ListOfAI = ListOfAI[:6]
        DictOfAI = {Player.Name:Player.Rating for Player in ListOfAI}
        DictOfAI["NumberOfRounds"] = NumberOfRounds
        
        with open('ListOfAI', 'wb') as f:
            pickle.dump(ListOfAI,f)

        with open('AITournamentResults.csv', "w") as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName","PlayerRating"])
            writer.writerow(["NumberOfRounds",NumberOfRounds])
            writer.writerow(["NumberOfAI",NumberOfAI])
            for Player in ListOfAI:
                writer.writerow([Player.Name,Player.Rating])
