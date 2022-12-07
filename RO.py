import gurobipy as g
from gurobipy import *
from time import *
from random import seed, randint
import matplotlib.pyplot as plt

U=[[12,20,6,5,8],
    [5,12,6,8,5],
    [8,5,11,5,6],
    [6,8,6,11,5],
    [5,6,8,7,7]]

def satisfaction(l, M): #calcule la satisfaction totale
    if len(l)==len(M):
        n=len(l)
        s=0
        for i in range(n):
            s+=M[i][l[i]-1]
    return s

def affichage(l, f, liste): #facilite l'affichage de π et u
    s="{} : [".format(f)
    for i in range(len(l)):
        if i!=len(l)-1:
            s+="{}, ".format(l[i])
        else:
            s+="{}] -> {}".format(l[i], liste)
    print(s)   

def create_matrix(n): #crée une matrice de taille n contenant des entiers aléatoires entre 0 et 20 inclus
    return [[randint(0,20) for i in range(n)] for j in range(n)]

def q1(M):
    print("Question 1\n")
    m=g.Model("question 1")
    m.Params.LogToConsole = 0
    taille=len(M)
    X=[]
    for i in range(taille):
        X.append([])
        for j in range(taille):
            X[i].append(m.addVar(vtype=g.GRB.BINARY, name="x_{}_{}".format(i+1,j+1)))

    obj=0
    for i in range(taille):
        for j in range(taille):
            obj+=M[i][j]*X[i][j]

    m.update()

    m.setObjective(obj, g.GRB.MAXIMIZE)

    for i in range(taille):
        m.addConstr(g.quicksum(X[i][j] for j in range(taille))==1)
    for j in range(taille):
        m.addConstr(g.quicksum(X[i][j] for i in range(taille))==1)

    m.optimize()
    m.printAttr('X')
    pi=[0 for i in range(taille)]
    upi=[0 for i in range(taille)]
    ListeN=[]
    for i in range(taille):
        ListeN.append(i+1)
        for j in range(taille):
            if X[i][j].x!=0:
                print("π(a_{}) = o_{}".format(i+1, j+1))
                pi[i]=j+1
                upi[i]=M[i][j]
    print("\n")
    affichage(ListeN, "π", pi)
    affichage(ListeN, "u", upi)
    print("\n")
    print("Valeur de la fonction objectif : {}".format(m.objVal))
    print("Satisfaction totale = {}".format(m.objVal))
    print("Satisfaction moyenne = {}".format(m.objVal/taille))
    return m.objVal, pi, upi

def courbe_Q1():
    Listn=[]
    cpu_q1=[]
    for i in range(5,100,5):
        Listn.append(i)
        start=time()
        for k in range(10):
            q1(create_matrix(i))
        end=time()
        cpu_q1.append((end-start)/10)
    plt.plot(Listn,cpu_q1)
    plt.title("Temps CPU de l'optimisation au sens de q1")
    plt.xlabel("Taille de l'instance (n)")
    plt.ylabel("Temps CPU (s)")
    
    plt.show()
# courbe_Q1()  

q1(U)

def q4(M, eps):
    print("---------------------------------------------------------------------------")
    print("Question 4\n")
    m=g.Model("q4")
    m.Params.LogToConsole = 0
    taille=len(M)
    X=[]
    for i in range (taille):
        X.append([])
        for j in range (taille):
            X[i].append(m.addVar(vtype=g.GRB.BINARY, name="x_{}_{}".format(i+1,j+1)))

    min=m.addVar(vtype=g.GRB.CONTINUOUS, name="min")
    m.update()
    obj=0+min
    for i in range(taille):
        for j in range(taille):
            u=X[i][j]*M[i][j]
            obj+=u*eps    

    m.setObjective(obj, g.GRB.MAXIMIZE)

    for i in range(taille):
        m.addConstr(g.quicksum(X[i][j] for j in range(taille))==1)
    for j in range(taille):
        m.addConstr(g.quicksum(X[i][j] for i in range(taille))==1) 
    for i in range(taille):
        m.addConstr(min<=g.quicksum(X[i][j]*M[i][j] for j in range (taille))) #pour que min soit vraiment un minimum

    m.optimize()
    m.printAttr('X')
    pi=[0 for i in range(taille)]
    upi=[0 for i in range(taille)]
    ListeN=[]
    for i in range(taille):
        ListeN.append(i+1)
        for j in range(taille):
            if X[i][j].x!=0:
                print("π(a_{}) = o_{}".format(i+1, j+1))
                pi[i]=j+1
                upi[i]=M[i][j]
    print("\n")
    print("(Ne pas prendre en compte si ε relativement grand)\nλ = {}".format(min.x))
    affichage(ListeN, "π", pi)
    affichage(ListeN, "u", upi)
    print("\n")
    sat=satisfaction(pi,M)
    print("Satisfaction totale = {}".format(sat))
    print("Satisfaction moyenne = {}".format(sat/taille))
    print("(Valeur de la fonction objectif : {})".format(m.objVal))
    return min.x, pi, upi   

