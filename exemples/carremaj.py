#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.

from gurobipy import *

taille=4

v=    [[1, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]]

 # Range of plants and warehouses
indices = range(taille)
indicesk = range(16)

m = Model("carremaj")     
        
# declaration variables de decision
x = []
for i in indices:
    x.append([])
    for j in indices:
        x[i].append([])
        for k in indicesk:
            x[i][j].append(m.addVar(vtype=GRB.BINARY))

y = []
for i in range(4):
    y.append([])
    for j in range(4):
        y[i].append(m.addVar(vtype=GRB.INTEGER,lb=0,ub=8))

# boolean for parity
b=m.addVar(vtype=GRB.BINARY)

# Update model to integrate new variables
m.update()

obj = LinExpr();
obj =0
for k in indicesk:
    obj += (k+1) * (x[1][1][k] + x[1][2][k] + x[3][1][k] + x[3][2][k] + x[3][3][k])
        
# Set optimization objective - maximize sum of fixed costs
m.setObjective(obj,GRB.MINIMIZE)


# contrainte de 1 par case
for i in indices:
    for j in indices:
        m.addConstr(quicksum(x[i][j][k] for k in indicesk) == 1)

## contrainte une occurence de k dans le tableau
for k in indicesk:
    m.addConstr(quicksum(x[i][j][k] for i in indices for j in indices) == 1)
        
    
# contrainte de somme a 34 en ligne
for i in indices:
    m.addConstr(quicksum((k+1)*x[i][j][k] for k in indicesk for j in indices) == 34)
    
# contrainte de somme a 34 en colonne
for j in indices:
    m.addConstr(quicksum((k+1)*x[i][j][k] for k in indicesk for i in indices) == 34)
    
# contrainte de somme a 34 en diagonale
m.addConstr(quicksum((k+1)*x[i][i][k] for k in indicesk for i in indices) == 34)
m.addConstr(quicksum((k+1)*x[3-i][i][k] for k in indicesk for i in indices) == 34)
  

# contrainte des 4 coins qui ont la meme parite
m.addConstr(quicksum((k+1)*x[0][0][k] for k in indicesk) - 2*y[0][0]-b  == 0)
m.addConstr(quicksum((k+1)*x[0][1][k] for k in indicesk) - 2*y[0][1]-(1-b)  == 0)
m.addConstr(quicksum((k+1)*x[1][0][k] for k in indicesk) - 2*y[1][0]-(1-b)  == 0)
m.addConstr(quicksum((k+1)*x[1][1][k] for k in indicesk) - 2*y[1][1]-b  == 0)
m.addConstr(quicksum((k+1)*x[2][0][k] for k in indicesk) - 2*y[2][0]-b  == 0)
m.addConstr(quicksum((k+1)*x[2][1][k] for k in indicesk) - 2*y[2][1]-(1-b)  == 0)
m.addConstr(quicksum((k+1)*x[3][0][k] for k in indicesk) - 2*y[3][0]-(1-b)  == 0)
m.addConstr(quicksum((k+1)*x[3][1][k] for k in indicesk) - 2*y[3][1]-b  == 0)

# Resolution
m.optimize() 

print()
print('-------------------')
print('Solution')
print()

for i in indices:
    for j in indices:
        for k in indicesk:
            if x[i][j][k].x==1:
                v[i][j]=k+1
                
for i in indices:
        print(v[i])                


print()
print('Valeur de la fonction objectif :', 4*34-m.objVal)

    