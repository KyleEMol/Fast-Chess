from NeuralNetwork import *
from EvaluatorBots import *

WhitePieceNames = ["WP","WR","WN","WB","WQ","WK" ] 
BlackPieceNames = ["BP","BR","BN","BB","BQ","BK" ]


def FindingIfKightIsAttacking(BoardDict=dict,Pos = int,Colour = str):
    KnightName = "WN" if Colour == "B" else "BN"
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            if Direction + Direction2 == 0 or Direction == Direction2:continue
            Diff = Direction + (Direction2 * 2)

            if BoardBoundsChecker(Pos + Diff):
                if BoardDict.get(Pos+Diff) == KnightName:
                    return True
    
    return False

def FindingIfRookQueenKingsIsAttacking(BoardDict=dict,Pos = int,Colour = str):
    OppositeColour = "W" if Colour == "B" else "B"

    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        LoopNum = 1 
        Diff = Direction
        while BoardBoundsChecker(Pos + Diff): 
            Diff = LoopNum*Direction
            LoopNum += 1 
            if BoardDict.get(Pos+Diff) == None:
                continue

            if BoardDict.get(Pos+Diff)[0] == OppositeColour:
                if BoardDict.get(Pos+Diff)[1] == "R" or "Q":
                    return True
                elif BoardDict.get(Pos+Diff)[1] == "K" and LoopNum == 1:
                    return True

            break
    return False

def FindingIfBishopQueenKingsIsAttacking(BoardDict=dict,Pos = int,Colour = str):
    OppositeColour = "W" if Colour == "B" else "B"

    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            if Direction + Direction2 == 0 or Direction == Direction2:continue
            Diff = Direction + Direction2
            LoopNum = 1 

            while BoardBoundsChecker(Pos + Diff): 
                Diff = LoopNum*Direction
                LoopNum += 1 

                if BoardDict.get(Pos+Diff) == None:
                    continue

                if BoardDict.get(Pos+Diff)[0] == OppositeColour:
                    if BoardDict.get(Pos+Diff)[1] == "R" or "Q":
                        return True
                    elif BoardDict.get(Pos+Diff)[1] == "K" and LoopNum == 1:
                        return True
           
                break
    return False

def CheckingIfPawnIsAttacking(BoardDict=dict,Pos = int,Colour = str):
    OppositeColour = "W" if Colour == "B" else "B"

    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000
    LegalDirections = [YU] if OppositeColour == "B" else [YD]
    LegalDirections += [WU, WD, ZL, ZR]
    
    
    AttackingDirections = LegalDirections + [XL,XR]
    for Direction in AttackingDirections:
        for Direction2 in AttackingDirections:
            if Direction + Direction2 == 0 or Direction == Direction2:continue

            if BoardDict.get(Direction+Direction2+Pos) == OppositeColour +"P":
                return True

  
    return False

def CheckingIfPieceIsAttacked(BoardDict = dict ,PieceLocation = int,Colour = str):
    ListOfFindingFuncs = [FindingIfKightIsAttacking,FindingIfRookQueenKingsIsAttacking,FindingIfBishopQueenKingsIsAttacking,CheckingIfPawnIsAttacking]
    
    for Func in ListOfFindingFuncs:
        if bool(Func(BoardDict = BoardDict,Pos = PieceLocation,Colour = Colour)):
            return True
    return False

def CheckingKingAttackers(BoardDict = dict ,PieceDict = dict,Colour = str):
    NumberOfKingsUnderAttack = 0
    for King in PieceDict[Colour+"K"]:
        NumberOfKingsUnderAttack += CheckingIfPieceIsAttacked(BoardDict = BoardDict ,PieceLocation = King,Colour = Colour)
    return NumberOfKingsUnderAttack

class NeuralNetworkPlayer(BasicBot):
    def __init__(self,FilterBot = NoFilter(None),Name = "NeuralNetwork"):
        BasicBot.__init__(self)
        self.Name = Name
        self.NeuralNetwork = NeuralNetwork(Layout = [14,28,56,28,14,1])
        self.FilterBot = FilterBot

    def Move(self,BoardDict ,PiecesDict, Colour):

        LegalMoves = self.FilterBot.Move(BoardDict,PiecesDict, Colour)

        BestEval = -9999999
        BestMoves = []

        for Move in LegalMoves:
            NewBoard = MovingAPiece(Move[0],Move[1],BoardDict,PiecesDict)
            Eval = float(self.Evaluate(NewBoard[0],NewBoard[1],Colour))
            Eval = round(Eval,2)
            if Eval > BestEval:
                BestMoves = [Move]
                BestEval = Eval
            
            elif Eval == BestEval:
                BestMoves.append(Move)
 
        return random.choice(BestMoves)

    def Evaluate(self,BoardDict,PiecesDict,Colour):
        if Colour == "W":Input = [len(PiecesDict[Piece]) for Piece in BlackPieceNames]
        else: Input = [len(PiecesDict[Piece]) for Piece in WhitePieceNames]

        Input += [CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "W"),CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "B")][::(1 if Colour == "W" else -1)]       

        Evaluation = self.NeuralNetwork.Output(Input)
        return Evaluation

    def Evolve(self):
        NewPlayer = NeuralNetworkPlayer(FilterBot = self.FilterBot)
        NewPlayer.NeuralNetwork = self.NeuralNetwork.MakingAnEvolvedNetwork()
        NewPlayer.Rating = self.Rating
        return NewPlayer
        