q4(U, 0.01)

def q5(M):
    print("---------------------------------------------------------------------------")
    print("Question 5\n")
    m=g.Model("q5")
    m.Params.LogToConsole = 0
    taille=len(M)
    obj=m.addVar(vtype=g.GRB.CONTINUOUS, name="obj")
    X=[]
    for i in range(taille):
        X.append([])
        for j in range(taille):
            X[i].append(m.addVar(vtype=g.GRB.BINARY, name="x_{}_{}".format(i+1,j+1)))
    m.update()
    m.setObjective(obj, g.GRB.MINIMIZE)
    for i in range(taille):
        m.addConstr(g.quicksum(X[i][j] for j in range(taille))==1)
    for j in range(taille):
        m.addConstr(g.quicksum(X[i][j] for i in range(taille))==1) 
    m.addConstrs(obj>=M[i][j]-g.quicksum(M[i][k]*X[i][k] for k in range(taille)) for i in range(taille) for j in range(taille))

    m.optimize()
    m.printAttr('X')
    pi=[0 for i in range(taille)]
    upi=[0 for i in range(taille)]
    ListeN=[]
    for i in range(taille):
        ListeN.append(i+1)
        for j in range(taille):
            if X[i][j].x!=0:
                print("π(a_{}) = o_{}".format(i+1, j+1))
                pi[i]=j+1
                upi[i]=M[i][j]
    print("\n")
    print("regret max = {}".format(m.objVal))
    affichage(ListeN, "π", pi)
    affichage(ListeN, "u", upi)
    print("\n")
    sat=satisfaction(pi,M)
    print("Satisfaction totale = {}".format(sat))
    print("Satisfaction moyenne = {}".format(sat/taille))
    print("(Valeur de la fonction objectif : {})".format(m.objVal))
    return m.objVal, pi, upi

q5(U)

seed(time())


def q6():
    print("---------------------------------------------------------------------------")
    print("Question 6\n")
    Listn=[]
    cpu_f=[]
    cpu_g=[]
    for i in range(5,100,5):
        Listn.append(i)

        #q4)
        start=time()
        for k in range(10):
            epsilon=1/(20*i) #pour assurer que la somme des utilités (fois) epsilon reste inférieure à 1
            q4(create_matrix(i),epsilon)
        end=time()
        cpu_f.append((end-start)/10)
        
        #q5)
        start=time()
        for k in range(10):
            q5(create_matrix(i))
        end=time()
        cpu_g.append((end-start)/10)


    plt.plot(Listn,cpu_f)
    plt.title("Temps CPU de l'optimisation au sens de f")
    plt.xlabel("Taille de l'instance (n)")
    plt.ylabel("Temps CPU (s)")
    plt.show()

    plt.plot(Listn,cpu_g)
    plt.title("Temps CPU de l'optimisation au sens de g")
    plt.xlabel("Taille de l'instance (n)")
    plt.ylabel("Temps CPU (s)")
    plt.show()

    plt.plot(Listn,cpu_f,label="f")
    plt.plot(Listn,cpu_g,label="g")
    plt.title("Comparaison entre f et g")
    plt.xlabel("Taille de l'instance (n)")
    plt.ylabel("Temps CPU (s)")
    plt.legend()
    plt.show()

# q6()
