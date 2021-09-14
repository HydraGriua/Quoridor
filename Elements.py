import pygame as pg
import networkx as nx
#9import randon as rd
from collections import deque
import heapq as hp
from tkinter import *
from tkinter import messagebox
import time
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
        #Condiciones de victoria según las posiciones iniciales de los jugadores
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
        self.victory = cvic #Una lista cuyos elementos indican el eje e índice de las posiciones de victoria
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
        #Con las operaciones a continuación definimos si un muro es horizontal o vertical
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
    def generateGraph(self):
        for i in range(self.numberBoxes**2):
            numberNode = i + 1
            idx, idy = 0,0
            if(numberNode % self.numberBoxes == 0):
                idx = self.numberBoxes
                idy = int(numberNode//self.numberBoxes)
            else:
                idx = int(numberNode - ((numberNode//self.numberBoxes)*self.numberBoxes))
                idy = int((numberNode//self.numberBoxes)+1)
            self.matchGraph.add_node(numberNode, indexX = idx, indexY = idy, visited=[], id= numberNode, occupied = False)        
        for numNode in range(1,(self.numberBoxes**2)+1):
            actualNode = self.matchGraph.nodes[numNode]
            if (numNode+1<((self.numberBoxes**2)+1)):
                nodeNext = self.matchGraph.nodes[numNode+1]
                if(actualNode['indexY']==nodeNext['indexY']):
                    self.matchGraph.add_edge(numNode, numNode + 1)
            if (numNode + self.numberBoxes<((self.numberBoxes**2)+1)):
                nodeDown = self.matchGraph.nodes[numNode + self.numberBoxes]
                if(actualNode['indexX']==nodeDown['indexX']):
                    self.matchGraph.add_edge(numNode, numNode + self.numberBoxes)
    def cleanVisited(self): #Funcuón que limpia información del grafo después de cada turno
        for node,prop in self.matchGraph.nodes(data= True):
            self.matchGraph.nodes[node]['visited'] = []
            self.matchGraph.nodes[node]['occupied'] = False
    def insertedWall(self, objWall): #Funcion que se llama cada vez que se inserta un muro, para hacer remove_edge
        node1 = objWall.nodesBlocked[0]
        node2 = objWall.nodesBlocked[1]
        n1,n2 = 0,0
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
    def generateWindow(self, players): #Genera y controla el juego
        pg.init()
        window = pg.display.set_mode((self.lenghtTable, self.lenghtTable))
        pg.display.set_caption("Tablero de Quoridor v3")
        run = True
        walls=[]
        while run:
            window.fill(colors[6])
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False 
            self.generateTable(window)
            for p in players:
                p.drawPlayer(window)
            for wall in walls:
               wall.drawWall(window, self.colors[8], self.lenghtBox)
            pressed = pg.key.get_pressed()
            won = [False,0]
            pg.display.set_caption("Tablero de Quoridor v3 || Turno de Jugador: " + str(self.numberTurn))
            if pressed[pg.K_w]: #Presionar 'w' para hacer un movimiento y gastar tu turno
                if self.numberTurn == 1:
                    won = self.turn(players[0],[players[1],players[2],players[3]])
                    self.numberTurn += 1
                elif self.numberTurn == 2:
                    won = self.turn(players[1],[players[0],players[2],players[3]])
                    self.numberTurn += 1
                elif self.numberTurn == 3:
                    won = self.turn(players[2],[players[1],players[0],players[3]])
                    self.numberTurn += 1
                elif self.numberTurn == 4:
                    won = self.turn(players[3],[players[0],players[1],players[2]])
                    self.numberTurn = 1
                self.tableGraph.cleanVisited()
            if pressed[pg.K_s]: #Presionar 's' para hacer un input con el fin de colocar un muro y usar el turno
                ax, ay, dx, dy, direc = map(int, input().split())
                bx,by,cx,cy = dx,ay,ax,dy
                walla = 0
                wallb = 0
                if direc == 1:
                    walla = Wall(ax,ay,cx,cy)
                    wallb = Wall(bx,by,dx,dy)
                else:
                    walla = Wall(ax,ay,bx,by)
                    wallb = Wall(cx,cy,dx,dy)
                self.tableGraph.insertedWall(walla)
                self.tableGraph.insertedWall(wallb)
                walls.append(walla)
                walls.append(wallb)
                if self.numberTurn <4:
                    self.numberTurn += 1
                else:
                    self.numberTurn =1 
            pg.time.delay(100)
            pg.display.update()
            if won[0] == True: #Sucede cuando gana un jugador
                window.fill(colors[6])
                self.generateTable(window)
                for p in players:
                    p.drawPlayer(window)
                for wall in walls:
                    wall.drawWall(window, self.colors[8], self.lenghtBox)
                pg.display.update()
                pg.time.delay(500)
                Tk().wm_withdraw()
                messagebox.showinfo('Ganó el jugador ' + str(won[1]),'Salir')
                run = False
                pg.display.quit()
                pg.quit()
    def generateTable(self, window): #Generar la tabla y dibujar
        coordX, coordY = self.lenghtSpace, self.lenghtSpace
        indexX, indexY = 1, 1
        for row in self.matrix:
            indexX = 1
            for col in row:
                box = Box(coordX, coordY, indexX, indexY)
                box.drawBox(window, self.colors[7], self.lenghtBox)
                coordX += self.lenghtBox + self.lenghtSpace
                indexX += 1
            coordX = self.lenghtSpace
            coordY += self.lenghtBox + self.lenghtSpace
            indexY += 1
    def generatePlayer(self, idx, idy, numberPlayer, numBoxes):
       p = Player(idx,idy,self.lenghtBox, numberPlayer,self.colors[numberPlayer], numBoxes)
       return p
    def pickUp(self,player,players): #Funcion llamada por 'turn' para obtener el menor de los caminos 
        gx = self.tableGraph.matchGraph
        startnode = player.stablishNode(gx)
        caux = []
        allNodes = []
        pts = player.victory
        #La siguiente línea es la que obtiene las posiciones de victoria
        allNodes = [node for node,val in gx.nodes(data = True) if ((pts[0] == 0 and val['indexX'] == pts[1]) or (pts[0] == 1 and val['indexY'] == pts[1]))]
        for node in allNodes:
            way = findShortPath(gx, startnode, node, self.numberBoxes**2,player.name)
            #Se evalua si en el camino hay jugadores
            self.tableGraph.cleanVisited()
            nodx = 0
            if len(way) > 1:
                for p in players:
                    nodeg = p.stablishNode(gx)
                    gx.nodes[nodeg]['occupied'] = True
                    if nodeg == way[-1]:
                        nodx = nodeg    
                scnd = False
                if nodx == way[-1]:
                    for p in players:
                        gg = p.stablishNode(gx)
                        if way[-2] == gg:
                            scnd = True
                            break
                    #Si por alguna razón no podemos saltar o ir en diagonal  
                    if scnd:
                        ln = []
                        for i in gx.neighbors(way[-1]):
                            if (gx.nodes[i]['occupied'] == False) and (i != player.stablishNode(gx)):
                                ln.append(i)
                        way[-1] = ln[0]
                    else:
                        way[-1] = way[-2]
            caux.append([way, len(way)])
        #Vemos cual de los caminos hacia los nodos de victoria es el mas corto
        shortestWay = min(caux, key=lambda x:x[1])
        return shortestWay[0]
    def turn(self, player,players): #Funcion que se ejecuta cada turno
        winPath = self.pickUp(player,players)
        print('move')
        if(len(winPath)>1):
            #if self.tableGraph.matchGraph.nodes[winPath[-1]]['occupied']:
            #    node = self.tableGraph.matchGraph.nodes[winPath[-2]]
            #else:
            node = self.tableGraph.matchGraph.nodes[winPath[-1]]
            player.movePlayer(node['indexX'],node['indexY'])
            return [False,player.name]
        else:
            node = self.tableGraph.matchGraph.nodes[winPath[-1]]
            player.movePlayer(node['indexX'],node['indexY'])
            return [True,player.name]

##################### ALGORITHM TIME #####################

def AStar(graph, source, destiny, numberVertex, parents, distances, Nplayer):
    s = source
    d = destiny
    def h(n):
        c1 = abs(graph.nodes[n]['indexX'] - graph.nodes[d]['indexX'])
        c2 = abs(graph.nodes[n]['indexY'] - graph.nodes[d]['indexY'])
        return c1+c2
    gScore = []
    fScore = []
    for i in range(numberVertex+1):
        fScore.append([999,i]) 
        gScore.append(999)
    gScore[s] = 0
    fScore[s][0] = h(s)
    q = [fScore[s]]
    while len(q) != 0:
        _,current = hp.heappop(q)
        if current == d:
            return True
        for ngh in graph.neighbors(current):
            tentative = gScore[current] + 1
            if tentative < gScore[ngh]:
                parents[ngh] = current
                gScore[ngh] = tentative
                fScore[ngh][0] = gScore[ngh] + h(ngh)
                if ngh not in q:
                    hp.heappush(q, [fScore[ngh][0], ngh])
    return False

def findShortPath(graph, source, destiny, numberVertex, NPlayer): #Funcion llamada para evaluar el grafo y buscar caminos
    parents = []
    distances = []
    for i in range(numberVertex+1):
        distances.append(numberVertex*2)
        parents.append(-1) 

    start = time.time()
    exist = AStar(graph, source, destiny, numberVertex, parents, distances, NPlayer) 
    end = time.time()
    if (exist == False):
        return
    shortPath = []
    auxDest = destiny
    shortPath.append(auxDest)
    while parents[auxDest] != -1:
        shortPath.append(parents[auxDest])
        auxDest = parents[auxDest]
    shortPath.pop(len(shortPath)-1)
    return list(shortPath)

##################### INPUT TIME ##########################
colors = [(255,255,255),(237,106,90),(244,241,187),(171,135,255),(43,43,43),(93,87,107),(28,110,140),(208,204,208),(195,235,120)]#bnr
numberBoxes = int(input('Ingrese el número de casillas de Quoridor: '))
mtx = [[1] * numberBoxes for i in range(numberBoxes)]
table = Table(numberBoxes, 625, mtx, colors, 0)
#Por defecto, las posiciones de los jugadores estarán a un extremo y al medio
p1 = table.generatePlayer(numberBoxes//2+1,1,1,numberBoxes)
p2 = table.generatePlayer(1,numberBoxes//2+1,2,numberBoxes)
p3 = table.generatePlayer(numberBoxes,numberBoxes//2+1,3,numberBoxes)
p4 = table.generatePlayer(numberBoxes//2+1,numberBoxes,4,numberBoxes)
table.generateWindow([p1,p2,p3,p4])