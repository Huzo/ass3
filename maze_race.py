class Position:
    def __init__(self):
            self.r = 0
            self.c = 0

    def getC(self):
        return self.c

    def getR(self):
        return self.r

    def setC(self,c):
        self.c = c

    def setR(self,r):
        self.r = r

class Cell:
    def __init__(self):
        self.pos = Position()
        self.content = '*'
        self.explored = 0

    def setExplored(self,value):
        self.explored = value

    def getExplored(self):
        return self.explored

    def setContent(self,content):
        self.content = content

    def getContent(self):
        return self.content

    def setPos(self,pos):
        self.pos = pos

    def getPos(self):
        return self.pos

    def isAvailable(self):
        if(self.content == '*' or self.content == 'O'):
            return 1
        else:
            return 0

class Maze:
    map = []

    def __init__(self):
        self.height = 0
        self.width = 0
        self.destPos = Position()

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def explore(self,pos):
        global map
        col = pos.getC()
        row = pos.getR()
        map[row][col].setExplored(1)

    def getCell(self,pos):
        global map
        col = pos.getC()
        row = pos.getR()
        return map[row][col]

    def setCell(self,pos,cell):
        global map
        col = pos.getC()
        row = pos.getR()
        map[row][col] = cell

    def getCellContent(self,pos):
        global map
        col = pos.getC()
        row = pos.getR()
        return map[col][row].getContent()

    def setCellContent(self,pos,value):
        global map
        col = pos.getC()
        row = pos.getR()
        map[row][col].setContent(value)

    def isAvailable(self,pos):
        global map
        col = pos.getC()
        row = pos.getR()
        if(row < self.getHeight() and col < self.getWidth()):
            if(map[row][col].isAvailable() == 0):
                return -1
            else:
                return 1

        else:
            return 0

    def reachDest(self,pos):
        if(pos.getC() == self.destPos.getC and pos.getR() == self.destPos.getR()):
            return 1
        else:
            return 0

    def displayMaze(self):
        global map
        h = self.getHeight
        w = self.getWidth
        print("Current Maze > \n\n",end='')
        indent = "\t\t\t"
        print(indent+"   |",end='')
        for j in range(w):
            print(" " + j +  " |",end='')
        print("\n"+indent,end='')
        for j in range(w+1):
            print("----",end='')
        print("")
        for i in range(h):
            print(indent+" "+i+" |",end='')
            for j in range(w):
                cell = map[i][j]
                ch = cell.content
                if(cell.getExplored() == 1):
                    if(ch != '*'):
                        print(" "+ch+" |",end='')
                    else:
                        print("   |",end='')
                else:
                    print(" ? |",end='')

            print("\n"+indent,end='')
            for j in range(w+1):
                print("----",end='')
            print("")
        print("\n--")

    def loadMaze(self,fh):
        global map
        f = open(fh)
        s = f.read()
        l = s.split(' ')
        h = l[0]
        w = l[1]

        end_h = 0
        end_w = 0
        coords = [0,0,0,0]
        for i in range(h):
            row = f.read()
            ch = row[i]
            cell = Cell()
            if(ch == 'O'):
                end_h = i
                end_w = j
            else:
                if(ch == '1'):
                    coords[0] = i
                    coords[1] = j
                    ch = 'E'
                else:
                    if(ch == "2"):
                        coords[2] = i
                        coords[3] = j
                        ch = 'H'

            cell.setContent(ch)
            pos = Position()
            pos.setR(i)
            pos.setC(j)
            cell.setPos(pos)
            map[i][j] = cell

        self.height = h
        self.width = w
        self.destPos.setR(end_h)
        self.destPos.setC(end_w)

        self.explore(self.destPos)
        return coords

