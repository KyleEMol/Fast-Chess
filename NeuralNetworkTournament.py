from Game import *
from NeuralNetworkPlayer import *
from KylesWeightings import *


def EvaluatingAListOfAI(ListOfAI = list):
    NewListOfAI = []
    for AI in ListOfAI:
        AI.Rating = 1000

        ListOfOppBots =  [WarmongerBot(BountyHunter),WarmongerBot(Bully),KylesWeighting()]
        

        ListOfOppBots[0].Rating,ListOfOppBots[1].Rating,ListOfOppBots[2].Rating = 1090,990,920
        for Bot in ListOfOppBots:
            TwoPlayers = [AI, Bot] 
            random.shuffle(TwoPlayers)
            RatedGame(TwoPlayers[0], TwoPlayers[1])

        NewListOfAI.append(AI)

    return NewListOfAI


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
        RoundTime = time.perf_counter()
        original = ListOfAI[:]
        while len(ListOfAI) < AIPerGen:
            NewAI = random.choice(original).Evolve()
            NewAI.Name = "NeuralNetwork" + str(NumberOfAI)
            ListOfAI.append(NewAI)
            NumberOfAI += 1 

        for AI in ListOfAI:
            AI.Rating = 1000        
        
        for Player1 in ListOfAI:
            for _ in range(NumberOfMatches-1):
                Player2 = random.choice(ListOfAI)
                TwoPlayers = [Player1,Player2]
                for _ in range(NumberOfGamesPerMatch):
                    random.shuffle(TwoPlayers)
                    RatedGame(TwoPlayers[0], TwoPlayers[1])

            Player2 = KylesWeighting()
            TwoPlayers = [Player1,Player2]
            Time = time.perf_counter()
            for _ in range(3):
                random.shuffle(TwoPlayers)
                RatedGame(TwoPlayers[0], TwoPlayers[1])
            
            Player1.TotalGameTime += time.perf_counter() - Time
            Player1.GamesPlayed += 3

            with open('ListOfAI', 'wb') as f:
                pickle.dump(ListOfAI,f)


        NumberOfRounds += 1
        print(f"Round Number : {NumberOfRounds}")
        print(time.perf_counter()-RoundTime)
        ListOfAI.sort(key=(lambda x:x.Fitness()), reverse=True)

        i = 3
        while ListOfAI[i].Fitness() > 1000 and len(ListOfAI)<7:
            i += 1
        ListOfAI = ListOfAI[:i]

        with open('AITournamentResults.csv', "w") as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName","PlayerRating"])
            writer.writerow(["NumberOfRounds",NumberOfRounds])
            writer.writerow(["NumberOfAI",NumberOfAI])
            for Player in ListOfAI:
                writer.writerow([Player.Name,Player.Rating])
        
        with open('ListOfAI', 'wb') as f:
            pickle.dump(ListOfAI,f)
        
        if NumberOfRounds%10 == 0 :
            ListOfAI = EvaluatingAListOfAI(ListOfAI = ListOfAI)

            with open('C:/Users/Kyle Molindo/Desktop/EMC/EMC 3/Chess/Fast-Chess/Saved AI Rounds/AITournamentResults '+ str(NumberOfRounds)+".csv", "w") as f:
                writer = csv.writer(f)
                writer.writerow(["PlayerName","PlayerRating"])
                writer.writerow(["NumberOfRounds",NumberOfRounds])
                writer.writerow(["NumberOfAI",NumberOfAI])
                for Player in ListOfAI:
                    writer.writerow([Player.Name,Player.Rating])


            AverageRating = sum([AI.Rating for AI in ListOfAI])/len(ListOfAI)
            AverageTimeTaken = sum([(AI.TotalGameTime / AI.GamesPlayed) for AI in ListOfAI])/len(ListOfAI)
            TList = [AverageRating,AverageTimeTaken,NumberOfRounds,NumberOfAI] + ListOfAI
            with open('C:/Users/Kyle Molindo/Desktop/EMC/EMC 3/Chess/Fast-Chess/Saved AI Rounds/ListOfAIRound '+str(NumberOfRounds)+".pckle", 'wb') as f:pickle.dump(TList,f)
