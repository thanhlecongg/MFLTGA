import os
import random
import time

from Experiment import setUp, run
from Problem import Problem
from Utils import encode_Prufer_graph, decodeMFO, decodeConnectorMFO
import argparse
from tqdm import tqdm

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--popSize",type=int,default=100)
    parser.add_argument("--maxEval",type=int,default=1000000)
    parser.add_argument("--nSeed",type=int,default=30)
    parser.add_argument("--maxPunishment",type=int,default=3)
    parser.add_argument("--basic",type=str,default="Type_1_Small")
    args = parser.parse_args()
    popSize = args.popSize
    maxEvaluation = args.maxEval
    number_of_seed = args.nSeed
    maxPunishment = args.maxPunishment
    basic = args.basic
    path = "Input/" + basic + '.txt'
    f = open(path, "r")
    instance = []
    while (True):
        x = str(f.readline().strip().split()[0])
        if x == "EOF":
            break
        instance.append(x)
    outputPath = 'Result'+ '/' + basic + '/Pop'+ str(popSize) + '/Para_File(MFLTGA_Clus_Tree)'

    for a in range(0, len(instance), 2):
        task1 = instance[a]
        task2 = instance[a + 1]
        problem = []
        problem.append(Problem('Data/' + basic + '/' + task1 + '.clt'))
        problem.append(Problem('Data/' + basic + '/' + task2 + '.clt'))
        lsDecodePos, info, keyValue = setUp(problem)
        for b in range(number_of_seed):
            random.seed(b)
            start_time = time.time()
            best = run(popSize, info, problem, maxEvaluation, lsDecodePos, keyValue, maxPunishment)
            end_time = time.time()
            w = open(outputPath + '_Task_1(' + str(task1) + ')_seed(' + str(b) + ').opt', 'w')
            w.write('File name: ' + str(task1))
            w.write('\n')
            w.write('Seed: ' + str(b))
            w.write('\n')
            w.write('Fitness: ' + str(best[0].fitness[0]))
            w.write('\n')
            w.write('Time: ' + '{:.9f}'.format(end_time - start_time))
            w.write('\n')
            w.write('Graph: \n')
            gene = decodeMFO(best[0].genes, lsDecodePos[0], problem[0].clusterInfo, )
            connector = decodeConnectorMFO(problem[0].clusterInfo, best[0].connector)
            g = encode_Prufer_graph(gene, problem[0].clusterInfo, problem[0].clusterSection, connector)
            dict = g._graph
            for i in range(len(dict)):
                for j in range(len(dict)):
                    if dict[i].__contains__(j):
                        w.write(str(1) + " ")
                    else:
                        w.write(str(0) + " ")
                w.write("\n")
            w.close()
            w = open(outputPath + '_Task_2(' + str(task2) + ')_seed(' + str(b) + ').opt', 'w')
            w.write('File name: ' + str(task2))
            w.write('\n')
            w.write('Seed: ' + str(b))
            w.write('\n')
            w.write('Fitness: ' + str(best[1].fitness[1]))
            w.write('\n')
            w.write('Time: ' + '{:.9f}'.format(end_time - start_time))
            w.write('\n')
            w.write('Graph: \n')
            gene = decodeMFO(best[1].genes, lsDecodePos[1], problem[1].clusterInfo)
            connector = decodeConnectorMFO(problem[1].clusterInfo, best[1].connector)
            g = encode_Prufer_graph(gene, problem[1].clusterInfo, problem[1].clusterSection, connector)
            dict = g._graph
            for i in range(len(dict)):
                for j in range(len(dict)):
                    if dict[i].__contains__(j):
                        w.write(str(1) + " ")
                    else:
                        w.write(str(0) + " ")
                w.write("\n")
            w.close()
    f.close()


















