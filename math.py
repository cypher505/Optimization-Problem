import gurobipy as gb
from gurobipy import *

def q1(U):
    m=gb.Model("question 1")
    taille=len(U)
    X=[]
    for i in range(taille):
        X.append([])
        for j in range(taille):
            X[i].append(m.addVar(vtype=GRB.BINARY, name="x_{}_{}".format(i,j)))

    obj=gb.LinExpr()
    obj=0
    for i in range(taille):
        for j in range(taille):
            obj+=U[i][j]*X[i][j]

    m.update()

    m.setObjective(obj, GRB.MAXIMIZE)

    for i in range(taille):
        m.addConstr(gb.quicksum(X[i][j] for j in range(taille))==1)
    for j in range(taille):
        m.addConstr(gb.quicksum(X[i][j] for i in range(taille))==1)

    m.optimize()

    return m, X

def q4(eps: float, U):
    n=len(U)
    m = gb.Model("question4")
    z = m.addVar(vtype=gb.GRB.CONTINUOUS, name="Z")
    m.addConstr(z >= 0)
    x = []
    for i in range(n):
        xi = []
        for j in range(n):
            name = f"x{i}_{j}"
            xi.append(m.addVar(vtype=gb.GRB.BINARY, name=name))

        x.append(xi)

    m.setObjective(z, gb.GRB.MAXIMIZE)

    for i in range(n):
        minimality = sum([x[i][j] * U[i][j] for j in range(n)]) + sum(
            [sum([(eps * U[j][k]) * x[j][k] for k in range(n)]) for j in range(n)])

        determinism = sum([x[i][j] for j in range(n)])
        injectivity = sum([x[j][i] for j in range(n)])

        m.addConstr(z <= minimality)
        m.addConstr(determinism == 1)
        m.addConstr(injectivity <= 1)

    m.optimize()

    if True:
        #for v in m.getVars():
            #print('%s %g' % (v.VarName, v.X))

        print('Obj: %g' % m.ObjVal)

    return m




U=[[12,20,6,5,8],
    [5,12,6,8,5],
    [8,5,11,5,6],
    [6,8,6,11,5],
    [5,6,8,7,7]]

#q1(U)
q4(0.000001,U)