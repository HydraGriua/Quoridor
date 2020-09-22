import pygame as pg
import sys
from TestGraph import *

#Configs iniciales
colors = [(255,255,255),(0,0,0),(255,0,0),(28,110,140),(208,204,208),(53,53,53),(39,65,86)]#bnr
WH = 900

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
        xDibujo = int((self.x)*(size+space)*1.12)
        yDibujo = int((self.y)*(size+space)+(size/2 + space))
        pg.draw.circle(win,color,(xDibujo,yDibujo),r)

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
    jug1.Dibujar(win,colors[2],12,n)
    jug2.Dibujar(win,colors[2],12,n)
    pg.display.update()

graph = CreateGraph(grid)
print(jug1.x,jug1.y)
startnode1 = [x for x,y in graph.nodes(data=True) if y['position']==(jug1.x,jug1.y)]
#9BFS(graph,startnode1)
print(startnode1)
#camino = []
#hallar_camino(graph,startnode1,graph.nodes[45],camino)
#print(camino)












