#ChessBots
import random 
import numpy as np
from Board import *

global WhitePieceNames
global BlackPieceNames

WhitePieceNames = ["WP","WR","WN","WB","WQ","WK"]
BlackPieceNames = ["BP","BR","BN","BB","BQ","BK"]

def CalculatingRatingChange(Player1Elo,Player2Elo,NumberOfGames,Player1Wins,KVal = 25):
    #Results are from player one's perspectve 
    Player1Elo = int(Player1Elo)
    Player2Elo = int(Player2Elo)

    Player1ExpectedScore = NumberOfGames/(1 + (8**((Player2Elo-Player1Elo)/400)))

    Player1RatingChange = KVal*(Player1Wins - Player1ExpectedScore)

    Player2ExpectedScore =  NumberOfGames/(1 + (8**((Player1Elo-Player2Elo)/400)))

    Player2RatingChange = KVal*((NumberOfGames-Player1Wins) - Player2ExpectedScore)

    return (round(Player1Elo + Player1RatingChange,2),round(Player2Elo + Player2RatingChange,2))

class BasicBot():
    def __init__(self, Rating = 1000):
        self.Rating = Rating
        self.Name = type(self).__name__
    
    def CalculatingGlickoVals(self):
        self.GlickoRating = round((self.Rating-1500)/173.7178,4)
        self.GlickoRD = round(self.RatingDistribution/173.7178,4)
    
    def RandomMoves(self,BoardDict ,PiecesDict, Colour):

        ListOfNames = WhitePieceNames if Colour == "W" else BlackPieceNames
        Pieces = []
        for Key in ListOfNames:Pieces += list(PiecesDict[Key])

        random.shuffle(Pieces)
        for Piece in Pieces:
            Moves = FindingLegalMoves(Piece,BoardDict)
            if len(Moves) > 0: 
                return (Piece,random.choice(list(Moves)))
    
    def Move(self,BoardDict ,PiecesDict, Colour):
        return self.RandomMoves(BoardDict ,PiecesDict, Colour)

"""
Decision Bots
"""

class DecisionBot(BasicBot):
    def __init__(self):
        BasicBot.__init__(self)

class RandomMoveBot(DecisionBot):
    def __init__(self):
        BasicBot.__init__(self)
    
    def Choose(self,BoardDict, LegalMoves, PiecesDict,  Colour):
        
        return random.choice(LegalMoves)

class BountyHunter(DecisionBot):
    def __init__(self):
        DecisionBot.__init__(self)
    
    def Choose(self,BoardDict, LegalMoves, PiecesDict,  Colour):
        if len(LegalMoves) == 1:return LegalMoves[0]

        PieceValDict = {"K":99999,"Q": 9, "R": 5, "B":3, "N": 3, "P": 1, None:0}
        BestMoveList = []
        BestMoveVal = None
        for Move in LegalMoves:
            MoveVal = PieceValDict[BoardDict.get(Move[1],[0,None])[1]]

            if BestMoveVal == None:
                BestMoveVal = MoveVal
                BestMoveList = [Move]
                continue
            
            if MoveVal>BestMoveVal:
                BestMoveList = [Move]
                BestMoveVal = MoveVal
            
            elif MoveVal == BestMoveVal:
                BestMoveList.append(Move)
        
        
        return random.choice(BestMoveList)

class Bully(DecisionBot):
    def __init__(self):
        DecisionBot.__init__(self)
    
    def Choose(self,BoardDict, LegalMoves, PiecesDict,  Colour):
        if len(LegalMoves) == 1:return LegalMoves[0]

        PieceValDict = {"K":99999,"Q": 9, "R": 5, "B":3, "N": 3, "P": 1, None:999999}
        
        BestMoveList = []
        BestMoveVal = None
        for Move in LegalMoves:
            MoveVal = PieceValDict[BoardDict.get(Move[1],[0,None])[1]]

            if BestMoveVal == None:
                BestMoveVal = MoveVal
                BestMoveList = [Move]
                continue

            if MoveVal < BestMoveVal:
                BestMoveList = [Move]
                BestMoveVal = MoveVal
            
            elif MoveVal == BestMoveVal:
                BestMoveList.append(Move)
        
        return random.choice(BestMoveList)

ListOfDecisionBots = [RandomMoveBot,BountyHunter,Bully]

"""
Filter Bots
"""

