from NeuralNetworkPlayer import *

class KylesWeighting(BasicBot):
    def __init__(self):
        BasicBot.__init__(self)
        self.FilterBot = NoFilter(None)

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
        Weights = [0,-0,-0,0,0,-5]+ list(map((lambda x: x + 7),[10,30,30,50,90,100000])) + [-10000] + [3] + [0,-2,0] + [0,-2,0] + list(map((lambda x:x*0.5),[-3,-1,-4,-7,-7,-4,-1,-3])) + list(map((lambda x:x*0.5),[0,-1,-1,-3,-6,-6,-10,-15]))+ [0,2,0] + [0,2,0] + list(map((lambda x:x*0.5),[-2,1,4,7,7,4,1,-2])) + list(map((lambda x:x*0.5),[0,1,1,3,6,6,10,15]))

        Eval = 0 
        for i in range(len(Input)):
            Eval += Input[i] * Weights[i]
        
        return Eval
