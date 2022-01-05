from ChessBots import *

WhitePieceNames = ["WP","WR","WN","WB","WQ","WK" ] 
BlackPieceNames = ["BP","BR","BN","BB","BQ","BK" ]

class EvaluatorBot():
    def __init__(self):
        BasicBot.__init__(self)

    def Choose(self, BoardDict, PiecesDict, Colour, LegalMoves):
        BestEval = -9999999
        BestMoves = []

        for Move in LegalMoves:
            if BoardDict.get(Move[1],"Na")[1] == "K":return Move
            NewBoard = MovingAPiece(Move[0],Move[1],BoardDict,PiecesDict)
            
            Eval = self.Evaluate(NewBoard[0],NewBoard[1],Colour)
            
            if Eval > BestEval:
                BestMoves = [Move]
                BestEval = Eval
            
            elif Eval == BestEval:
                BestMoves.append(Move)
        
        return random.choice(BestMoves)
    
    def Evaluate(self,BoardDict,PiecesDict,Colour):
        return random.randint(1,20)

class RandomEvaluatorBot(EvaluatorBot):
    def __init__(self):
        EvaluatorBot.__init__(self)

class HoarderEvaluatorBot(EvaluatorBot):
    def __init__(self):
        EvaluatorBot.__init__(self)
    
    def Evaluate(self,BoardDict,PiecesDict,Colour):
        PiecesList = WhitePieceNames  if Colour  == "W" else BlackPieceNames
        TotalPieces = 0

        for PieceName in PiecesList: TotalPieces += len(PiecesDict[PieceName])
        return TotalPieces

class CollectorEvaluatorBot(EvaluatorBot):
    def __init__(self):
        EvaluatorBot.__init__(self)
    
    def Evaluate(self,BoardDict,PiecesDict,Colour):
        PieceValDict = {"K":9999,"Q": 9, "R": 5, "B":3, "N": 3, "P": 1, None:0}
        PeicesList = WhitePieceNames  if Colour  == "W" else BlackPieceNames
        TotalPieceVal = 0

        for PieceName in PeicesList: TotalPieceVal += (len(PiecesDict[PieceName]) * PieceValDict[PieceName[1]])
        return TotalPieceVal

class SpaciousEvaluatorBot(EvaluatorBot):
    def __init__(self):
        EvaluatorBot.__init__(self)
    
    def Evaluate(self,BoardDict,PiecesDict,Colour):
        PeicesList = WhitePieceNames  if Colour  == "W" else BlackPieceNames
        LegalMoves = 0

        for PieceName in PeicesList: 
            for Pos in PiecesDict[PieceName]:
                LegalMoves += len(FindingLegalMoves(Pos, BoardDict))

        return LegalMoves
       
#Comparing Bots

class ComparisonEvaluatorBot(EvaluatorBot):
    def __init__(self):
        EvaluatorBot.__init__(self)
    
    def Choose(self, BoardDict, PiecesDict, Colour, LegalMoves):
        BestEval = None
        BestMoves = []

        for Move in LegalMoves:
             
            NewBoard = MovingAPiece(Move[0],Move[1],BoardDict,PiecesDict)

            Eval = self.Evaluate(NewBoard[0],NewBoard[1],"W") - self.Evaluate(NewBoard[0],NewBoard[1],"B")

            if Colour == "B": Eval *= -1
            
            if BestEval == None:
                BestMoves = [Move]
                BestEval = Eval
                continue
            
            if Eval > BestEval or BestEval == None:
                BestMoves = [Move]
                BestEval = Eval
            
            elif Eval == BestEval:
                BestMoves.append(Move)
        
        return random.choice(BestMoves)
    
class ComparingHoarderBot(ComparisonEvaluatorBot):
    def __init__(self):
        ComparisonEvaluatorBot.__init__(self)
    
    def Evaluate(self,BoardDict,PiecesDict,Colour):
        PeicesList = WhitePieceNames  if Colour  == "W" else BlackPieceNames
        TotalPieces = 0

        for PieceName in PeicesList: TotalPieces += len(PiecesDict[PieceName])
        return TotalPieces

class ComparingCollectorBot(ComparisonEvaluatorBot):
    def __init__(self):
        ComparisonEvaluatorBot.__init__(self)
    
    def Evaluate(self,BoardDict,PiecesDict,Colour):
        PieceValDict = {"K":9999,"Q": 9, "R": 5, "B":3, "N": 3, "P": 1, None:0}
        PeicesList = WhitePieceNames  if Colour  == "W" else BlackPieceNames
        TotalPieceVal = 0

        for PieceName in PeicesList: TotalPieceVal += (len(PiecesDict[PieceName]) * PieceValDict[PieceName[1]])
        return TotalPieceVal

class ComparisonSpaciousBot(ComparisonEvaluatorBot):
    def __init__(self):
        ComparisonEvaluatorBot.__init__(self)
    
    def Evaluate(self,BoardDict,PiecesDict,Colour):
        TimeThing = time.time()

        PeicesList = WhitePieceNames  if Colour  == "W" else BlackPieceNames
        LegalMoves = 0

        for PieceName in PeicesList: 
            for Pos in PiecesDict[PieceName]:
                LegalMoves += len(FindingLegalMoves(Pos, BoardDict))

        return LegalMoves

ListOfEvaluatorBots = [RandomEvaluatorBot,HoarderEvaluatorBot,CollectorEvaluatorBot,SpaciousEvaluatorBot,ComparingHoarderBot,ComparingCollectorBot,ComparisonSpaciousBot]
ListOfEvaluatorBotsWithoutSpacious = [HoarderEvaluatorBot,CollectorEvaluatorBot,ComparingHoarderBot,ComparingCollectorBot]
