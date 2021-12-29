from ChessBots import *
from EvaluatorBots import *
from Board import *
from BotLists import *

import pickle
import time

def BasicGame(Player1,Player2):
    MoveNum = 0
    CurrentPlayer = Player1
    OtherPlayer = Player2
    CurrentColour = "W"
    y = MakingStartingPos()

    Board, Pieces = y[0], y[1]
    
    while True:
        MoveNum+=1

        if MoveNum >= 500:
            return 0.5

        if len(Pieces["WK"]) + len(Pieces["BK"]) < 18:break

        Move = CurrentPlayer.Move(Board,Pieces,CurrentColour)

        NewBoard = MovingAPiece(Move[0], Move[1],Board,Pieces)

        Board, Pieces = NewBoard[0], NewBoard[1]

        CurrentPlayer, OtherPlayer = OtherPlayer, CurrentPlayer
        CurrentColour = "B" if CurrentColour == "W" else "W"

    WhiteWin = int(len(Pieces["WK"]) == 9)
    
    return WhiteWin

def DisplayGame(Player1,Player2,WaitTime = 1,DispLastMove = True):
    MoveNum = 0
    CurrentPlayer = Player1
    OtherPlayer = Player2
    CurrentColour = "W"
    y = MakingStartingPos()

    Board, Pieces = y[0], y[1]
    
    while True:
        
        if MoveNum >= 300:
            print("Draw")
            return 0.5
        MoveNum+=1

        if len(Pieces["WK"]) + len(Pieces["BK"]) < 18:break

        Move = CurrentPlayer.Move(Board,Pieces,CurrentColour)

        NewBoard = MovingAPiece(Move[0], Move[1],Board,Pieces)

        Board, Pieces = NewBoard[0], NewBoard[1]

        LastMove = None if not DispLastMove else str(Move[0])
        DisplayingBoard(Board,Wait = 0,LastMove = LastMove)

        print(Board[Move[1]] + " " + ConvertingPosToCoords(Move[0]) + " " + ConvertingPosToCoords(Move[1]))
        time.sleep(WaitTime)

        CurrentPlayer, OtherPlayer = OtherPlayer, CurrentPlayer
        CurrentColour = "B" if CurrentColour == "W" else "W"

    WhiteWin = int(len(Pieces["WK"]) == 9)
    
    return WhiteWin

def RatedGame(Player1,Player2):
    Result = BasicGame(Player1,Player2)
    Ratings = CalculatingRatingChange(Player1.Rating,Player2.Rating,1,Result)
    Player1.Rating = Ratings[0]
    Player2.Rating = Ratings[1]
    
    return Player1,Player2

def Battle(Player1,Player2,NumberOfGames = 10):
    Players = [Player1,Player2]
    Wins = [0,0]

    for _ in range(NumberOfGames):
        Result = BasicGame(Players[0],Players[1])
        Wins[0] += Result
        Wins[1] += 1- Result
        Wins = Wins[::-1]
        Players = Players[::-1]
    
    print(Players[0].Name," : ",Wins[0])
    print(Players[1].Name," : ",Wins[1])

def SettingUpBattle(NumberOfGames = 10):
    Bots = sorted(ListOfEveryBot(),key = (lambda x:x.Name))
    for i in range(len(Bots)):
        print(i," : ",Bots[i].Name)

    Player1 = Bots[int(input("Player 1 index "))]
    Player2 = Bots[int(input("Player 2 index "))]

    Battle(Player1,Player2,NumberOfGames)

def Tournament(ListOfPlayers = ListOfEveryBot(),MaxMatches = 5 ,NumberOfGamesPerMatch = 3):
    ListOfPlayers = GettingBotEloForList(ListOfPlayers)
    for _ in range(MaxMatches):
        for Player1 in ListOfPlayers:
            Player2 = random.choice(ListOfPlayers)

            print(Player1.Name,"\nvs")
            print(Player2.Name,"\n")
            for _ in range(NumberOfGamesPerMatch):
                RatedGame(Player1, Player2)


    ListOfPlayers.sort(key=(lambda x:x.Rating), reverse=True)

    for Bot in ListOfPlayers:
        print(Bot.Name,Bot.Rating)
    
    return ListOfPlayers

