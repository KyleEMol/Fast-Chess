from Game import *
from NeuralNetworkPlayer import *

def EternalNeuralNetworkTournament(NumberOfAI=60,NumberOfGamesPerMatch = 2,NumberOfMatches = 3):
    
    ListOfHardCodedBots = GettingBotEloForList([WarmongerBot(BountyHunter),BishopBudger(BountyHunter),WarmongerBot(ComparingCollectorBot),NoFilter(BountyHunter),BasicBot()])

    with open('ListOfAI', 'rb') as f:
        ListOfAI = pickle.read(f)
    
    if len(ListOfAI) == 0:

    NumberOfRounds = 0
    with open('TournamentResults.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in reader:
            if len(row) == 0:continue
            
            if row[0] == "NumberOfRounds":
                NumberOfRounds = int(row[1])
                break

    while True:
        for Player1 in ListOfPlayers:
            Player2 = random.choice(ListOfPlayers)
            for _ in range(NumberOfGamesPerMatch):
                RatedGame(Player1, Player2)

        NumberOfRounds += 1
        print(f"Round Number : {NumberOfRounds}")
        ListOfPlayers.sort(key=(lambda x:x.Rating), reverse=True)
        DictOfPlayers = {Player.Name:Player.Rating for Player in ListOfPlayers}
        DictOfPlayers["NumberOfRounds"] = NumberOfRounds
        
        with open('TournamentResultsDict', 'wb') as f:
            pickle.dump(DictOfPlayers,f)

        with open('TournamentResults.csv', "w") as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName","PlayerRating"])
            writer.writerow(["NumberOfRounds",NumberOfRounds])
            for Player in ListOfPlayers:
                writer.writerow([Player.Name,Player.Rating])
