from ChessBots import *
from EvaluatorBots import *
import pickle
def RandomBot():
    Bot = random.choice(ListOfFilterBots)(random.choice(ListOfEvaluatorBots+ListOfDecisionBots))
    return Bot

def ListOfEveryBot():
    ListOfAllBots=[]
    for FilterBot in ListOfFilterBots:
        for EvalBot in ListOfEvaluatorBots+ListOfDecisionBots:
            ListOfAllBots.append(FilterBot(EvalBot))

    random.shuffle(ListOfAllBots)
    return ListOfAllBots

def CulledListOfBots():
    CulledListOfAllBots=[]

    for FilterBot in ListOfFilterBotsWithoutPacifist:
        for EvalBot in ListOfEvaluatorBotsWithoutSpacious+ListOfDecisionBots:
            CulledListOfAllBots.append(FilterBot(EvalBot))

    CulledListOfAllBots.append(Pacifist(RandomMoveBot))
    CulledListOfAllBots.append(BasicBot)
    
    random.shuffle(CulledListOfAllBots)
    return CulledListOfAllBots

def TestListOfBots():
    TestList = []
    for FilterBot in [WarmongerBot,KnightKnocker]:
        for EvalBot in [RandomEvaluatorBot,ComparingHoarderBot]+[RandomMoveBot,BountyHunter]:
            TestList.append(FilterBot(EvalBot))
    
    return TestList

def AllBots():
    ListOfAllBots=[]
    for FilterBot in ListOfFilterBots:
        for EvalBot in ListOfEvaluatorBots+ListOfDecisionBots:
            ListOfAllBots.append(FilterBot(EvalBot))

    random.shuffle(ListOfAllBots)
    for bot in ListOfAllBots:
        yield bot

def GettingBotElo(Bot):
    with open('TournamentResultsDict', 'rb') as f:
        RatingsDict = pickle.load(f)
    Bot.Rating = int(RatingsDict.get(Bot.Name, 1000))
    return Bot

def GettingBotEloForList(ListOfBots):
    
    PlayersDict = {}
    with open('TournamentResults.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in reader:
            if len(row) == 0: continue
            PlayersDict[row[0]] = row[1]
                

    for Bot in ListOfBots:
        Bot.Rating = float(PlayersDict.get(Bot.Name, 1000))
    
    return ListOfBots
