from NeuralNetworkPlayer import *

class KylesWeighting(BasicBot):
    def __init__(self):
        BasicBot.__init__(self)
        self.FilterBot = NoFilter(None)

    def Move(self,BoardDict ,PiecesDict, Colour):
        LegalMoves = self.FilterBot.Move(BoardDict,PiecesDict,Colour)

        for Move in LegalMoves:
            Eval = self.Evaluate(Move,BoardDict,PiecesDict,Colour)
    
    def Evaluate(self,Move,BoardDict,PiecesDict,Colour):
        OwnPiece = BoardDict[Move[0]]
        PiecesValDict = {None : 0,"P":1,"B":3,"N":3,"R":5,"Q":9,"K":100000}

        OppPieceVal = PiecesValDict[BoardDict.get(Move[1],[None,None])[1]]
        OwnPieceVal = PiecesValDict[OwnPiece[1]]

        BlackKingAttacked = CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "B")
        WhiteKingAttacked = CheckingKingAttackers(BoardDict = BoardDict ,PieceDict = PiecesDict,Colour = "W")

        if Colour == "W":
            OppKingAttacked,OwnKingAttacked = BlackKingAttacked,WhiteKingAttacked
        else:
            OppKingAttacked,OwnKingAttacked = WhiteKingAttacked,BlackKingAttacked

        ExtraDWeights = [0,2,0]
        XWeights = [1,2,3,4,4,3,2,1]
        YWeights = [0,0,1,2,3,3,4,5][::-1 if Colour == "B" else 1]

        TMove = str(Move[1])
        PositionalVal = ExtraDWeights[int(TMove[0])-1]+ExtraDWeights[int(TMove[1])-1]+YWeights[int(TMove[2])-1] + XWeights[int(TMove[3])-1]

        if OwnPiece[1] == "K":PositionalVal*=-1

        Eval = (OppPieceVal + PositionalVal + OppKingAttacked*1000) - (OwnPieceVal*0.75 + OwnKingAttacked * 10000)

        return Eval





