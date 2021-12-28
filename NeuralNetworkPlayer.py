from NeuralNetwork import *
from EvaluatorBots import *

WhitePieceNames = ["WP","WR","WN","WB","WQ","WK" ] 
BlackPieceNames = ["BP","BR","BN","BB","BQ","BK" ]


def FindingIfKightIsAttacking(BoardDict=dict,Pos = int,Colour = str):
    KnightName = "WN" if Colour == "B" else "BN"
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    KnightLocations = set([])

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            if Direction + Direction2 == 0 or Direction == Direction2:continue
            Diff = Direction + (Direction2 * 2)

            if BoardBoundsChecker(Pos + Diff):
                if BoardDict.get(Pos+Diff) == KnightName:
                    KnightLocations.add(Pos+Diff)
                    return KnightLocations
    
    return KnightLocations

def FindingIfFileIsAttacked(BoardDict=dict,Pos = int,Colour = str):
    OppositeColour = "W" if Colour == "B" else "B"

    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    FileAttackers = set([])

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        LoopNum = 1 
        Diff = Direction
        while BoardBoundsChecker(Pos + Diff):
            TempMoves = set([])
            Diff = LoopNum*Direction
            LoopNum += 1
            if BoardDict.get(Pos+Diff) == None:
                TempMoves.add(Pos+Diff)
                continue

            if BoardDict.get(Pos+Diff)[0] == OppositeColour:
                if BoardDict.get(Pos+Diff)[1] == "R" or "Q":
                    TempMoves.add(Pos+Diff)
                    FileAttackers.update(TempMoves)
                    return FileAttackers

            break

    return FileAttackers

def FindingIfDiagonalIsAttacked(BoardDict=dict,Pos = int,Colour = str):
    OppositeColour = "W" if Colour == "B" else "B"

    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    DiagonalAttackers = set([])

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            if Direction + Direction2 == 0 or Direction == Direction2:continue
            Diff = Direction + Direction2
            LoopNum = 1 
            TempMoves = set([])

            while BoardBoundsChecker(Pos + Diff): 
                Diff = LoopNum*Direction
                LoopNum += 1 

                if BoardDict.get(Pos+Diff) == None:
                    TempMoves.add(Pos+Diff)
                    continue

                if BoardDict.get(Pos+Diff)[0] == OppositeColour:
                    if BoardDict.get(Pos+Diff)[1] == "B" or "Q":
                        TempMoves.add(Pos+Diff)
                        DiagonalAttackers.update(TempMoves)
                        return DiagonalAttackers
                break

    return DiagonalAttackers

def CheckingIfPawnIsAttacking(BoardDict=dict,Pos = int,Colour = str):
    OppositeColour = "W" if Colour == "B" else "B"

    PawnAttacks = set([])
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000
    LegalDirections = [YU] if OppositeColour == "B" else [YD]
    LegalDirections += [WU, WD, ZL, ZR]
    
    AttackingDirections = LegalDirections + [XL,XR]
    for Direction in AttackingDirections:
        for Direction2 in AttackingDirections:
            if Direction + Direction2 == 0 or Direction == Direction2:continue

            if BoardDict.get(Direction+Direction2+Pos) == OppositeColour +"P":
                PawnAttacks.add((Direction+Direction2+Pos))
                return PawnAttacks

    return PawnAttacks

def CheckingIfPieceIsAttacked(BoardDict = dict ,PieceLocation = int,Colour = str):
    ListOfFindingFuncs = [FindingIfDiagonalIsAttacked,FindingIfFileIsAttacked,FindingIfKightIsAttacking,CheckingIfPawnIsAttacking]
    Output = set([])
    for Func in ListOfFindingFuncs:
        Result =  Func(BoardDict = BoardDict,Pos = PieceLocation,Colour = Colour)
        if Result:
            return Result
    return Output

def CheckingKingAttackedSquares(BoardDict = dict ,PieceDict = dict,Colour = str):
    for King in PieceDict[Colour+"K"]:
        TempResults = CheckingIfPieceIsAttacked(BoardDict = BoardDict ,PieceLocation = King,Colour = Colour)
        if TempResults:
            TempResults.add(King)
            return TempResults
    
    return set([])

