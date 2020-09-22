import pygame as pg
import sys
from TestGraph import *

#Configs iniciales
colors = [(255,255,255),(0,0,0),(255,0,0),(28,110,140),(208,204,208),(53,53,53),(39,65,86)]#bnr
WH = 900
camino = []
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
        

#pos inicial jugadores 
class Jugador():
    def __init__(self,x,y):
        self.x = (x//(size+space))
        self.y = (y//(size+space))
    def Dibujar(self,win,color,r,n):
        xDibujo = int((self.x)*(size+space)+(size/2 + space))
        yDibujo = int((self.y)*(size+space)+(size/2 + space))
        pg.draw.circle(win,color,(xDibujo,yDibujo),r)
    def Mover(self,x,y):
        self.x = x
        self.y = y

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

while run:
    win.fill(colors[3])
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            #aki

    #Calls
    draw(win)
    graph = CreateGraph(grid)
    startnode1 = [x for x,y in graph.nodes(data=True) if y['position']==(int(jug1.x),int(jug1.y))]
    BFS(graph,graph.nodes[startnode1[0]])
    hallar_camino(graph,graph.nodes[startnode1[0]],graph.nodes[91],camino)
    jug1.Dibujar(win,colors[2],12,n)
    pressed = pg.key.get_pressed()
    if pressed[pg.K_w]:
        i+=1
        x = graph.nodes[int(camino[i])]['position'][0]
        y = graph.nodes[int(camino[i])]['position'][1]
        jug1.Mover(x,y)
    #jug2.Dibujar(win,colors[2],12,n)

    pg.display.update()






