class Player:
    rshift = [1,0,-1,0]
    cshift = [0,1,0,-1]

    def __init__(self):
        self.name = ""
        self.curPos = Position()
        self.specialMovesLeft = 4

    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name

    def getPos(self):
        return self.curPos

    def occupy(self,maze):
        maze.setCellContent(self.getPos(), self.getName())
        maze.explore(self.getPos())

    def leave(self,maze):
        maze.setCellContent(self.getPos(), '*')
        maze.explore(self.getPos())

    def move(self,pointTo,maze):
        p = self.next(pointTo)
        if(maze.isAvailable(p) == 1):
            self.leave(maze)
            cur_h = self.curPos.getR()
            cur_w = self.curPos.getC()
            self.occupy(maze)
        elif(p.getR() < maze.getHeight() and p.getC() < maze.getWidth()):
            maze.explore(p)

    def next(self,pointTo):
        global rshift
        global cshift
        pos = Position()
        pos.setR(self.getPos().getR()+rshift[pointTo])
        pos.setC(self.getPos().getC()+cshift[pointTo])
        return pos

    def rush(self,pointTo,maze):
        self.move(pointTo, maze)
        pos = self.next(pointTo)
        while(pos.getR() < maze.getHeight() and pos.getC() < maze.getWidth()):
            if(maze.isAvailable(pos) == 1):
                self.move(pointTo,maze)
                pos = self.next(pointTo)
            else:
                break
        if(pos.getR() < maze.getHeight() and pos.getC() < maze.getWidth()):
            maze.explore(pos)

    def throughBlocked(self,pointTo,maze):
        global cshift
        global rshift
        pos = self.getPos()
        c = pos.getC()
        c = pos.getR()

        if(c + (2 * cshift[pointTo]) < maze.getWidth() and r + (2 * rshift[pointTo]) < maze.getHeight()):
            tmp_p = Position()
            tmp_p.setR(r + rshift[pointTo])
            tmp_p.setC(c + cshift[pointTo])
            tmp_content = maze.getCellContent(tmp_p)
            maze.setCellContent(tmp_p, '*')
            self.move(pointTo, maze)
            self.move(pointTo, maze)
            maze.setCellContent(tmp_p, tmp_content)

    def teleport(self,maze):
        import random
        row = random.randint(0,maze.getHeight())
        col = random.randint(0,maze.getWidth())
        pos = Position()
        pos.setR(row)
        pos.setC(col)
        if(maze.getCellContent(pos) == '*'):
            self.leave(maze)
            self.curPos.setR(row)
            self.curPos.setC(col)
            self.occupy(maze)
        else:
            maze.explore(pos)

    def makeMove(self,maze):
        p_name = self.getName()
        if(self.specialMovesLeft < 0):
            print("Your (Player "+p_name+") moving type: normal move.")
            print("Your (Player "+p_name+") moving direction (0: S, 1:E, 2: N, 3: W).")
            d = input()
            while(d != '0' and d != '1' and d != '2' and d != '3'):
                print("The moving direction can only be 0, 1, 2, or 3, please re-input > ",end='')
                d = input()
            d = int(d)
            self.move(d,maze)
        else:
            scnt = self.specialMovesLeft
            if(scnt > 1):
                print("You (Player "+p_name+") can make a normal move (unlimited) or a special move (only "+scnt+" times left).")
            else:
                print("You (Player "+p_name+") can make a normal move or a special move (only "+scnt+" time left).")
            print("Your (Player "+p_name+") moving type (0: rush, 1: through-blocked, 2: teleport, default: normal move) > ",end='')
            op = input()

            if(op == ""):
                op = "-1"
            op = int(op)

            if(op == 2):
                self.teleport(maze)
                self.specialMovesLeft = self.specialMovesLeft - 1
            else:
                print("Your (Player "+p_name+") moving direction (0: S, 1: E, 2: N, 3: W) > ",end="")
                d = input()

                while(d != "0" and d != "1" and d != "2" and d != "3"):
                    print("The moving direction can only be 0, 1, 2, or 3, please re-input >",end='')
                    d = input()
                d = int(d)

                if(op == -1):
                    self.move(d,maze)
                else:
                    if(op == 0):
                        self.rush(d,maze)
                    else:
                        self.throughBlocked(d,maze)
                    self.specialMovesLeft = self.specialMovesLeft - 1

class MazeRace:
    def __init__(self, fileName):
        maze = Maze()
        p1 = Player()
        p2 = Player()

        p1.setName('E')
        p2.setName('H')
        fh = open(fileName,"r")
        coords = maze.loadMaze(fh)

        p1.getPos().setR(int(coords[0]))
        p1.getPos().setC(int(coords[1]))
        p2.getPos().setR(int(coords[2]))
        p2.getPos().setC(int(coords[3]))

        maze.explore(p1.getPos())
        maze.explore(p2.getPos())

        self.maze = maze
        self.p1 = p1
        self.p2 = p2

    def start(self):
        maze = self.maze
        maze.displayMaze()

        pArr = [self.p1, self.p2]
        turn = 0
        finished = 0
        while(finished == 0):
            pArr[turn].makeMove(maze)
            maze.displayMaze()
            if(maze.reachDest(pArr[turn].getPos())):
                i = turn + 1
                print("\n--\nPlayer"+i+" wins! ")
                finished = 1
            turn = (turn + 1) % 2

if __name__ == "__main__":
    config_file = "maze.test"
    game = MazeRace(config_file)
    game.start()






























