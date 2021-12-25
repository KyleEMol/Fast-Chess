import random
import time
import os 
import csv

ZAxis = ["_","=","~"]
WAxis = ["{{","{}","}}"]
XAxis = ["A","B","C","YD","E","F","G","H"]
YAxis = ["1","2","3","4","5","6","7","8"]

ZAxisNums = [1000,2000,3000]
WAxisNums = [100,200,300]
YAxisNums = [10,20,30,40,50,60,70,80]
XAxisNums = [1,2,3,4,5,6,7,8]

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def BoardBoundsChecker(Position):
    if Position < 1111 or Position > 3388:
        return False
    Position = str(Position)
    return ((0<int(Position[0])<4) and (0<int(Position[1])<4) and (0<int(Position[2])<9) and (0<int(Position[3])<9))


def FillingBoard(PiecesDict):
    BoardDict = {}
    
    for Key in PiecesDict:
        for Position in PiecesDict[Key]:
            BoardDict[Position] = Key

    return BoardDict

def MakingInitalDict():
    PiecesDict = {"WP":set([]),"WR":set([]),"WN":set([]),"WB":set([]),"WQ":set([]),"WK":set([]), "BP":set([]),"BR":set([]),"BN":set([]),"BB":set([]),"BQ":set([]),"BK":set([])}
    for ZLevel in ZAxisNums:
        for WLevel in WAxisNums:
            for XLevel in XAxisNums:
                PiecesDict["WP"].add(ZLevel + WLevel + 20 + XLevel)
                PiecesDict["BP"].add(ZLevel + WLevel + 70 + XLevel)

            PiecesDict["WR"].add(ZLevel + WLevel + int("1" +"8" ))
            PiecesDict["WR"].add(ZLevel + WLevel + int("1" +"1" ))
            PiecesDict["WN"].add(ZLevel + WLevel + int("1" +"7" ))
            PiecesDict["WN"].add(ZLevel + WLevel + int("1" +"2" ))
            PiecesDict["WB"].add(ZLevel + WLevel + int("1" +"6" ))
            PiecesDict["WB"].add(ZLevel + WLevel + int("1" +"3" ))
            PiecesDict["WQ"].add(ZLevel + WLevel + int("1" +"4" ))
            PiecesDict["WK"].add(ZLevel + WLevel + int("1" +"5" ))
            
            PiecesDict["BR"].add(ZLevel + WLevel + int("8" + "8"))
            PiecesDict["BR"].add(ZLevel + WLevel + int("8" + "1"))
            PiecesDict["BN"].add(ZLevel + WLevel + int("8" + "7"))
            PiecesDict["BN"].add(ZLevel + WLevel + int("8" + "2"))
            PiecesDict["BB"].add(ZLevel + WLevel + int("8" + "6"))
            PiecesDict["BB"].add(ZLevel + WLevel + int("8" + "3"))
            PiecesDict["BQ"].add(ZLevel + WLevel + int("8" + "4"))
            PiecesDict["BK"].add(ZLevel + WLevel + int("8" + "5"))
    
    return PiecesDict

def MakingStartingPos():
    Dicts = MakingInitalDict()
    BoardDict = FillingBoard(Dicts)
    return (BoardDict , Dicts)

