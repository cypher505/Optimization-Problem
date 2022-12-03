from gurobipy import *

m=Model("question 1")

taille=5
U=[[12,20,6,5,8],
    [5,12,6,8,5],
    [8,5,11,5,6],
    [6,8,6,11,5],
    [5,6,8,7,7]]


X=[]
for i in range(taille):
    X.append([])
    for j in range(taille):
        X[i].append(m.addVar(vtype=GRB.BINARY))

obj=LinExpr()
obj=0
for i in range(taille):
    for j in range(taille):
        obj+=U[i][j]*X[i][j]

m.update()

m.setObjective(obj, GRB.MAXIMIZE)

for i in range(taille):
    m.addConstr(quicksum(X[i][j] for j in range(taille))==1)
for j in range(taille):
    m.addConstr(quicksum(X[i][j] for i in range(taille))==1)

m.optimize()

m.printAttr('X')


