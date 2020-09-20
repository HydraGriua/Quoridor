import pygame as pg

#Configs and values and functions
colors = [(255,255,255),(0,0,0),(255,0,0)]#bnr
WH = 900
p = int(input(" ingrese x (tablero sera de x * x):"))
grid = [[1]*p for x in range(p)]
G=(WH/p)
p = G/(p-1)
gw=G-p
def draw(win):
    x,y=p,p
    for row in grid:
        for col in row:
            pg.draw.rect(win,colors[2],[x,y,gw,gw])
            x+=gw+p
        y+=gw+p
        x=p



#window
pg.init()
win = pg.display.set_mode((WH,WH))
pg.display.set_caption("Tablero version 1")
run = True
while run:
    win.fill(colors[0])
    #pg.time.delay(80)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    #Calls
    draw(win)





    #pg.draw.rect(win,colors[1],rect=[x,y,10,20])

    pg.display.update()