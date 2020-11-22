import pygame as pg
import networkx as nx
#9import randon as rd
from collections import deque
from tkinter import *
from tkinter import messagebox
##################### CLASSES TIME ########################
class Player():
    def __init__(self, indexX, indexY, lenghtStep, name, color, numBoxes):
        self.firstX = indexX
        self.firstY = indexY
        self.indexX =indexX
        self.indexY = indexY
        self.name = name
        self.lenghtStep = lenghtStep
        self.lenghtSpace = self.lenghtStep / 5
        self.name = name
        self.coordX = ((self.indexX * self.lenghtSpace) + (self.lenghtStep * (self.indexX - 0.5)))
        self.coordY = ((self.indexY * self.lenghtSpace) + (self.lenghtStep * (self.indexY - 0.5)))
        self.colorPlayer = color
        #self.victory = v
        #
        cvic = 0
        difX, difY = self.firstX - 1, self.firstY - 1  
        if(self.firstX == (numBoxes//2)+1 and difY == 0):
            cvic = [1,numBoxes] # [y,numBoxes]
        elif(self.firstX == (numBoxes//2)+1 and difY > 0):
            cvic = [1,1] # [y, 1]
        elif(self.firstY == (numBoxes//2)+1 and difX == 0):
            cvic = [0,numBoxes] # [x, numBoxes]
        elif(self.firstY == (numBoxes//2)+1 and difX > 0):
            cvic = [0,1] # [x, 1]
        self.victory = cvic

    def drawPlayer(self, window):
        pg.draw.circle(window, self.colorPlayer, (int(self.coordX), int(self.coordY)), int(self.lenghtStep / 4))
    def movePlayer(self, indexX, indexY):
        self.indexX = indexX
        self.indexY = indexY
        self.coordX = ((self.indexX * self.lenghtSpace) + (self.lenghtStep * (self.indexX - 0.5)))
        self.coordY = ((self.indexY * self.lenghtSpace) + (self.lenghtStep * (self.indexY - 0.5)))
    def stablishNode(self, g):
        for node,info in g.nodes(data = True):
            if(info['indexX'] == self.indexX and info['indexY'] == self.indexY):
                return node


class Wall():
    def __init__(self, AindexX, AindexY, BindexX, BindexY):
        cn = [0,0] 
        difX = AindexX - BindexX
        difY = AindexY - BindexY
        self.typeWall = bool(difX) #FALSE = HORIZONTAL, TRUE = VERTICAL
        if(difX == -1 or difY == -1):
            cn = [AindexX, AindexY]
        elif(difX == 1 or difY == 1):
            cn = [BindexX, BindexY]
        self.closestNode = cn
        self.nodesBlocked = [[AindexX,AindexY],[BindexX,BindexY]]
    def drawWall(self, window, color, lenghtBox):
        space = lenghtBox/5
        cx = (self.closestNode[0] * space) + (lenghtBox * (self.closestNode[0]-1))
        cy = (self.closestNode[1] * space) + (lenghtBox * (self.closestNode[1]-1))
        major,minor = lenghtBox,(space/2)
        if(self.typeWall == True):
            pg.draw.rect(window,color,[cx + lenghtBox + (minor/2),cy,minor,major])
        else:
            pg.draw.rect(window,color,[cx,cy + lenghtBox + (minor/2),major,minor])

class Box():
    def __init__(self, coordX, coordY, indexX, indexY):
        self.coordX = coordX
        self.coordY = coordY
        self.indexX = indexX
        self.indexY = indexY
    def drawBox(self, window, color, lenghtBox):
        pg.draw.rect(window, color, [self.coordX, self.coordY, lenghtBox, lenghtBox])

class TableGraph():
    def __init__(self, numberBoxes):
        self.matchGraph = nx.Graph()
        self.numberBoxes = numberBoxes
        self.generateGraph()
    def generateGraph(self): #generar el grafo correspondiente al tablero
        for i in range(self.numberBoxes**2):
            numberNode = i + 1
            idx, idy = 0,0
            if(numberNode % self.numberBoxes == 0):
                idx = self.numberBoxes
                idy = int(numberNode//self.numberBoxes)
            else:
                idx = int(numberNode - ((numberNode//self.numberBoxes)*self.numberBoxes))
                idy = int((numberNode//self.numberBoxes)+1)
            self.matchGraph.add_node(numberNode, indexX = idx, indexY = idy, visited=[], id= numberNode)
        
        for numNode in range(1,(self.numberBoxes**2)+1):
            actualNode = self.matchGraph.nodes[numNode]
            if (numNode+1<((self.numberBoxes**2)+1)):
                nodeNext = self.matchGraph.nodes[numNode+1]
                if(actualNode['indexY']==nodeNext['indexY']):
                    self.matchGraph.add_edge(numNode, numNode + 1, nodes=[[actualNode['indexX'],actualNode['indexY']],[nodeNext['indexX'],nodeNext['indexY']]])
            if (numNode + self.numberBoxes<((self.numberBoxes**2)+1)):
                nodeDown = self.matchGraph.nodes[numNode + self.numberBoxes]
                if(actualNode['indexX']==nodeDown['indexX']):
                    self.matchGraph.add_edge(numNode, numNode + self.numberBoxes, nodes=[[actualNode['indexX'],actualNode['indexY']],[nodeDown['indexX'],nodeDown['indexY']]])
    
    def cleanVisited(self):
        for node,prop in self.matchGraph.nodes(data= True):
            self.matchGraph.nodes[node]['visited'] = []

    def insertedWall(self, objWall): #funcion que se llama cada vez que se inserta un muro
        node1 = objWall.nodesBlocked[0]
        node2 = objWall.nodesBlocked[1]
        n1,n2 = 0,0
        #n3 = [node for node, info in self.matchGraph.nodes(data = True) if (node1[0] == info['indexX'] and node1[1] == info['indexY'])]
        #n4 = [node for node, info in self.matchGraph.nodes(data = True) if (node2[0] == info['indexX'] and node2[1] == info['indexY'])]
        for node,info in self.matchGraph.nodes(data = True):
            if(info['indexX'] == node1[0] and info['indexY'] == node1[1]):
                n1 = node
            if(info['indexX'] == node2[0] and info['indexY'] == node2[1]):
                n2 = node
        self.matchGraph.remove_edge(n1,n2)

class Table():
    def __init__(self, numberBoxes, lenghtTable, matrix, colors, numberWalls):
        self.lenghtTable = lenghtTable
        self.numberBoxes = numberBoxes
        self.lenghtBox = (5 * self.lenghtTable) / ((6 * self.numberBoxes) + 1)
        self.lenghtSpace = self.lenghtBox / 5
        self.matrix = matrix
        self.colors = colors
        self.numberWalls = numberWalls
        self.tableGraph = TableGraph(self.numberBoxes)
        self.numberTurn = 1
    def generateWindow(self, players): #general la ventana de pygame
        pg.init()
        window = pg.display.set_mode((self.lenghtTable, self.lenghtTable))
        pg.display.set_caption("Tablero de Quoridor v3")
        run = True
        wall1 = Wall(5,5,5,6)
        wall2 = Wall(3,3,4,3)
        walls=[wall1,wall2]
        for wall in walls:
            self.tableGraph.insertedWall(wall)
        while run:
            window.fill(colors[6])
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False 
            self.generateTable(window)
            for p in players:
                p.drawPlayer(window)
            for wall in walls:
               wall.drawWall(window, self.colors[7], self.lenghtBox)

            pressed = pg.key.get_pressed()
            won = [False,0]
            if pressed[pg.K_w]:
                pg.display.set_caption("Tablero de Quoridor v3 || Turno de Jugador: " + str(self.numberTurn))
                if self.numberTurn == 1:
                    won = self.turn(players[0])
                    self.numberTurn += 1
                elif self.numberTurn == 2:
                    won = self.turn(players[1])
                    self.numberTurn += 1
                elif self.numberTurn == 3:
                    won = self.turn(players[2])
                    self.numberTurn += 1
                elif self.numberTurn == 4:
                    won = self.turn(players[3])
                    self.numberTurn = 1
                self.tableGraph.cleanVisited()
            pg.time.delay(100)
            pg.display.update()
            if won[0] == True:
                for p in players:
                    p.drawPlayer(window)
                Tk().wm_withdraw()
                messagebox.showinfo('Ganó el jugador ' + str(won[1]),'Salir')
                run = False
                pg.display.quit()
                pg.quit()
    def generateTable(self, window): #generar la tabla y dibujar
        coordX, coordY = self.lenghtSpace, self.lenghtSpace
        indexX, indexY = 1, 1
        for row in self.matrix:
            indexX = 1
            for col in row:
                box = Box(coordX, coordY, indexX, indexY)
                box.drawBox(window, self.colors[0], self.lenghtBox)
                coordX += self.lenghtBox + self.lenghtSpace
                indexX += 1
            coordX = self.lenghtSpace
            coordY += self.lenghtBox + self.lenghtSpace
            indexY += 1
    def generatePlayer(self, idx, idy, numberPlayer, numBoxes):
       p = Player(idx,idy,self.lenghtBox, numberPlayer,self.colors[numberPlayer], numBoxes)
       return p
    #defgenerateWall(self):
        #rIndexX, rIndexY = rd.randint(1,9), rd.randint(1,9)
        #rNode = [n for n,v in self.tableGraph.matchGraph.nodes(data=True) if(rIndexX == v['indexX'] and rIndexY==v['indexY'])]
    def pickUp(self,player):
        startnode = player.stablishNode(self.tableGraph.matchGraph)
        caux = []
        allNodes = []
        pts = player.victory
        allNodes = [node for node,val in self.tableGraph.matchGraph.nodes(data = True) if ((pts[0] == 0 and val['indexX'] == pts[1]) or (pts[0] == 1 and val['indexY'] == pts[1]))]
        for node in allNodes:
            way = findShortPathBFS(self.tableGraph.matchGraph, startnode, node, self.numberBoxes**2,player.name)
            caux.append([way, len(way)])
            self.tableGraph.cleanVisited()
            #programacion dinamica
        shortestWay = min(caux, key=lambda x:x[1])
        return shortestWay[0]

    def turn(self, player):
        #winPath = findShortPathBFS(self.tableGraph.matchGraph, startnode, player.victory, self.numberBoxes**2, 1)
        winPath = self.pickUp(player)
        node = [v for x,v in self.tableGraph.matchGraph.nodes(data=True) if (self.tableGraph.matchGraph.nodes[x]['id'] == winPath[-1])]
        player.movePlayer(node[0]['indexX'],node[0]['indexY'])
        if(len(winPath)==1):
            return [True,player.name]
        else:
            return [False,player.name]

##################### ALGORITHMS TIME #####################

####### DFS #######
####### BFS ####### Modified
def BFSBase(graph, source, destiny, numberVertex, parents, distances, Nplayer):
    queue = deque()
    for i in range(numberVertex+1):
        distances.append(numberVertex*2)
        parents.append(-1)
    #s = [node for node,info in graph.nodes(data = True) if(source[0] == info['indexX'] and source[1] == info['indexY'])]
    #d = [node for node,info in graph.nodes(data = True) if(destiny[0] == info['indexX'] and destiny[1] == info['indexY'])]
    s = source
    d = destiny
    graph.nodes[s]['visited'].append(Nplayer)
    distances[s] = 0
    queue.append(s)
    while len(queue) != 0:
        current = queue[0]
        queue.popleft()

        for ngh in graph.neighbors(current):
            if(Nplayer not in graph.nodes[ngh]['visited']):
                graph.nodes[ngh]['visited'].append(Nplayer)
            #if ngh != parents[current]:
                distances[ngh] = distances[current] + 1
                parents[ngh] = current
                queue.append(ngh)
                
                if(ngh == d):
                    return True
    return False

def findShortPathBFS(graph, source, destiny, numberVertex, NPlayer):
    parents = []
    distances = []

    if (BFSBase(graph, source, destiny, numberVertex, parents, distances, NPlayer) == False):
        return
    shortPath = []
    auxDest = destiny
    shortPath.append(auxDest)

    while parents[auxDest] != -1:
        shortPath.append(parents[auxDest])
        auxDest = parents[auxDest]
    shortPath.pop(len(shortPath)-1)
    return list(shortPath)

##### Dijkstra ####
#defDijkstraAlgo(graph, source):
#    for node,prop in graph.nodes(data = True):


##################### INPUT TIME ##########################
colors = [(255,255,255),(0,0,0),(237,106,90),(53,53,53),(244,241,187),(93,87,107),(28,110,140),(208,204,208),(39,65,86)]#bnr
numberBoxes = int(input('Ingrese el número de casillas de Quoridor: '))
numberWalls = int(input('Ingrese el número de muros (máximo 4): '))
mtx = [[1] * numberBoxes for i in range(numberBoxes)]
table = Table(numberBoxes, 625, mtx, colors, 0)
p1 = table.generatePlayer(numberBoxes//2+1,1,1,numberBoxes)
p2 = table.generatePlayer(1,numberBoxes//2+1,2,numberBoxes)
p3 = table.generatePlayer(numberBoxes,numberBoxes//2+1,3,numberBoxes)
p4 = table.generatePlayer(numberBoxes//2+1,numberBoxes,4,numberBoxes)
table.generateWindow([p1,p2,p3,p4])