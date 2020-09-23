import networkx as nx
import queue
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
      if(Matrix[i][j] != 0 and (i,j) != jugc.Pos()):
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

def CreateDownSideGraph(Matrix):
  g = nx.DiGraph()
  N = len(Matrix)
  
  for i in reversed(range(N * N)):
    g.add_node(i+1)
    g.nodes[i+1]['id']=str(i+1)
  ActualNode = 9
  
  for i in reversed(range(N)):
   for j in reversed(range(N)):
      if(Matrix[i][j] != 0):
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


def DFS_Visit(G, u):
  global tiempo
  tiempo = tiempo + 1
  u['inicio'] = tiempo
  u['color'] = 'Gris'
  for v_id in G.neighbors(int(u['id'])):
    v = G.nodes[v_id]
    if v['color'] == 'Blanco':
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
	  
def hallar_camino(G, s, v, camino):
  if (v['id'] == s['id']):
    camino.append(s['id'])
  elif v['padre'] == None:
    print('No exste camino de {} a {}'.format(s['id'],v['id']))
  else:
    hallar_camino(G,s,v['padre'],camino)
    camino.append(v['id'])
########################################

#BFS PATHFINDING
def BFS(G,s):
  for _,u in G.nodes(data = True):
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
      if v['color'] == 'Blanco':
        v['color'] = 'Gris'
        v['padre'] = u
        v['distance'] = u['distance'] + 1
        q.put(v)
      u['color'] = 'Negro'

tiempo = 0