def CheckingWaysToAttackWithKnight(BoardDict=dict,Pos = int,Colour = str):
    PlacesToAttackFrom = set([])
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            if Direction + Direction2 == 0 or Direction == Direction2:continue
            Diff = Direction + (Direction2 * 2)

            if BoardBoundsChecker(Pos + Diff):
                if BoardDict.get(Pos+Diff) != None:
                    if BoardDict.get(Pos+Diff)[0] != Colour:
                        PlacesToAttackFrom.add(Pos+Diff) 
    
    return PlacesToAttackFrom

def CheckingHowToAttackFiles(BoardDict=dict,Pos = int,Colour = str):
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    PlacesToAttackFrom = set([])

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        LoopNum = 1 
        Diff = Direction
        while BoardBoundsChecker(Pos + Diff):
            Diff = LoopNum*Direction
            LoopNum += 1
            if BoardDict.get(Pos+Diff) == None:
                PlacesToAttackFrom.add(Pos+Diff)
                continue

            if BoardDict.get(Pos+Diff)[0] != Colour:
                PlacesToAttackFrom.add(Pos+Diff)

            break

    return PlacesToAttackFrom

def CheckingHowToAttackDiagonals(BoardDict=dict,Pos = int,Colour = str):
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000

    PlacesToAttackFrom = set([])

    for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
        for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            if Direction + Direction2 == 0 or Direction == Direction2:continue
            Diff = Direction + Direction2
            LoopNum = 1 

            while BoardBoundsChecker(Pos + Diff): 
                Diff = LoopNum*Direction
                LoopNum += 1 

                if BoardDict.get(Pos+Diff) == None:
                    PlacesToAttackFrom.add(Pos+Diff)
                    continue

                if BoardDict.get(Pos+Diff)[0] != Colour:
                    if BoardDict.get(Pos+Diff)[1] == "B" or "Q":
                        PlacesToAttackFrom.add(Pos+Diff)
                break

    return PlacesToAttackFrom

def CheckingWaysToAttackWithPawn(BoardDict=dict,Pos = int,Colour = str):

    PlacesToAttackFrom = set([])
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000
    LegalDirections = [YU] if Colour == "W" else [YD]
    LegalDirections += [WU, WD, ZL, ZR]
    
    AttackingDirections = LegalDirections + [XL,XR]
    for Direction in AttackingDirections:
        for Direction2 in AttackingDirections:
            if Direction + Direction2 == 0 or Direction == Direction2:continue

            if BoardDict.get(Direction+Direction2+Pos) == "W" if Colour == "B" else "B" +"P":
                PlacesToAttackFrom.add((Direction+Direction2+Pos))

    return PlacesToAttackFrom

def CheckingWaysToAttackKings(BoardDict = dict ,PieceDict = dict,Colour = str):
    WaysToAttackKings = [set([]) for _ in range(4)]
    ListOfFindingFuncs = [CheckingWaysToAttackWithKnight,CheckingHowToAttackFiles,CheckingHowToAttackDiagonals,CheckingWaysToAttackWithPawn]

    for King in PieceDict[Colour+"K"]:
        i = 0
        for Func in ListOfFindingFuncs:
            WaysToAttackKings[i].update(Func(BoardDict=BoardDict,Pos = King,Colour = Colour))
            i += 1
    
    return WaysToAttackKings


