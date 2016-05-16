from networkx import * 
from numpy.linalg import eig
from numpy import *

G=Graph()
fn=raw_input("Enter the File name:")
G=read_edgelist(fn)
bt=betweenness_centrality(G, normalized=True, weighted_edges=False)
deg = G.degree(with_labels=True)
fn1=raw_input("Enter the Output file name:")
f=open(fn1, 'w')
k = bt.keys()
k.sort()
k.sort(lambda a,b: cmp(int(a), int(b)))
for key in k:
    f.write(key)
    f.write("\t")
    s=str(bt[key])
    f.write(s)
    f.write("\n")
k = deg.keys()
k.sort()
k.sort(lambda a,b: cmp(int(a), int(b)))
for key in k:
    f.write(key)
    f.write("\t")
    s=str(deg[key])
    f.write(s)
    f.write("\n")
f.close()

