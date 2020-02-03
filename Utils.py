import random

from City import City
from Graph import Graph


def readFile(filename):

    '''
    Given a file name
    :return: information of clu-SPT Problem :
    name : name of instance
    dimension : number of vertex
    number_of_cluster : number of cluster
    clusterSection : set of vertex of each cluster
    clusterInfo : number of vertex of each cluster
    '''

    # Open file
    f = open(filename, 'r')

    # Read name
    info = f.readline().strip().split()
    name = info[2]

    # Read dimension
    f.readline()
    info = f.readline().strip().split()
    dimension = int(info[2])

    # Read number of clusters
    info = f.readline().strip().split()
    number_of_cluster = int(info[1])
    f.readline()
    f.readline()

    # Read position and build distance metrix
    position = []
    for i in range(dimension):
        info = f.readline().strip().split()
        position.append(City(int(info[1]), int(info[2])))
    distance = []
    for i in range(dimension):
        x = []
        for j in range(dimension):
            x.append(position[i].euclidDistance(position[j]))
        distance.append(x)
    f.readline()

    # Read source vertex and cluster section
    info = f.readline().strip().split()
    sourceVertex = int(info[1])
    clusterSection = []
    for i in range(number_of_cluster):
        info = f.readline().strip().split()
        x =[]
        index = 1
        while(int(info[index]) != -1):
            x.append(int(info[index]))
            index += 1
        clusterSection.append(x)

    # Re-order cluster section
    for i in range(number_of_cluster):
        for j in range(number_of_cluster-2,i-1,-1):
            if len(clusterSection[j]) < len(clusterSection[j+1]):
                temp = clusterSection[j]
                clusterSection[j] = clusterSection[j+1]
                clusterSection[j+1] = temp

    clusterInfo = []
    for i in range(number_of_cluster):
        clusterInfo.append(len(clusterSection[i]))

    f.close()

    return name, dimension, number_of_cluster, distance, clusterInfo, clusterSection, sourceVertex

def encode_Prufer_cluster(genes):
    '''
    given prufer code . Encode to the dictionary of graph

    '''
    # Initialize
    collections = []
    n = len(genes)
    degree = []
    for i in range(n + 2):
        degree.append(1)
    for i in range(n):
        degree[genes[i]] += 1

    # add edge
    for i in range(n):
        for j in range(n + 2):
            if degree[j] == 1:
                collections.append((genes[i], j))
                degree[genes[i]] -= 1
                degree[j] -= 1
                break

    # add final edge
    u = 0
    v = 0
    for i in range(n + 2):
        if degree[i] == 1:
            if u == 0:
                u = i
            else:
                v = i
                break
    collections.append((u, v))
    degree[u] -= 1
    degree[v] -= 1

    return collections

def encode_Prufer_graph(genes, clusterInfo, clusterSection, connector ):
    g = Graph([])
    start = 0
    length = len(clusterInfo)
    for i in range(length):
        if clusterInfo[i] > 2:
            gene = genes[start:start + max(clusterInfo[i] - 2, 1)]
            start += clusterInfo[i] - 2
            collection = encode_Prufer_cluster(gene)
            for u, v in collection:
                g.add(clusterSection[i][u], clusterSection[i][v])
        elif clusterInfo[i] is 2:
            g.add(clusterSection[i][0], clusterSection[i][1])
    gene = []
    for i in range(start, start+length -2):
        gene.append(genes[i])
    collection = encode_Prufer_cluster(gene)
    for u, v in collection:
        g.add(clusterSection[u][connector[u]], clusterSection[v][connector[v]])


    return g

def random_Prufer(clusterInfo):
    gen = []
    connector = []
    start = 0
    length = len(clusterInfo)
    for i in range(length):
        if clusterInfo[i] > 2:
            for j in range(start, start + clusterInfo[i] - 2):
                gen.append(random.randint(0, clusterInfo[i] - 1))
            start += clusterInfo[i] - 2
        else:
            gen.append(clusterInfo[i]-3)
            start += 1

    for i in range(start,start +length-2):
        gen.append(random.randint(0,length-1))

    for i in range(len(clusterInfo)):
        connector.append(random.randint(0,clusterInfo[i] -1))

    return gen, connector

def decodeMFO(genes,lstDecodePos,clusterInfo):
    decodegene = []
    index  = 0
    number = 0
    for i in lstDecodePos:
        index += 1
        if number < len(clusterInfo):
            if clusterInfo[number] > 2:
                decodegene.append(genes[i] % clusterInfo[number])
                if index == clusterInfo[number] - 2:
                    index = 0
                    number += 1
            else:
                decodegene.append(clusterInfo[number] - 3)
                index = 0
                number += 1

        else:
            decodegene.append(genes[i] % len(clusterInfo))


    return decodegene

def decodeConnectorMFO(clusterInfo, connector):
    decodeconnector = []
    for i in range(len(clusterInfo)):
        decodeconnector.append(connector[i] % clusterInfo[i])
    return decodeconnector


if __name__=='__main__':
    print('test')


