import random

from Individual import Individual
from MFLTGA import MFLTGA
from Utils import *


def createInitialPopulation(popSize, info, problems,lstDecodePos, nTask):
    population = []
    for i in range(popSize):
        genes, connector = random_Prufer(info)
        fitness = []
        for j in range(nTask):
            fitness.append(problems[j].computeFitness(genes,connector,lstDecodePos[j]))

        ind = Individual(genes, fitness, connector)
        population.append(ind)
    return population

def getbestSolution(population, task):
    best = population[0]
    for i in range(len(population)):
        if best.fitness[task] > population[i].fitness[task] :
            best = Individual(population[i].genes,population[i].fitness,best.connector)
            best.skillFactor = population[i].skillFactor
    return best

    # newPop = []
    # for i in range(popSize):
    #     newPop.append(population[rankScalar.index(i)])


def updateSkillFactor(population, nTask):
    ranks = []
    for i in range(nTask):
        rank = []
        for j in range(len(population)):
            rank.append(j)
        for j in range(len(population)):
            for k in range(len(population)-2, j-1,-1):
                if population[rank.index(k)].fitness[i] - population[rank.index(k+1)].fitness[i] > 0:
                    tm = rank.index(k)
                    rank[rank.index(k+1)] = k
                    rank[tm] = k+1
        ranks.append(rank)
    for i in range(len(population)):
        skillFactor = 0
        for j in range(nTask):
            if ranks[skillFactor][i] > ranks[j][i]:
                skillFactor = j
        population[i].updateSkillFactor(skillFactor)

def selection(offspring, nTask, popSize):
    ranks = []
    for i in range(nTask):
        rank = []
        for j in range(len(offspring)):
            rank.append(j)
        for j in range(len(offspring)):
            for k in range(len(offspring) - 2, j - 1, -1):
                if offspring[rank.index(k)].fitness[i] - offspring[rank.index(k + 1)].fitness[i] > 0:
                    tm = rank.index(k)
                    rank[rank.index(k + 1)] = k
                    rank[tm] = k + 1
        ranks.append(rank)
    scalarFitness = []
    for i in range(len(offspring)):
        skillFactor = 0
        for j in range(nTask):
            if ranks[skillFactor][i] > ranks[j][i]:
                skillFactor = j
        scalarFitness.append(ranks[skillFactor][i]+1)
    rankScalar = []
    for j in range(len(offspring)):
        rankScalar.append(j)
    for j in range(len(offspring)):
        for k in range(len(offspring) - 2, j - 1, -1):
            if scalarFitness[rankScalar.index(k)] - scalarFitness[rankScalar.index(k + 1)] > 0:
                tm = rankScalar.index(k)
                rankScalar[rankScalar.index(k + 1)] = k
                rankScalar[tm] = k + 1

    newPop  = []
    for i in range(popSize):
        newPop.append(offspring[rankScalar.index(i)])

    return newPop

def run(popSize, info, problems, maxEvaluation, lstDecodePos, keyValue, maxPunishment):
    nTask = len(problems)
    treeSize = []
    for i in range(len(lstDecodePos)):
        treeSize.append(2*(len(lstDecodePos[i])) - 1)
    population = createInitialPopulation(popSize,info,problems,lstDecodePos,nTask)
    evaluation = popSize*nTask
    updateSkillFactor(population, nTask)
    iteration = 0
    print("Iteration :" + str(iteration))
    best = []
    print("Population : " + str(len(population)))
    for task in range(nTask):
        best.append(getbestSolution(population, task))
    for task in range(nTask):
        print("best solution task " + str(task) + " : " + str(best[task].__str__()))

    optimal = False
    while(evaluation < maxEvaluation and not optimal):
        print(evaluation)
        iteration += 1
        print("Iteration :" + str(iteration))
        optimizers = []
        for i in range(nTask):
            optimizers.append(MFLTGA(population, lstDecodePos[i],i,keyValue[i],problems[i].clusterInfo))

        for i in range(nTask):
            optimizers[i].leastLinkedFirst(optimizers[i].buildTree(), lstDecodePos[i])
        backup = []
        offspring = []
        # Does the following twice in order to make enough children
        random.shuffle(population)
        # pairs off paren ts with their neighbor
        #
        # for mask in linkageTree[0]:
        #     print(mask)
        for x in range(2):
            for i in range(0, len(population) - 1, 2):
                p1 = population[i]
                p2 = population[i + 1]
                if p1.skillFactor is p2.skillFactor:
                    sF = p1.skillFactor

                else:
                    if random.random() < 0.5:
                        sF = p1.skillFactor
                        temp = Individual(p2.genes, p2.fitness, p2.connector)
                        temp.updateSkillFactor(p2.skillFactor)
                        backup.append(temp)
                    else:
                        sF = p2.skillFactor
                        temp = Individual(p1.genes, p1.fitness, p1.connector)
                        temp.updateSkillFactor(p1.skillFactor)
                        backup.append(temp)
                o = optimizers[sF].twoParentCrossover_1child(problems, p1, p2, sF, lstDecodePos)
                evaluation += 2*treeSize[sF]
                # offspring.append(o1)
                offspring.append(o)
                if p1.unchange > maxPunishment and p1.fitness > best[p1.skillFactor].fitness:
                    p1.mutation(info, problems, lstDecodePos)
                if p2.unchange > maxPunishment and p2.fitness > best[p2.skillFactor].fitness:
                    p2.mutation(info, problems, lstDecodePos)


        for i in range(len(backup)):
            offspring.append(backup[i])
        population = selection(offspring,nTask,popSize)
        best = []
        for task in range(nTask):
            best.append(getbestSolution(population, task))
        for task in range(nTask):
            print("best solution task " + str(task) + " : " + str(best[task].__str__()))

    return best


def setUp(problem):
    maxCluster = max(len(problem[0].clusterInfo), len(problem[1].clusterInfo))
    info = []
    for i in range(maxCluster):
        if i <= len(problem[0].clusterInfo)-1 and i <= len(problem[1].clusterInfo) -1:
            info.append(max(problem[0].clusterInfo[i],problem[1].clusterInfo[i]))
        else:
            if i > len(problem[1].clusterInfo)-1:
                info.append(problem[0].clusterInfo[i])
            if i > len(problem[0].clusterInfo)-1:
                info.append(problem[1].clusterInfo[i])
    lstDecodePos = []
    keyValue = []
    for i in range(2):
        start = 0
        x = []
        for j in range(maxCluster):
            if j < len(problem[i].clusterInfo):
                for k in range(start, start + problem[i].clusterInfo[j]-2):
                    x.append(k)

            start += info[j]-2
        for j in range(start, start + len(problem[i].clusterInfo)-2):
            x.append(j)
        lstDecodePos.append(x)
        keyValueEachTask = []
        maxValue = max(problem[i].clusterInfo[0], len(problem[i].clusterInfo))
        for i in range(maxValue):
            keyValueEachTask.append(i / maxValue + random.random() / pow(10, 6))
        keyValue.append(keyValueEachTask)
    return lstDecodePos, info, keyValue

