def StoredTournament(ListOfPlayers = ListOfEveryBot(),MaxMatches = 5 ,NumberOfGamesPerMatch = 3):
    
    ListOfPlayers = Tournament(ListOfPlayers,MaxMatches,NumberOfGamesPerMatch)
    ListOfPlayers = GettingBotEloForList(ListOfPlayers)

    DictOfPlayers = {Player.Name:Player.Rating for Player in ListOfPlayers}

    file = open("TournamentResultsDict", "wb")
    pickle.dump(DictOfPlayers,file)
    file.close()

    f = open('TournamentResults', 'w')

    writer = csv.writer(f)

    writer.writerow(["PlayerName","PlayerRating"])
    for Player in ListOfPlayers:
        writer.writerow([Player.Name,Player.Rating])
    f.close()

def EternalTournament(ListOfPlayers = ListOfEveryBot(),NumberOfGamesPerMatch = 3):
    ListOfPlayers = GettingBotEloForList(ListOfPlayers)

    NumberOfRounds = 0
    with open('TournamentResults.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in reader:
            if len(row) == 0:continue
            
            if row[0] == "NumberOfRounds":
                NumberOfRounds = int(row[1])
                break

    while True:
        random.shuffle(ListOfPlayers)
        for Player1 in ListOfPlayers:
            Player2 = random.choice(ListOfPlayers)
            TwoPlayers = [Player1,Player2]
            for _ in range(NumberOfGamesPerMatch):
                random.shuffle(TwoPlayers)
                RatedGame(TwoPlayers[0], TwoPlayers[1])

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

def FindingEloOfABot(Bot,ListOfOpponents = CulledListOfBots(),NumberOfGamesPerMatch = 3):
    ListOfOpponents = GettingBotEloForList([ Player for Player in ListOfOpponents if Player.Name != Bot.Name]) 
    Bot = GettingBotEloForList([Bot])[0]
    DictOfPlayers = {Player.Name:Player.Rating for Player in ListOfOpponents + [Bot]}
    NumberOfRounds = 0

    with open('TournamentResults.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in reader:
            if len(row) == 0:continue
            
            if row[0] == "NumberOfRounds":
                DictOfPlayers["NumberOfRounds"] = row[1]
                break
    while True:
        for _ in range(5):
            Player2 = random.choice(ListOfOpponents)
            Players = [Bot,Player2]
            random.shuffle(Players)
            for _ in range(NumberOfGamesPerMatch):
                RatedGame(Players[0], Players[1])

        NumberOfRounds += 1
        print(f"Round Number : {NumberOfRounds}")
        DictOfPlayers[Bot.Name] = Bot.Rating
        
        with open('TournamentResultsDict', 'wb') as f:
            pickle.dump(DictOfPlayers,f)

        with open('TournamentResults.csv', "w") as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName","PlayerRating"])
            writer.writerow(["NumberOfRounds",DictOfPlayers["NumberOfRounds"]])
            for Player in sorted(ListOfOpponents + [Bot],key=(lambda X:DictOfPlayers[X.Name]),reverse=True):
                writer.writerow([Player.Name,DictOfPlayers[Player.Name]])

def EternalTournamentWithAI(ListOfPlayers = ListOfEveryBot(),NumberOfGamesPerMatch = 3):
    ListOfPlayers = GettingBotEloForList(ListOfPlayers)
    with open('ListOfAI', 'rb') as f:
        ListOfAI = pickle.load(f)
    
    ListOfPlayers += ListOfAI
    NumberOfRounds = 0
    with open('TournamentResults.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in reader:
            if len(row) == 0:continue
            
            if row[0] == "NumberOfRounds":
                NumberOfRounds = int(row[1])
                break

    while True:
        random.shuffle(ListOfPlayers)
        for Player1 in ListOfPlayers:
            Player2 = random.choice(ListOfPlayers)
            TwoPlayers = [Player1,Player2]
            for _ in range(NumberOfGamesPerMatch):
                random.shuffle(TwoPlayers)
                RatedGame(TwoPlayers[0], TwoPlayers[1])

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
