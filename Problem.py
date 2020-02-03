import collections

from Utils import readFile, encode_Prufer_graph, decodeMFO, decodeConnectorMFO


class Problem :
    def __init__(self,filename):
        '''
        Given a file path to init cluster shortest path tree Problem
        '''
        self.name, self.dimension, self.number_of_cluster, self.distance, self.clusterInfo, self.clusterSection,self.sourceVertex = readFile(filename)

    def __str__(self):
        '''
        :return: info about problem
        '''
        return "name : " + str(self.name) + " | " + "dimension : " + str(self.dimension) \
               + " | " + "number of cluster : " +str(self.number_of_cluster)

    def computeFitness(self, genes, connector, lstDecodePos):
        decodeGene = decodeMFO(genes,lstDecodePos,self.clusterInfo)
        decodeConnector = decodeConnectorMFO(self.clusterInfo,connector)
        graph = encode_Prufer_graph(decodeGene,self.clusterInfo,self.clusterSection,decodeConnector)
        path = {}
        fitness = 0.0
        path[self.sourceVertex] = 0.0
        seen, queue = {self.sourceVertex}, collections.deque([self.sourceVertex])
        while queue:
            vertex = queue.popleft()
            for node in graph._graph[vertex]:
                if node not in seen:
                    seen.add(node)
                    queue.append(node)
                    path[node] = path[vertex] + self.distance[vertex][node]
        for i in path:
            fitness += path[i]

        return fitness

    def decodeMFO(self, genes, lstDecodePos):
        gene = []
        for i in lstDecodePos:
            gene.append(genes[i])

if __name__=='__main__':
    print(Problem('Data/Type_1_Large/10a280.clt').__str__())