class FilterBot(BasicBot):
    def __init__(self,DecisionBot = RandomMoveBot):
        BasicBot.__init__(self)

        if DecisionBot != None:
            self.DecisionBot = DecisionBot()
        else:
            self.DecisionBot = None
        self.Name = self.Name +" "+ (self.DecisionBot.Name if self.DecisionBot != None else "")

class NoFilter(FilterBot):
    def __init__(self,DecisionBot = RandomMoveBot):
        FilterBot.__init__(self,DecisionBot)

    def Move(self, BoardDict, PiecesDict,  Colour):
        Pieces = set([])

        PieceNames = BlackPieceNames if Colour == "B" else WhitePieceNames

        for Key in PieceNames:
            Pieces.update(PiecesDict[Key])
        
        LegalMoves = []

        for Piece in Pieces:
            PieceLegalMoves = FindingLegalMoves(Piece,BoardDict)
            for Move in PieceLegalMoves:
                LegalMoves.append((Piece,Move))
        
        if len(LegalMoves) == 0:
            return None
        
        if self.DecisionBot == None:
            return LegalMoves
        return self.DecisionBot.Choose(BoardDict = BoardDict, LegalMoves = LegalMoves, PiecesDict = PiecesDict,  Colour = Colour)
class Pacifist(FilterBot):
    def __init__(self,DecisionBot = RandomMoveBot):
        FilterBot.__init__(self,DecisionBot)
    
    def Move(self, BoardDict, PiecesDict,  Colour):
        
        WhitePieces = set([])
        BlackPieces = set([])

        for Key in WhitePieceNames:
            WhitePieces.update(PiecesDict[Key])

        for Key in BlackPieceNames:
            BlackPieces.update(PiecesDict[Key])
        
        ChosenMoves = []
 
        Pieces = WhitePieces if Colour == "W" else BlackPieces

        OtherPieces = WhitePieces if Colour == "B" else BlackPieces


        for Piece in Pieces:
            LegalMoves = FindingLegalMoves(Piece,BoardDict)
            
            for Move in LegalMoves:
                if Move not in OtherPieces:
                    ChosenMoves.append((Piece, Move))
        
        if len(ChosenMoves) == 0:
            return self.RandomMoves(BoardDict,PiecesDict,Colour)

        return self.DecisionBot.Choose(BoardDict = BoardDict, LegalMoves = ChosenMoves, PiecesDict = PiecesDict,  Colour = Colour)
class WarmongerBot(FilterBot):
    def __init__(self,DecisionBot = RandomMoveBot):
        FilterBot.__init__(self,DecisionBot)
    
    def Move(self, BoardDict, PiecesDict,  Colour):

        WhitePieces = set([])
        BlackPieces = set([])

        for Key in WhitePieceNames:
            WhitePieces.update(PiecesDict[Key])

        for Key in BlackPieceNames:
            BlackPieces.update(PiecesDict[Key])

        ChosenMoves = []
        Pieces = WhitePieces if Colour == "W" else BlackPieces
        OtherPieces = WhitePieces if Colour == "B" else BlackPieces

        for Piece in Pieces:
            LegalMoves = FindingLegalMoves(Piece,BoardDict)
            
            for Move in LegalMoves:
                if Move in OtherPieces:
                    ChosenMoves.append((Piece, Move))

        if len(ChosenMoves) == 0:
            return self.RandomMoves(BoardDict,PiecesDict,Colour)

        LegalMoves = ChosenMoves 

        if len(LegalMoves) == 0: return None

        return self.DecisionBot.Choose(BoardDict = BoardDict, LegalMoves = LegalMoves, PiecesDict = PiecesDict,  Colour = Colour)

class ChampionBot(FilterBot):
    def __init__(self,DecisionBot = RandomMoveBot):
        FilterBot.__init__(self,DecisionBot)
        self.Champion = None
    
    def Move(self, BoardDict, PiecesDict, Colour):
        PieceNames = WhitePieceNames if Colour == "W" else BlackPieceNames
        OwnPieces = []
        LegalMoves = set([])
        for Name in PieceNames:OwnPieces += PiecesDict[Name]

        if self.Champion != None:
            if  self.Champion not in OwnPieces:
                self.Champion = None
            
            else:
                LegalMoves = FindingLegalMoves(self.Champion,BoardDict)
                if len(LegalMoves) == 0:
                    self.Champion = None


        while self.Champion == None:
            self.Champion = random.choice(OwnPieces)
            OwnPieces.remove(self.Champion)
            LegalMoves = FindingLegalMoves(self.Champion,BoardDict)

            if len(LegalMoves) == 0:
                self.Champion = None
        
        LegalMoves = [[self.Champion,Move] for Move in LegalMoves]

        return self.DecisionBot.Choose(BoardDict = BoardDict, LegalMoves = LegalMoves, PiecesDict = PiecesDict,  Colour = Colour)

