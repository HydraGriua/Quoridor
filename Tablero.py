import pygame as pg
import sys

#Configs iniciales
colors = [(255,255,255),(0,0,0),(255,0,0)]#bnr
WH = 900

#Medidas para graficar
n = int(input(" ingrese x (tablero sera de x * x):"))
grid = [[1]*n for x in range(n)]
esp=(WH/n)
sep = esp/(n-1)
anchCuad=esp-sep

 #Graficar el tablero con las medidas
def draw(win):
    x,y=sep,sep
    for row in grid:
        for col in row:
            pg.draw.rect(win,colors[2],[x,y,anchCuad,anchCuad])
            x+=anchCuad+sep
        y+=anchCuad+sep
        x=sep

#pos inicial jugadores 
pos1 = [8*int(sep+(anchCuad/2)),int(sep+(anchCuad/2))]
pos2 = [8*int((sep+(anchCuad/2))),15*int((sep+(anchCuad/2)))]

#window
pg.init()
win = pg.display.set_mode((WH,WH))
pg.display.set_caption("Tablero version 1")
run = True

base_font= pg.font.Font(None,60)
MenuLabel = "Jugar Corridor de " + str(n) +"X"+ str(n) 
Label = base_font.render(MenuLabel,True,(255,255,255))
menu = True
botonMenu = pg.Rect(300,400,500,60)
while menu:
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if botonMenu.collidepoint(event.pos):
                menu = False
    
    pg.draw.rect(win,colors[1],botonMenu)
    win.blit(Label,(botonMenu.x+5,botonMenu.y+5))
    pg.display.update()

while run:
    win.fill(colors[0])

    #pg.time.delay(80)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    #Calls
    draw(win)
    pg.draw.circle(win,colors[0],pos1,12)
    pg.draw.circle(win,colors[0],pos2,12)
    pg.display.update()