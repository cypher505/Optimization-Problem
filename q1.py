import gurobipy as g
from gurobipy import *


def q1(M):
    m=g.Model("question 1")
    taille=len(M)
    X=[]
    for i in range(taille):
        X.append([])
        for j in range(taille):
            X[i].append(m.addVar(vtype=GRB.BINARY, name="x_{}_{}".format(i,j)))

    obj=g.LinExpr()
    obj=0
    for i in range(taille):
        for j in range(taille):
            obj+=M[i][j]*X[i][j]

    m.update()

    m.setObjective(obj, GRB.MAXIMIZE)

    for i in range(taille):
        m.addConstr(g.quicksum(X[i][j] for j in range(taille))==1)
    for j in range(taille):
        m.addConstr(g.quicksum(X[i][j] for i in range(taille))==1)

    m.optimize()

    return m, X

U=[[12,20,6,5,8],
    [5,12,6,8,5],
    [8,5,11,5,6],
    [6,8,6,11,5],
    [5,6,8,7,7]]

q1(U)

def q4(M, eps):
    m=g.Model("q4")
    taille=len(M)
    X=[]
    for i in range (taille):
        X.append([])
        for j in range (taille):
            X[i].append(m.addVar(vtype=GRB.BINARY, name="x_{}_{}".format(i,j)))

    min=m.addVar(vtype=GRB.CONTINUOUS, name="min")
    m.update()
    obj=g.LinExpr()
    obj=0
    obj+=min
    L=[]
    for i in range(taille):
        for j in range(taille):
            u=X[i][j]*M[i][j]
            if X[i][j]==1:
                L.append(u)
            obj+=u*eps

    m.setObjective(obj, GRB.MAXIMIZE)

    for i in range(taille):
        m.addConstr(g.quicksum(X[i][j] for j in range(taille))==1)
    for j in range(taille):
        m.addConstr(g.quicksum(X[i][j] for i in range(taille))==1)
    m.addConstr(min==g.min_(u for u in L))

    m.optimize()

    return m.objVal,X    

q4(U, 0.01)