class OnePiecePusher(FilterBot):
    def __init__(self,PieceName,DecisionBot = RandomMoveBot):
        FilterBot.__init__(self,DecisionBot)
        self.PieceName = PieceName

    def Move(self, BoardDict, PiecesDict,  Colour):
        
        Pieces = PiecesDict[Colour + self.PieceName]
        NoPieces = False 
        
        if len(Pieces) == 0:
            NoPieces = True
        
        if NoPieces:return self.RandomMoves(BoardDict, PiecesDict,Colour =  Colour)

        LegalMoves = []

        for Piece in Pieces:
            for LegalMove in FindingLegalMoves(Piece,BoardDict):
                LegalMoves.append([Piece,LegalMove])
        
        if len(LegalMoves) == 0:
            return self.RandomMoves(BoardDict,PiecesDict,Colour)
        
        elif len(LegalMoves) == 1:
            return LegalMoves[0]
        return self.DecisionBot.Choose(BoardDict = BoardDict, LegalMoves = LegalMoves, PiecesDict = PiecesDict,  Colour = Colour)       

class PawnPusher(OnePiecePusher):
    def __init__(self,DecisionBot = RandomMoveBot):
        OnePiecePusher.__init__(self,"P",DecisionBot)

class KnightKnocker(OnePiecePusher):
    def __init__(self,DecisionBot = RandomMoveBot):
        OnePiecePusher.__init__(self,"N",DecisionBot)

class BishopBudger(OnePiecePusher):
    def __init__(self,DecisionBot = RandomMoveBot):
        OnePiecePusher.__init__(self,"B",DecisionBot)

class RookRelocator(OnePiecePusher):
    def __init__(self,DecisionBot = RandomMoveBot):
        OnePiecePusher.__init__(self,"R",DecisionBot)

class QueenQuarreler(OnePiecePusher):
    def __init__(self,DecisionBot = RandomMoveBot):
        OnePiecePusher.__init__(self,"Q",DecisionBot)

class KingKicker(OnePiecePusher):
    def __init__(self,DecisionBot = RandomMoveBot):
        OnePiecePusher.__init__(self,"K",DecisionBot)


ListOfFilterBots = [NoFilter,Pacifist,WarmongerBot,ChampionBot,PawnPusher,KnightKnocker,BishopBudger,RookRelocator,QueenQuarreler,KingKicker]
ListOfFilterBotsWithoutPacifist = [NoFilter,WarmongerBot,ChampionBot,PawnPusher,KnightKnocker,BishopBudger,RookRelocator,QueenQuarreler,KingKicker]
""" 
Misc Bots
"""

class Human(BasicBot):
    def __init__(self):
        BasicBot.__init__(self)
    
    def Move(self, BoardDict, PiecesDict,  Colour):
        
        ColourDict = {"W":"White", "B": "Black"}
        PieceNameDict = {"K":"King", "Q":"Queen","R":"Rook", "N":"Knight","B":"Bishop", "P":"Pawn"}

        while True:
            StartingPiece = int(input("What is the coordinate of the piece that you want to move?"))

            PieceName = BoardDict.get(StartingPiece)
            if PieceName == None:
                print("There is no Piece at", StartingPiece)
                continue
            LegalMoves = FindingLegalMoves(StartingPiece,BoardDict)

            while True:
                Move = int(input("Where do you want to move the "+ ColourDict.get(PieceName[0])+" " + PieceNameDict.get(StartingPiece[1])))

                if Move in LegalMoves: return (StartingPiece,Move)

                print("That wasn't a valid Move")
                if input("Do you want to keep moving" +  ColourDict.get(PieceName[0])+ " " + PieceNameDict.get(StartingPiece[1]) + "(y/n)") in ["Y","y"]:break
        
class NothingBot(BasicBot):
    def __init__(self):
        BasicBot.__init__(self)
    
    def Move(self, BoardDict, PiecesDict,  Colour):
        for King in PiecesDict[Colour+"K"]:
            return (King,King)