def FindingLegalMoves(Pos,BoardDict):
    #YU - Up, YD - Down, XL - Left, XR - Right, WU - Up in W Axis, WD - Down in W Axis, ZL - Left in Z Axis, ZR - Right in Z Axis
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000
    LegalDestinations = set([])
    PieceType = BoardDict[Pos]

    if PieceType[-1] == "P":
        LegalDirections = [YU] if PieceType == "WP" else [YD]
        LegalDirections += [WU, WD, ZL, ZR]
        
        for Direction in LegalDirections:
            if not BoardBoundsChecker(Pos+Direction):continue

            if not BoardDict.get(Pos+Direction):
                LegalDestinations.add(Pos+Direction)
        
        if (str(Pos)[-2] == "2" and PieceType[0] == "W") or (str(Pos)[-2] == "7" and PieceType[0] == "B"):
            for Direction in LegalDirections:
                if not BoardBoundsChecker(Pos+(Direction*2)):continue

                if not BoardDict.get(Pos+Direction) and not BoardDict.get(Pos+(Direction*2)):
                    LegalDestinations.add(Pos+(Direction*2))

        AttackingDirections = LegalDirections + [XL,XR]
        for Direction in AttackingDirections:
            for Direction2 in AttackingDirections:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                if BoardDict.get(Pos+Direction+Direction2) == None:continue
                if not BoardBoundsChecker(Pos+Direction):continue

                if BoardDict.get(Pos+Direction+Direction2)[0] != PieceType[0]:
                    LegalDestinations.add(Pos+Direction+Direction2)

    elif PieceType[-1] == "B":

        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                Diff = Direction + Direction2
                LoopNum = 1 

                while True:
                    Diff = LoopNum*(Direction + Direction2)
                    if not  BoardBoundsChecker(Pos+Diff):break
                    LoopNum += 1 
                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                    break
    
    elif PieceType[-1] == "N":

        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                Diff = Direction + (Direction2 * 2)

                if BoardBoundsChecker(Pos + Diff):
                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                    elif BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
    
    elif PieceType[-1] == "R":
        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                LoopNum = 1 
                Diff = Direction
                while BoardBoundsChecker(Pos + Diff): 

                    Diff = LoopNum*Direction
                    LoopNum += 1 

                    if BoardDict.get(Pos+Diff) == None :
                        if BoardBoundsChecker(Pos + Diff):
                            LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                    break

    elif PieceType[-1] == "Q":
        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                LoopNum = 1 
                Diff = Direction
                while True:
                    Diff = LoopNum*Direction
                    LoopNum += 1 
                    if not BoardBoundsChecker(Pos+Diff):
                        break

                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                    break

        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                Diff = Direction + Direction2
                LoopNum = 1 

                while True:
                    Diff = LoopNum*(Direction + Direction2)
                    LoopNum += 1 

                    if not BoardBoundsChecker(Pos+Diff):
                        break

                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                    
                    break

    elif PieceType[-1] == "K":

        for Direction in [YU, YD, XL, XR]:
            Diff = Direction 
            if BoardBoundsChecker(Pos + Diff):
                if BoardDict.get(Pos+Diff) == None:
                    LegalDestinations.add(Pos+Diff)
                    continue
                if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                    LegalDestinations.add(Pos+Diff)

        for Direction in [YU, YD, XL, XR]:
            for Direction2 in [YU, YD, XL, XR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                Diff = Direction + Direction2
                if  BoardBoundsChecker(Pos + Diff):
                    Diff = (Direction + Direction2)

                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)

    return LegalDestinations

