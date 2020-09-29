import networkx as nx
import queue
import math
import matplotlib.pyplot as plt
global tiempo


##CREAR GRAFO
def CreateGraph(Matrix,jugc):
  g = nx.DiGraph()
  N = len(Matrix)
  
  for i in range(N * N):
    g.add_node(i+1)
    g.nodes[i+1]['id']=str(i+1)
  ActualNode = 1
  
  for i in range(N):
   for j in range(N):
      if(Matrix[j][i] != 0):
        if((j,i) == jugc.Pos()):
          g.nodes[ActualNode]['position']= None #La coordenada
          g.nodes[ActualNode]['HasPosition'] = False #
        else:
          g.nodes[ActualNode]['HasPosition'] = True
          g.nodes[ActualNode]['position']=(j,i)
          if(NodeExist(i,j+1,Matrix)):
            g.add_edge(ActualNode,ActualNode+1)
          if(NodeExist(i,j-1,Matrix)):
            g.add_edge(ActualNode,ActualNode-1)
          if(NodeExist(i+1,j,Matrix)):
            g.add_edge(ActualNode,ActualNode + N)
          if(NodeExist(i-1,j,Matrix)):
            g.add_edge(ActualNode,ActualNode - N)
      ActualNode += 1
  return g

def CreateDownSideGraph(Matrix,jugc):
  g = nx.DiGraph()
  N = len(Matrix)
  
  for i in reversed(range(N * N)):
    g.add_node(i+1)
    g.nodes[i+1]['id']=str(i+1)
  ActualNode = N*N
  
  for i in reversed(range(N)):
   for j in reversed(range(N)):
      if(Matrix[j][i] != 0):
        if((j,i) == jugc.Pos()):
          g.nodes[ActualNode]['position']= None
          g.nodes[ActualNode]['HasPosition'] = False
        else:
          g.nodes[ActualNode]['HasPosition'] = True
          g.nodes[ActualNode]['position']=(j,i)
        if(NodeExist(i,j+1,Matrix)):
          g.add_edge(ActualNode,ActualNode+1)
        if(NodeExist(i,j-1,Matrix)):
          g.add_edge(ActualNode,ActualNode-1)
        if(NodeExist(i+1,j,Matrix)):
          g.add_edge(ActualNode,ActualNode + N)
        if(NodeExist(i-1,j,Matrix)):
          g.add_edge(ActualNode,ActualNode - N)
      ActualNode -= 1
  return g 
#######################################

##DFS PATHFINDING
def DFS(G):
  global tiempo
  for _, u in G.nodes(data=True):
    u['color'] = 'Blanco'
    u['padre'] = None
  tiempo = 0
  for _, u in G.nodes(data=True):
    if u['color'] == 'Blanco':
      DFS_Visit(G,u)

#El Salto falta validar
def DFS_Visit(G, u):
  global tiempo
  tiempo = tiempo + 1
  u['inicio'] = tiempo
  u['color'] = 'Gris'
  nodos = len(list(G.nodes))
  #if u['id'] == '1':
   # u['padre']  = G.nodes[int(u['id']) + int(math.sqrt(nodos))]
  # if u['id'] == str(nodos):
  #   u['padre']  = G.nodes[int(u['id']) - int(math.sqrt(nodos))]
  for v_id in G.neighbors(int(u['id'])):
    v = G.nodes[v_id]
    if v['color'] == 'Blanco' and v['HasPosition'] == True:
      v['padre'] = u
      DFS_Visit(G, v)
  u['color'] = 'Negro'
  tiempo = tiempo + 1
  u['fin'] = tiempo


def NodeExist(i,j,Matrix):
  if (i >= 0 and i < len(Matrix) and j >= 0 and j < len(Matrix[0])):
    if(Matrix[i][j] == 0):
      return False 
    return True 
  return False
	  
def hallar_caminoD(G, s, v, camino):
  if (v['id'] == s['id']):
    camino.append(s['id'])
  elif s['padre']['id'] == v['id']:
    camino.append(v['id'])
    return
  elif v['padre'] == None:
    camino.append(v['id'])
    return
  else:
    hallar_caminoD(G,s,v['padre'],camino)
    camino.append(v['id'])
########################################

def hallar_caminoB(G, s, v, camino):
  if (v['id'] == s['id']):
    camino.append(s['id'])
  elif v['padre'] == None:
    v = G.nodes[int(v['id'])-1]
    hallar_caminoB(G,s,v,camino)
    return
  else:
    hallar_caminoB(G,s,v['padre'],camino)
    camino.append(v['id'])



#BFS PATHFINDING
def BFS(G,s):
  for _,u in G.nodes(data = True):
    # _ es el prmer valor
    #u es el 2do valor
    #Todos los nodos tiene color blanco,padre ninguno y distancia ninguna
    u['color'] = 'Blanco'
    u['padre'] = None
    u['distance'] = None

  s['color'] = 'Gris'
  s['distance'] = 0
  s['padre'] = None
  q = queue.Queue()
  q.put(s)
  while not q.empty():
    u = q.get()
    for v_id in G.neighbors(int(u['id'])):
      v = G.nodes[v_id]
      if v['color'] == 'Blanco' and v['HasPosition'] == True:
        v['color'] = 'Gris'
        v['padre'] = u
        v['distance'] = u['distance'] + 1
        q.put(v)
      u['color'] = 'Negro'

tiempo = 0



