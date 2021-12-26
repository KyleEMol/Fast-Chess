from NeuralNetworkPlayer import *

class KylesWeighting(BasicBot):
    def __init__(self):
        BasicBot.__init__(self)
        self.FilterBot = NoFilter(None)

    def Move(self,BoardDict ,PiecesDict, Colour):
        LegalMoves = self.FilterBot.Move(BoardDict,PiecesDict,Colour)
        BestEval = -9999999
        BestMoves = []

        for Move in LegalMoves:
            if BoardDict.get(Move[1],[None,None])[1] == "K":return Move
            Eval = self.Evaluate(Move,BoardDict,PiecesDict,Colour)

            if Eval > BestEval:
                BestEval = Eval
                BestMoves = [Move]
            elif Eval == BestEval:
                BestMoves.append(Move)
        
        return random.choice(BestMoves)

    def Evaluate(self,Move,BoardDict,PiecesDict,Colour):
        OppPiece = BoardDict[Move[1]]
        PieceNames = ["P","R","N","B","Q","K" ]
        OppPiece = [(0 if PieceNames[i] != OppPiece[1] else 1) for i in range(8)]

        if Colour == "W":
            OppKingAttacked,OwnKingAttacked = CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "B"),CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "W")
        else:
            OppKingAttacked,OwnKingAttacked = CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "W"),CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "B")

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

        #OppPiece  + OwnKingAttacked + OpponentKingAttacked + before(Z + W + Y  dist from starting + X) + after(Z + W + Y  dist from starting + X)
        Input = OppPiece + [OwnKingAttacked] + [OppKingAttacked] + OldZ + OldW + OldX + OldY + NewZ + NewW + NewX + NewY
        Weights = [1,3,3,5,9,100000] + [-10000] + [9] + [0,2,0] + [0,2,0] + [1,2,3,4,4,3,2,1] + [0,0,1,2,3,3,4,5] + [0,2,0] + [0,2,0] + [1,2,3,4,4,3,2,1] + [0,0,1,2,3,3,4,5]

        Eval = 0 
        for i in range(len(Input)):
            Eval += Input[i] * Weights[i]
        
        return Eval

    def BasicEvaluate(self,Move,BoardDict,PiecesDict,Colour):

        #OppPiece  + OwnKingAttacked + OpponentKingAttacked+ +Z + W + Y + X
        Input = [0,0,0,0,0,0] + [0] + [0] + [0,0,0] + [0,0,0] + [0,0,0,0,0,0,0,0] + [0,0,0,0,0,0,0,0]
        Weights = [1,3,3,5,9,100000] + [-10000] + [9] + [0,2,0] + [0,2,0] + [1,2,3,4,4,3,2,1] + [0,0,1,2,3,3,4,5]
        OwnPiece = BoardDict[Move[0]]
        PiecesValDict = {None : 0,"P":1,"B":3,"N":3,"R":5,"Q":9,"K":100000}

        OppPieceVal = PiecesValDict[BoardDict.get(Move[1],[None,None])[1]]


        if Colour == "W":
            OppKingAttacked,OwnKingAttacked = CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "B"),CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "W")
        else:
            OppKingAttacked,OwnKingAttacked = CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "W"),CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "B")


        ExtraDWeights = [0,2,0]
        XWeights = [1,2,3,4,4,3,2,1]
        YWeights = [0,0,1,2,3,3,4,5][::-1 if Colour == "B" else 1]

        if OwnPiece[1] == "K":
            ExtraDWeights = [3 - X for X in ExtraDWeights]
            XWeights = [2 - X for X in XWeights]
            YWeights = [2 - X for X in YWeights]

        TMove = str(Move[0])
        OldPositionalVal = ExtraDWeights[int(TMove[0])-1]+ExtraDWeights[int(TMove[1])-1]+YWeights[int(TMove[2])-1] + XWeights[int(TMove[3])-1]
        TMove = str(Move[1])
        NewPositionalVal = ExtraDWeights[int(TMove[0])-1]+ExtraDWeights[int(TMove[1])-1]+YWeights[int(TMove[2])-1] + XWeights[int(TMove[3])-1]
        

        Eval = (OppPieceVal + (NewPositionalVal - OldPositionalVal)/10 + OppKingAttacked*1000) - ( OwnKingAttacked * 10000)

        return Eval





