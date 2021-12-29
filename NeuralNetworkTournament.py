from Game import *
from NeuralNetworkPlayer import *
from KylesWeightings import *

def EternalNeuralNetworkTournament(AIPerGen=20,NumberOfGamesPerMatch = 2,NumberOfMatches = 3):
    
    #ListOfHardCodedBots = GettingBotEloForList([WarmongerBot(BountyHunter),BishopBudger(BountyHunter),WarmongerBot(ComparingCollectorBot),KylesWeighting(),BasicBot()])
    
    try:
        with open('ListOfAI', 'rb') as f:
            ListOfAI = pickle.load(f)
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
            ListOfAI.append(NewAI)
            NumberOfAI += 1 

    while True:
        Time = time.perf_counter()
        original = ListOfAI[:]
        while len(ListOfAI) < AIPerGen:
            NewAI = random.choice(original).Evolve()
            NewAI.Name = "NeuralNetwork" + str(NumberOfAI)
            ListOfAI.append(NewAI)
            NumberOfAI += 1 
        
        for Player1 in ListOfAI:
            for _ in range(NumberOfMatches-1):
                Player2 = random.choice(ListOfAI)
                TwoPlayers = [Player1,Player2]
                for _ in range(NumberOfGamesPerMatch):
                    random.shuffle(TwoPlayers)
                    RatedGame(TwoPlayers[0], TwoPlayers[1])

            Player2 = KylesWeighting()
            TwoPlayers = [Player1,Player2]
            for _ in range(3):
                random.shuffle(TwoPlayers)
                RatedGame(TwoPlayers[0], TwoPlayers[1])
            
            with open('ListOfAI', 'wb') as f:pickle.dump(ListOfAI,f)


        NumberOfRounds += 1
        print(f"Round Number : {NumberOfRounds}")
        print(time.perf_counter()-Time)
        ListOfAI.sort(key=(lambda x:x.Rating), reverse=True)

        i = 3
        while ListOfAI[i].Rating > 1000 and len(ListOfAI)<7:
            i += 1
        ListOfAI = ListOfAI[:i]

        DictOfAI = {Player.Name:Player.Rating for Player in ListOfAI}
        DictOfAI["NumberOfRounds"] = NumberOfRounds
        for AI in ListOfAI:AI.Rating = 1000
        
        with open('ListOfAI', 'wb') as f:pickle.dump(ListOfAI,f)
 
        with open('AITournamentResults.csv', "w") as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName","PlayerRating"])
            writer.writerow(["NumberOfRounds",NumberOfRounds])
            writer.writerow(["NumberOfAI",NumberOfAI])
            for Player in ListOfAI:
                writer.writerow([Player.Name,Player.Rating])
