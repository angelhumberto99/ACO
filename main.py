import numpy as np
import random
import decimal
from source.Graph import *
import matplotlib.pyplot as plt

def selection(candidates):
    # definimos las variables que nos ayudarán
    # a encontrar al candidato
    ranges = []
    acum = 0

    # ordenamos los datos
    candidates.sort()

    # generamos los rangos de los candidatos
    for i in candidates:
        acum += i
        ranges.append(acum)
    
    # generamos un número aleatorio entre 0 y 1
    r = float(decimal.Decimal(random.randrange(0,100))/100)

    # evaluamos que candidato será seleccionado
    for i in range(len(ranges)):
        if r <= ranges[i]:
            return candidates[i]

def get_path():
    aux = Graph(True)
    file = open("path.txt", "r")
    stringAux = ""
    lines = sum(1 for line in open('path.txt'))
    for i in range(lines):
        stringAux = file.readline()
        stringAux = stringAux[:-1].split(',')
        aux.CreateEdge(int(stringAux[0]), # origen
                       int(stringAux[1]), # destino
                       [float(stringAux[2]), # costo
                       1/float(stringAux[2]), # visibilidad
                       float(stringAux[3])]) # feromonas
    file.close()
    return aux
           
def explore(currentLoc, path):
    # obtenemos caminos y pesos
    paths = path.GetNeighbors(currentLoc)
    prob = []
    solutions = {}
    # calculamos la probabilidad de
    # seleccionar un camino
    for i in paths.keys():
        tau = paths[i][2]
        eta = paths[i][1]
        prob.append(np.abs(tau)*np.abs(eta))
    summation = np.sum(prob)
    candidates = np.array(prob)
    candidates = candidates * (1/summation)
    candidates = np.abs(candidates)
    pos = 0
    for i in paths.keys():
        solutions[candidates[pos]] = i
        pos += 1
    # obtenemos el camino a seguir
    sel = selection(candidates)
    return solutions[sel]

def get_distance(solution, path):
    costs = 0
    for i in range(len(solution)):
        if i + 1 == len(solution):
            break
        else:
            costs += path.GetCost(solution[i],solution[i+1])[0]
    return costs

def update_pheromones(path, antPath, lk):
    rho = 0.01 # taza de evaporación
    Q = 1 # aprendizaje

    # creamos un grafo con antPath
    auxG = Graph(True)
    for i in range(len(antPath)):
        if i + 1 == len(antPath):
            break
        else:
            auxG.CreateEdge(antPath[i],antPath[i+1],1)

    # actualizamos el valor de las feromonas
    costs = []
    for i in path.graph.keys():
        neighbors = path.GetNeighbors(i)
        for j in neighbors.keys():
            if auxG.IsEdge(i,j):
                costs.append(neighbors[j][:-1] + [(1 - rho)* neighbors[j][2] + Q/lk])
            else:
                costs.append(neighbors[j][:-1] + [(1 - rho)* neighbors[j][2]])

    del auxG
    auxG = Graph(True)
    pos = 0
    # actulizamos el grafo original
    for i in path.graph.keys():
        neighbors = path.GetNeighbors(i)
        for j in neighbors.keys():
            auxG.CreateEdge(i, j, costs[pos])
            pos += 1
    return auxG

def main():
    antPath = []
    pathSolution = []
    costSolution = []

    x = list(range(500))
    # caminos contiene (eta, tau, origen, destino y costo)
    path = get_path() 
    anthill = 1 # punto de partida
    food = 4 # objetivo

    for i in range(500):
        # recorremos el camino desde el hormigero hasta la comida
        currentLoc = anthill
        while currentLoc != food:
            antPath.append(currentLoc)
            currentLoc = explore(currentLoc, path)
        antPath.append(food)
        # guardamos la solución y costo total encontrada por iteración
        pathSolution.append(antPath[:])
        # obtenemos la distancia recorrida por la hormiga
        finalCost = get_distance(antPath, path)
        costSolution.append(finalCost)
        #limpiamos la solución auxiliar
        path = update_pheromones(path, antPath, finalCost)
        antPath.clear()
    
    # imprimimos las mejores y peores soluciones encontradas
    best = np.amin(costSolution)
    worst = np.amax(costSolution)
    for i in range(len(pathSolution)):
        if costSolution[i] == best:
            print("Mejor solución: ", pathSolution[i], " costo: ", best)
            break
    for i in range(len(pathSolution)):
        if costSolution[i] == worst:
            print("Peor solución: ", pathSolution[i], " costo: ", worst)
            break

    print("costo promedio de soluciones: ", np.average(costSolution))

    # graficamos los costos 
    fig = plt.figure(figsize=(5, 5))
    fig.tight_layout()
    plt1 = fig.add_subplot(1,1,1)
    plt1.plot(x, costSolution)
    plt1.set_title("Optimizacion por colonia de hormigas")
    plt.show()

if __name__ == "__main__":
    main()