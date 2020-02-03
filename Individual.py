import random
import sys

from Utils import random_Prufer


class Individual(object):

    def __init__(self, genes, fitness, connector):
        self.genes = genes
        self.fitness = fitness
        self.connector = connector
        self.unchange = 0

    def updateSkillFactor(self,skillFactor):
        self.skillFactor = skillFactor
        for i in range(len(self.fitness)):
            if i is not skillFactor:
                self.fitness[i] = sys.maxsize

    def updateUnchange(self):
        self.unchange +=1

    def mutation(self, info, problems, lstDecodePos):
        self.genes, self.connector = random_Prufer(info)
        self.fitness = []
        for j in range(len(problems)):
            if j is self.skillFactor:
                self.fitness.append(problems[j].computeFitness(self.genes, self.connector, lstDecodePos[j]))
            else:
                self.fitness.append(sys.maxsize)
        self.unchange = 0


    def getDivNumber(self,index,info):
        n = 0
        max = 0
        for i in range(len(info)+1):
            if i is not len(info):
                max += info[i]-2
                if index < max:
                    n = i
            else:
                n = len(info)
        return n




    def __cmp__(self, other):

        if self.fitness > other.fitness:
            return 1
        elif self.fitness < other.fitness:
            return -1
        else:
            return 0


    def __str__(self):
        '''
        Converts the individual into a string representation useful for
        displaying an individual.
        '''
        return "%s" % (str(self.fitness))

    def __int__(self):
        '''
        Converts a binary individual's genes into a single integer.  Useful
        for uniqueness checking.
        '''
        return int("".join(map(str, self.genes)), 2)

    def __hash__(self):
        '''
        Returns the value of ``__int__``, used when determinging sets of unique
        individuals.
        '''
        return int(self)