def FindingLegalMovesAttackedAndDefended(Pos,BoardDict):
    #YU - Up, YD - Down, XL - Left, XR - Right, WU - Up in W Axis, WD - Down in W Axis, ZL - Left in Z Axis, ZR - Right in Z Axis
    YU, YD, XL, XR, WU, WD, ZL, ZR = 10,-10,1,-1,100,-100,1000,-1000
    LegalDestinations = set([])
    AttackedPieces = set([])
    DefendedPieces = set([])

    PieceType = BoardDict[Pos]

    if PieceType[-1] == "P":
        LegalDirections = [YU] if PieceType == "WP" else [YD]
        LegalDirections += [WU, WD, ZL, ZR]
        
        for Direction in LegalDirections:
            if not BoardDict.get(Pos+Direction) and BoardBoundsChecker(Pos+Direction):
                LegalDestinations.add(Pos+Direction)
        
        if (str(Pos)[-2] == "2" and PieceType[0] == "W") or (str(Pos)[-2] == "7" and PieceType[0] == "B"):
            for Direction in LegalDirections:
                if not BoardDict.get(Pos+Direction) and not BoardDict.get(Pos+(Direction*2))and BoardBoundsChecker(Pos+Direction):
                    LegalDestinations.add(Pos+(Direction*2))

        for Direction in [XL, XR, WU, WD, ZL, ZR]:
            for Direction2 in [XL, XR, WU, WD, ZL, ZR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                if BoardDict.get(Pos+Direction+Direction2) == None:continue
                if BoardDict.get(Pos+Direction+Direction2)[0] != PieceType[0]:
                    LegalDestinations.add(Pos+Direction+Direction2)
                    AttackedPieces.add(Pos+Direction+Direction2) 

                elif BoardDict.get(Pos+Direction+Direction2)[0] == PieceType[0] :
                    DefendedPieces.add(Pos+Direction+Direction2) 

    elif PieceType[-1] == "B":

        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                Diff = Direction + Direction2
                LoopNum = 1 

                while BoardBoundsChecker(Pos + Diff):
                    Diff = LoopNum*(Direction + Direction2)
                    LoopNum += 1 

                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                        AttackedPieces.add(Pos+Diff)
                    else:
                        DefendedPieces.add(Pos+Diff)
                    break
    
    elif PieceType[-1] == "N":

        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                Diff = Direction + (Direction2 * 2)

                if BoardBoundsChecker(Pos + Diff):
                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue
                    if BoardDict.get(Pos+Diff)[0] != PieceType[0] :
                        LegalDestinations.add(Pos+Diff)
                        AttackedPieces.add(Pos+Diff)
                    else:
                        DefendedPieces.add(Pos+Diff)

    elif PieceType[-1] == "R":
        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                LoopNum = 1 
                Diff = Direction
                while BoardBoundsChecker(Pos + Diff): 
                    Diff = LoopNum*Direction
                    LoopNum += 1 

                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                        AttackedPieces.add(Pos+Diff)
                    else:
                        DefendedPieces.add(Pos+Diff)
                    break

    elif PieceType[-1] == "Q":
        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                LoopNum = 1 
                Diff = Direction
                while BoardBoundsChecker(Pos + Diff):
                    Diff = LoopNum*Direction
                    LoopNum += 1 

                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                        AttackedPieces.add(Pos+Diff)
                    else:
                        DefendedPieces.add(Pos+Diff)
                    break

        for Direction in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
            for Direction2 in [YU, YD, XL, XR, WU, WD, ZL, ZR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                Diff = Direction + Direction2
                LoopNum = 1 

                while BoardBoundsChecker(Pos + Diff):
                    Diff = LoopNum*(Direction + Direction2)
                    LoopNum += 1 

                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                        AttackedPieces.add(Pos+Diff)
                    else:
                        DefendedPieces.add(Pos+Diff)

                    break

    elif PieceType[-1] == "K":

        for Direction in [YU, YD, XL, XR]:
            Diff = Direction 
            if BoardBoundsChecker(Pos + Diff):
                if BoardDict.get(Pos+Diff) == None:
                    LegalDestinations.add(Pos+Diff)
                    continue

                if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                    LegalDestinations.add(Pos+Diff)
                    AttackedPieces.add(Pos+Diff)
                else:
                    DefendedPieces.add(Pos+Diff)

        for Direction in [YU, YD, XL, XR]:
            for Direction2 in [YU, YD, XL, XR]:
                if Direction + Direction2 == 0 or Direction == Direction2:continue
                Diff = Direction + Direction2
                if  BoardBoundsChecker(Pos + Diff):
                    Diff = (Direction + Direction2)

                    if BoardDict.get(Pos+Diff) == None:
                        LegalDestinations.add(Pos+Diff)
                        continue

                    if BoardDict.get(Pos+Diff)[0] != PieceType[0]:
                        LegalDestinations.add(Pos+Diff)
                        AttackedPieces.add(Pos+Diff)
                    else:
                        DefendedPieces.add(Pos+Diff)
    
    NewLegalDest = set([])
    for Dest in LegalDestinations:
        if not BoardBoundsChecker(Dest):
            print("Issue With",PieceType)
        else:NewLegalDest.add(Dest)

    return (NewLegalDest,AttackedPieces,DefendedPieces)

def DisplayingBoard(BoardDict,Wait = 0,LastMove = None):
    #https://unicode-table.com/en/sets/chess-symbols/
    NameUnicodeDict = {"WK":"\u2654","WQ":"\u2655","WR":"\u2656","WB":"\u2657","WN":"\u2658","WP":"\u2659","BK":"\u265A","BQ":"\u265B","BR":"\u265C","BB":"\u265D","BN":"\u265E","BP":"\u265F"}

    DispBoard = [[[[ " " for Y in range(8)] for X in range(8)] for W in range(3)] for Z in range(3)]
    for Key in BoardDict:
        TempKey = str(Key)
        while len(TempKey) < 4:TempKey = "0" + TempKey
        DispBoard[int(TempKey[0])-1][int(TempKey[1])-1][int(TempKey[2])-1][int(TempKey[3])-1] = NameUnicodeDict[BoardDict[Key]]
    
    if LastMove != None:DispBoard[int(LastMove[0])-1][int(LastMove[1])-1][int(LastMove[2])-1][int(LastMove[3])-1] = "X"

    os.system('cls')

    print("="*126)
    for BoardRow in DispBoard:
        TempBoard = []
        for y in range(8):
            DispRow = [TwoDBoard[y] for TwoDBoard in BoardRow]
            #DispRow.insert(1,"||")
            #DispRow.insert(3,"||")
            TempBoard.append(DispRow)
        for Row in TempBoard[::-1]:print(Row)
        print("="*126)
    
    time.sleep(Wait)

def DisplayingLegalMoves(PiecePosition,BoardDict, PiecesDict = None):
    #https://unicode-table.com/en/sets/chess-symbols/
    NameUnicodeDict = {"WK":"\u2654","WQ":"\u2655","WR":"\u2656","WB":"\u2657","WN":"\u2658","WP":"\u2659","BK":"\u265A","BQ":"\u265B","BR":"\u265C","BB":"\u265D","BN":"\u265E","BP":"\u265F"}
    DispBoard = [[[[ " " for Y in range(8)] for X in range(8)] for W in range(3)] for Z in range(3)]

    if PiecesDict == None:
        for Key in BoardDict:
            TempKey = str(Key)
            DispBoard[int(TempKey[0])-1][int(TempKey[1])-1][int(TempKey[2])-1][int(TempKey[3])-1] = NameUnicodeDict[BoardDict[Key]]
    else:
        for Key in PiecesDict:
            for Pos in PiecesDict[Key]:
                Pos = str(Pos)
                Piece = Key
                DispBoard[int(Pos[0])-1][int(Pos[1])-1][int(Pos[2])-1][int(Pos[3])-1] = NameUnicodeDict[Piece]
    
    LegalMoves = FindingLegalMoves(PiecePosition,BoardDict)

    for Pos in LegalMoves:
        DispBoard[int(Pos[0])-1][int(Pos[1])-1][int(Pos[2])-1][int(Pos[3])-1] = "X"

    os.system('cls')

    print("="*126)
    for BoardRow in DispBoard:
        for y in range(8):
            DispRow = [TwoDBoard[y] for TwoDBoard in BoardRow]
            #DispRow.insert(1,"||")
            #DispRow.insert(3,"||")
            print(DispRow)
        print("="*126)

def ConvertingPosToCoords(Pos):
    TempPos = str(Pos) 
    Pos = ""
    for Char in range(len(TempPos)):
        Pos += str(int(TempPos[Char])-1)
    Y = ["A","B","C","YD","E","F","G","H"]
    X = ["1","2","3","4","5","6","7","8"]
    W = ["[[","[]","]]"]
    Z = ["~","-","_"]


    return Z[int(Pos[0])] + W[int(Pos[1])]  + Y[int(Pos[3])] + X[int(Pos[2])]

def MovingAPiece(StartingSquare,FinalSquare,BoardDict,PiecesDict):
    PieceName = BoardDict[StartingSquare]

    NewBoardDict = BoardDict.copy()
    NewPiecesDict = {}
    for Key in PiecesDict:
        NewPiecesDict[Key] = PiecesDict[Key].copy()
    
    if not(NewBoardDict.get(FinalSquare)):
        NewBoardDict[FinalSquare] = NewBoardDict[StartingSquare]
        NewPiecesDict[PieceName].remove(StartingSquare)
        NewPiecesDict[PieceName].add(FinalSquare)    

    else:
        OpponentPiece = NewBoardDict[FinalSquare]
        if PieceName[0] == OpponentPiece[0]:
            return None

        NewPiecesDict[OpponentPiece].remove(FinalSquare)
        NewBoardDict[FinalSquare] = NewBoardDict[StartingSquare]
        NewPiecesDict[PieceName].remove(StartingSquare)
        NewPiecesDict[PieceName].add(FinalSquare)   
            
    NewBoardDict.pop(StartingSquare)

    return (NewBoardDict,NewPiecesDict)


