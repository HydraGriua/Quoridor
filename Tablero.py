import pygame as pg
import sys
from TestGraph import *

#Configs iniciales
colors = [(255,255,255),(0,0,0),(255,0,0),(28,110,140),(208,204,208),(53,53,53),(39,65,86)]#bnr
WH = 900
i = 0


#Medidas para graficar
n = int(input(" ingrese x (tablero sera de x * x):"))
grid = [[1]*n for x in range(n)]
size = WH / (n*1.15)
space = WH / (n*8.15)

 #Graficar el tablero con las medidas
def draw(win):
    x,y=space,space
    for row in grid:
        for col in row:
            pg.draw.rect(win,colors[4],[x,y,size,size])
            x+=size + space
        x = space
        y+=size + space

def Turnos(grid,jug,jugc,pos):
    graph = CreateGraph(grid,jugc) 
    camino = []
    i = 0
    startnode = [x for x,y in graph.nodes(data=True) if (y['position'] ==(int(jug.x),int(jug.y)) and y['HasPosition'] == True)]
    BFS(graph,graph.nodes[startnode[0]])
    hallar_camino(graph,graph.nodes[startnode[0]],graph.nodes[pos],camino)  
    i+=1
    if len(camino) == 1:
        x = graph.nodes[int(camino[0])]['position'][0]
        y = graph.nodes[int(camino[0])]['position'][1]
    else:
        x = graph.nodes[int(camino[i])]['position'][0]
        y = graph.nodes[int(camino[i])]['position'][1]
    pg.time.delay(200)
    jug.Mover(x,y)
    jug.Dibujar(win,colors[2],12)



#pos inicial jugadores 
class Jugador():
    def __init__(self,x,y):
        self.x = (x//(size+space))
        self.y = (y//(size+space))
    def Dibujar(self,win,color,r):
        xDibujo = int((self.x)*(size+space)+(size/2 + space))
        yDibujo = int((self.y)*(size+space)+(size/2 + space))
        pg.draw.circle(win,color,(xDibujo,yDibujo),r)
    def Mover(self,x,y):
        self.x = x
        self.y = y
    def Pos(self):
        return (int(self.x),int(self.y))

jug1= Jugador(WH/2,space+(size/2))
jug2= Jugador(WH/2,WH-(space+(size/2)))

#window
pg.init()
win = pg.display.set_mode((WH,WH))
pg.display.set_caption("Tablero version 1")
run = True
base_font= pg.font.Font(None,60)
MenuLabel = "Jugar Corridor de " + str(n) +"X"+ str(n) 
Label = base_font.render(MenuLabel,True,colors[5])
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
Turno = True
while run:
    win.fill(colors[3])
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            #aki
    
    jug1.Dibujar(win,colors[2],12)
    jug2.Dibujar(win,colors[5],12)

    #Calls
    draw(win)
    pressed = pg.key.get_pressed()
    if pressed[pg.K_w]:
        if Turno:
            Turnos(grid,jug1,jug2,81)
        else:
            Turnos(grid,jug2,jug1,81)
        Turno = not Turno
    
    pg.display.update()
    






















