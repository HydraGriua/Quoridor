import pygame as pg
import sys
from TestGraph import *
from tkinter import *
from tkinter import messagebox
import time
sys.setrecursionlimit(10**7)

#Configs iniciales
colors = [(255,255,255),(0,0,0),(237,106,90),(53,53,53),(244,241,187),(93,87,107),(28,110,140),(208,204,208),(39,65,86)]#bnr
WH = 900
i = 0
#Medidas para graficar
n = int(input(" ingrese x (tablero sera de x * x):"))
grid = [[1]*n for x in range(n)]
size = WH / (n*1.15)
space = WH / (n*8.15)

#radio jugador
r = int((size-space)/3.14159)

 #Graficar el tablero con las medidas
def draw(win):
    x,y=space,space
    for row in grid:
        for col in row:
            pg.draw.rect(win,colors[7],[x,y,size,size])
            x+=size + space
        x = space
        y+=size + space

def Eleccion(t,g,st,p,c,jugs):
    n = int(math.sqrt(g.number_of_nodes()))
    shortwin = n*n
    caux = []
    if t == 0:
        for i in range(n):
            node = [x for x,y in g.nodes(data=True) if (y['position'] == None)]
            if p-i not in node:
                hallar_caminoB(g,g.nodes[st[0]],g.nodes[p-i],caux)
                #hallar_caminoD(g,g.nodes[st[0]],g.nodes[p-i],caux)
                if len(caux) < shortwin:
                    j = p-i
                    shortwin = len(caux)
                caux = [] 
    elif t == 1:
        for i in range(n):            
            node = [x for x,y in g.nodes(data=True) if (y['position'] == None)]
            if p+i not in node:
                hallar_caminoB(g,g.nodes[st[0]],g.nodes[p+i],caux)
                #hallar_caminoD(g,g.nodes[st[0]],g.nodes[p+i],caux)
                if len(caux) < shortwin:
                    j = p+i
                    shortwin = len(caux)
                caux = []
    elif t == 2:
        for i in range(n):
            node = [x for x,y in g.nodes(data=True) if (y['position'] == None)]
            if p+(n*i) not in node:
                hallar_caminoB(g,g.nodes[st[0]],g.nodes[p+(n*i)],caux)
                #hallar_caminoD(g,g.nodes[st[0]],g.nodes[p+(n*i)],caux)
                if len(caux) < shortwin:
                    j = p+(n*i)
                    shortwin = len(caux)
                caux = []
    elif t == 3:
        for i in range(n):          
            node = [x for x,y in g.nodes(data=True) if (y['position'] == None)]
            if p-(n*i) not in node:
                hallar_caminoB(g,g.nodes[st[0]],g.nodes[p-(n*i)],caux)
                #hallar_caminoD(g,g.nodes[st[0]],g.nodes[p-(n*i)],caux)
                if len(caux) < shortwin:
                    j = p-(n*i)
                    shortwin = len(caux)
                caux = []
    hallar_caminoB(g,g.nodes[st[0]],g.nodes[j],c)

def Turnos(grid,jug,jugs,pos,turno):
    if Turno == 0 or Turno == 3:
        graph = CreateGraph(grid,jugs) 
    else:
        graph = CreateDownSideGraph(grid,jugs)
    camino = []
    startnode = [x for x,y in graph.nodes(data=True) if (y['position'] ==(int(jug.x),int(jug.y)) and y['HasPosition'] == True)]
    #BFS(graph,graph.nodes[startnode[0]])
    #DFS(graph)
    #start = time.time()
    Dijkstra(graph,graph.nodes[startnode[0]])
    #end = time.time()
    #print (end-start)
    
    Eleccion(Turno,graph,startnode,pos,camino,jugs)

    if len(camino) == 1:
        x = graph.nodes[int(camino[0])]['position'][0]
        y = graph.nodes[int(camino[0])]['position'][1]
        Tk().wm_withdraw()
        messagebox.showinfo('Ganó el jugador en la posicion ' + str(jug.Pos()),'Salir')
        run = False
        pg.display.quit()
        pg.quit()
    else:
        x = graph.nodes[int(camino[1])]['position'][0]
        y = graph.nodes[int(camino[1])]['position'][1]
    pg.time.delay(100)
    jug.Mover(x,y)


#pos inicial jugadores 
class Jugador():
    def __init__(self,x,y,c):
        self.x = (x//(size+space))
        self.y = (y//(size+space))
        self.color = colors[c]
    def Dibujar(self,win,r):
        xDibujo = int((self.x)*(size+space)+(size/2 + space))
        yDibujo = int((self.y)*(size+space)+(size/2 + space))
        pg.draw.circle(win,self.color,(xDibujo,yDibujo),r)
    def Mover(self,x,y):
        self.x = x
        self.y = y
    def Pos(self):
        return (int(self.x),int(self.y))

jug1= Jugador(WH/2,space+(size/2),2)
jug2= Jugador(WH/2,WH-(space+(size/2)),3)
jug3 = Jugador(WH-(space+(size/2)),WH/2,5)
jug4 = Jugador(space+(size/2),WH/2,4)

#window
pg.init()
win = pg.display.set_mode((WH,WH))
pg.display.set_caption("Quoridor V.1.5.0")
run = True
base_font= pg.font.Font(None,60)
MenuLabel = "Jugar Corridor de " + str(n) +"X"+ str(n) 
Label = base_font.render(MenuLabel,True,colors[3])
menu = True
botonMenu = pg.Rect(300,400,500,60)
while menu:
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if botonMenu.collidepoint(event.pos):
                menu = False   
    pg.draw.rect(win,colors[0],botonMenu)
    win.blit(Label,(botonMenu.x+5,botonMenu.y+5))
    pg.display.update()
Turno = 0
while run:
    win.fill(colors[6])
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False   
    #Calls
    draw(win)
    jug1.Dibujar(win,r)
    jug2.Dibujar(win,r)
    jug3.Dibujar(win,r)
    jug4.Dibujar(win,r)
    pressed = pg.key.get_pressed()
    if pressed[pg.K_w]:
        if Turno == 0:
            jugs = [jug2,jug3,jug4]
            Turnos(grid,jug1,jugs,n*n,Turno)
            Turno += 1
        elif Turno == 1:
            jugs = [jug1,jug3,jug4]
            Turnos(grid,jug2,jugs,1,Turno)
            Turno += 1
        elif Turno == 2:
            jugs = [jug2,jug1,jug4]
            Turnos(grid,jug3,jugs,1,Turno)
            Turno += 1
        elif Turno == 3:
            jugs = [jug2,jug3,jug1]
            Turnos(grid,jug4,jugs,n*n,Turno)
            Turno = 0
    try:
        pg.display.update()
    except:
        run = False
 


