class NeuralNetworkPlayer(BasicBot):
    def __init__(self,FilterBot = NoFilter(None),Name = "NeuralNetwork"):
        BasicBot.__init__(self)
        self.Name = Name
        self.NeuralNetwork = NeuralNetwork(Layout = [62,62,62,16,1])
        self.FilterBot = FilterBot

    def Move(self,BoardDict ,PiecesDict, Colour):
        LegalMoves = self.FilterBot.Move(BoardDict,PiecesDict,Colour)
        BestEval = -9999999
        BestMoves = []

        SquaresOwnKingAttackedFrom = CheckingKingAttackedSquares(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = Colour)
        WaysToAttackOppKing = CheckingWaysToAttackKings(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = Colour)

        for Move in LegalMoves:
            if BoardDict.get(Move[1],[None,None])[1] == "K":return Move
            Eval = self.Evaluate(Move,BoardDict,PiecesDict,Colour,SquaresOwnKingAttackedFrom,WaysToAttackOppKing)

            if Eval > BestEval:
                BestEval = Eval
                BestMoves = [Move]
            elif Eval == BestEval:
                BestMoves.append(Move)
        
        return random.choice(BestMoves)

    def Evaluate(self,Move,BoardDict,PiecesDict,Colour,SquaresOwnKingAttackedFrom,WaysToAttackOppKing):
        OppPieceName = BoardDict.get(Move[1],[None,None])[1]
        OwnPieceName = BoardDict.get(Move[0])[1]

        PieceNames = ["P","R","N","B","Q","K" ]
        OppPiece = [0 for _ in range(6)]  

        OwnPiece = [0 for _ in range(6)] 
        OwnPiece[PieceNames.index(OwnPieceName)] = 1 

        if OppPieceName:
            OppPiece[PieceNames.index(OppPieceName)] = 1 
        
        
        OldZ = [0,0,0]
        NewZ = [0,0,0]
        OldW = [0,0,0]
        NewW = [0,0,0]
        OldX = [0 for _ in range(8)]
        NewX = [0 for _ in range(8)]
        OldY = [0 for _ in range(8)]
        NewY = [0 for _ in range(8)]
        
        TMove = str(Move[0])
        OldZ[int(TMove[0])-1] = 1
        OldW[int(TMove[1])-1] = 1
        OldX[int(TMove[2])-1] = 1
        OldY[int(TMove[3])-1] = 1 

        TMove = str(Move[1])
        NewZ[int(TMove[0])-1] = 1
        NewW[int(TMove[1])-1] = 1
        NewX[int(TMove[2])-1] = 1
        NewY[int(TMove[3])-1] = 1 

        if Colour == "B":
            OldY = OldY[::-1]
            NewY = NewY[::-1]
        
        IsOpponentKingAttacked = False
        if OwnPieceName == "B":
            if Move[1] in WaysToAttackOppKing[1]:
                IsOpponentKingAttacked = True

        elif OwnPieceName == "N":
            if Move[1] in WaysToAttackOppKing[0]:
                IsOpponentKingAttacked = True

        elif OwnPieceName == "R":
            if Move[1] in WaysToAttackOppKing[2]:
                IsOpponentKingAttacked = True

        elif OwnPieceName == "Q":
            if Move[1] in WaysToAttackOppKing[2] or Move[1] in WaysToAttackOppKing[1]:
                IsOpponentKingAttacked = True
        
        elif OwnPieceName == "P":
            if Move[1] in WaysToAttackOppKing[3]:
                IsOpponentKingAttacked = True         

        IsOwnKingAttacked = False

        if len(SquaresOwnKingAttackedFrom)>0:
            IsOwnKingAttacked = True
            if Move[1] in SquaresOwnKingAttackedFrom:
                IsOwnKingAttacked = False      
            
            if OwnPieceName == "K":
                if Move[0] in SquaresOwnKingAttackedFrom:
                    IsOwnKingAttacked = True
                    if Move[1] not in SquaresOwnKingAttackedFrom:
                        IsOwnKingAttacked = False


        #OppPiece  + OwnKingAttacked + IsOpponentKingAttacked + before(Z + W + Y  dist from starting + X) + after(Z + W + Y  dist from starting + X)
        Input = OwnPiece + OppPiece + [int(IsOwnKingAttacked)] + [int(IsOpponentKingAttacked)] + OldZ + OldW + OldX + OldY + NewZ + NewW + NewX + NewY
        #Weights = [0,-1,-1.5,-2.5,-3.5,-5]+ list(map((lambda x: x + 7),[1,3,3,5,9,100000])) + [-10000] + [3] + [0,-2,0] + [0,-2,0] + list(map((lambda x:x*0.5),[-3,-1,-4,-7,-7,-4,-1,-3])) + list(map((lambda x:x*0.5),[0,-1,-1,-3,-6,-6,-10,-15]))+ [0,2,0] + [0,2,0] + list(map((lambda x:x*0.5),[-2,1,4,7,7,4,1,-2])) + list(map((lambda x:x*0.5),[0,1,1,3,6,6,10,15]))

        Evaluation = self.NeuralNetwork.Output(Input)
        return Evaluation

    def Evolve(self):
        NewPlayer = NeuralNetworkPlayer(FilterBot = self.FilterBot)
        NewPlayer.NeuralNetwork = self.NeuralNetwork.MakingAnEvolvedNetwork()
        NewPlayer.Rating = self.Rating
        return NewPlayer
        
