import math
import random
from itertools import combinations

from Individual import Individual
from Utils import decodeMFO


class MFLTGA(object):
    '''

    '''

    def __init__(self, population,decodePos, skillFactor, keyValue, clusterInfo):
        self.keyValue = keyValue
        self.individuals = []
        for i in range(len(population)):
            if population[i].skillFactor is skillFactor:
                genes = decodeMFO(population[i].genes,decodePos,clusterInfo)
                self.individuals.append(genes)
        self.decodePos = decodePos

    def getMaskValue(self,individual, mask):
        return tuple(individual.genes[g] for g in mask)


    def setMarkValues(self, individual, mask, value):
        for valueIndex, geneIndex in enumerate(mask):
            individual.genes[geneIndex] = value[valueIndex]

    def applyMask(self, p1, p2, mask,problems, skillFactor,lstDecodePos):
        '''
        Used by two parent crossover to create an individual by coping the
        genetic information from p2 into a clone of p1 for all genes in the
        given mask.  Returns the newly created individual.

        Parameters:

        - ``p1``: The first parent.
        - ``p2``: The second parent.
        - ``mask``: The list of indices used in this crossover.
        '''
        maskSet = set(mask)
        genes = [p2.genes[g] if g in maskSet else p1.genes[g]
                           for g in range(len(p1.genes))]
        connector = p1.connector
        fitness = []
        for i in range(len(problems)):
            if i is skillFactor:
                fitness.append(problems[skillFactor].computeFitness(genes,connector,lstDecodePos[skillFactor]))
            else:
                fitness.append(0)
        ind = Individual(genes,fitness,connector)
        ind.updateSkillFactor(skillFactor)
        return ind

    def adjacencyInfo(self,c1, c2, aIlookup,keyValue):
        if (c1, c2) in aIlookup:
            return aIlookup[c1, c2]
        else:
            value = 0
            for i in range(len(self.individuals)):
                value += (keyValue[self.individuals[i][c1]] - keyValue[self.individuals[i][c2]])**2



            value = 1 - value/len(self.individuals)
            aIlookup[c1, c2] = value
            return value

    def crossEntropy(self,c1, c2, cElookup,keyValue):
        if (c1, c2) in cElookup:
            return cElookup[c1, c2]
        else:
            prob = 0
            for i in range(len(self.individuals)):
                if keyValue[self.individuals[i][c1]] < keyValue[self.individuals[i][c2]]:
                    prob += 1
            prob /= len(self.individuals)
            if prob == 0 or prob == 1 :
                value = 0
            else:
                value = 1 + (prob*math.log(prob,2) + (1-prob)*math.log(1-prob,2))
            cElookup[c1, c2] = value
            return value

    def clusterDistance(self, c1, c2, cElookup, aIlookup, dislookup,keyValue):
        if (c1, c2) in dislookup:
            return dislookup[c1, c2]
        else:
            value = self.adjacencyInfo(c1, c2, aIlookup,keyValue)*self.crossEntropy(c1, c2, cElookup,keyValue)
            dislookup[c1, c2] = value
            dislookup[c2, c1] = value
            return value

    def pairwiseDistance(self,c1, c2, cElookup, aIlookup, dislookup,keyValue):
        if (c1, c2) in dislookup :
            return dislookup[c1, c2]
        else:
            result = 0
            for a in c1 :
                for b in c2:
                    result += self.clusterDistance(a, b, cElookup, aIlookup, dislookup,keyValue)
            result /= float(len(c1)*len(c2))
            dislookup[c1, c2] = result
            dislookup[c2, c1] = result
            return result


    def buildTree(self):
        '''
        Given a method of calculating distance, build the linkage tree for the
        current population.  The tree is built by finding the two clusters with
        the minimum distance and merging them into a single cluster.  The
        process is initialized with all possible clusters of size 1 and ends
        when only a single cluster remains.  Returns the subtrees in the order
        they were created.

        Parameters:

        - ``distance``: The method of calculating distance.  Current options
          are ``self.clusterDistance`` and ``self.pairwiseDistance``
        '''
        clusters = [(i, ) for i in range(len(self.individuals[0]))]
        subtrees = [(i, ) for i in range(len(self.individuals[0]))]
        random.shuffle(clusters)
        random.shuffle(subtrees)
        dislookup = {}
        aIlookup = {}
        cElookup = {}

        def allLowest():
            '''
            Internal function used to find the list of all clusters pairings
            with the current smallest distances.
            '''
            minVal = 3  # Max possible distance should be 2
            results = []
            for c1, c2 in combinations(clusters, 2):
                result = self.pairwiseDistance(c1, c2, cElookup, aIlookup, dislookup,self.keyValue)
                if result < minVal:
                    minVal = result
                    results = [(c1, c2)]
                if result == minVal:
                    results.append((c1, c2))
            return results

        while len(clusters) > 1:
            c1, c2 = random.choice(allLowest())
            clusters.remove(c1)
            clusters.remove(c2)
            combined = c1 + c2
            clusters.append(combined)
            # Only add it as a subtree if it is not the root
            if len(clusters) != 1:
                subtrees.append(combined)
        return subtrees

    def leastLinkedFirst(self, subtrees, lstDecodePos):
        '''
        Reorders the subtrees such that the cluster pairs with the least
        linkage appear first in the list.  Assumes incoming subtrees are
        ordered by when they were created by the ``self.buildTree`` function.

        Parameters:

        - ``subtrees``: The list of subtrees ordered by how they were
          originally created.
        '''
        self.masks = []
        tree = list(reversed(subtrees))
        for mask in tree :
            maskSet = set(mask)
            newMask = ()
            for i in maskSet:
                newMask += (lstDecodePos[i],)
            self.masks.append(newMask)


    def twoParentCrossover_1child(self,problems, p1,p2,skillFactor,lstDecodePos):
        '''
        Creates individual generator using the two parent crossover variant.
        Uses coroutines to send out individuals and receive their fitness
        values.  Terminates when a complete evolutionary generation has
        finished.

        Parameters:

        - ``masks``: The list of crossover masks to be used when generating
          individuals, ordered based on how they should be applied.
        '''
        for mask in self.masks:
            c1 = self.applyMask(p1, p2, mask, problems, skillFactor,lstDecodePos)
            c2 = self.applyMask(p2, p1, mask, problems, skillFactor,lstDecodePos)
            # if the best child is better than the best parent
            if min(p1.fitness[skillFactor], p2.fitness[skillFactor])\
                    > min(c1.fitness[skillFactor], c2.fitness[skillFactor]):
                p1, p2 = c1, c2
            else:
                p1.updateUnchange()
                p2.updateUnchange()
        # Overwrite the parents with the modified version
        if p1.fitness[skillFactor] < p2.fitness[skillFactor]:
            return p1
        else:
            return p2









