from collections import defaultdict
import math
import random
POPULATION=200
SELECTED_POPULATION=15
GENERATION=1000
ORDER_NUMBER=280
MUTATION_RATE=0.3
def GetDistance(taple1,taple2):
    return math.sqrt((taple1[0]-taple2[0])**2+(taple1[1]-taple2[1])**2)

class Gene:
    def __init__(self):
        self.patrollOrder=list(range(1,ORDER_NUMBER+1))
        random.shuffle(self.patrollOrder)

    def Evaluate(self,idPositionTable):
        result=0.0
        for num in range(0,ORDER_NUMBER-1):
            result+=GetDistance(idPositionTable[self.patrollOrder[num]],idPositionTable[self.patrollOrder[num+1]])
        self.evaluation=result
        return result

    def Mutation(self):
        random.shuffle(self.patrollOrder)


    @staticmethod
    def OrderCrossOver(gene1Origin,gene2Origin):
        crossPosition=random.randint(1,279)
        gene1OrderAfterCrossPoint=gene1Origin.patrollOrder[:crossPosition]
        gene2OrderAfterCrossPoint=gene2Origin.patrollOrder[:crossPosition]
        gene1CrossedOrderAfterCrossPoint=[]
        gene2CrossedOrderAfterCrossPoint=[]
        for element in gene2Origin.patrollOrder:
            if element in gene1OrderAfterCrossPoint:
                gene1CrossedOrderAfterCrossPoint.append(element)
        for element in gene1Origin.patrollOrder:
            if element in gene2OrderAfterCrossPoint:
                gene2CrossedOrderAfterCrossPoint.append(element)
        newGene1=Gene()
        newGene1.patrollOrder=gene1Origin.patrollOrder[crossPosition:]+gene1CrossedOrderAfterCrossPoint
        newGene2=Gene()
        newGene2.patrollOrder=gene2Origin.patrollOrder[crossPosition:]+gene2CrossedOrderAfterCrossPoint
        return (newGene1,newGene2)

    def SortGenesInEvaluation(genes):
        for i in range(0,len(genes)-1):
            for j in range(i+1,len(genes)):
                if genes[i].evaluation-genes[j].evaluation>0:
                    genes[i],genes[j]=genes[j],genes[i]
        return genes

    def EvaluateGenes(genes,idPositionTable):
        for gene in genes:
            gene.Evaluate(idPositionTable)

    def SelectGenes(genes):
        genes=genes[:SELECTED_POPULATION]
        return genes



def GetMasterData():
    path="C:/Users/chunn/Desktop/YNU/ソフトコンピューティング/kadai.txt"
    with open(path) as f:
        lines=f.readlines()
        idPositionTable=defaultdict(tuple)
        for line in lines:
            number=line.strip().split(' ')
            numbers=[s for s in number if s != '']
            if(numbers[0]!='EOF'):
                idPositionTable[int(numbers[0])]=(int(numbers[1]),int(numbers[2]))
    return idPositionTable

def InitializeGene(gene,idPositionTable):
    for person in range(0,POPULATION):
        genes.append(Gene())
        genes[person].Evaluate(idPositionTable)
    return genes

def AdvanceGeneration(genes):
    genes=Gene.SortGenesInEvaluation(genes)
    genes=Gene.SelectGenes(genes)
    geneChildren=[]
    for i in range(0,len(genes)-1):
        for j in range(i+1,len(genes)):
            children=Gene.OrderCrossOver(genes[i],genes[j])
            if random.random()<MUTATION_RATE:
                children[0].Mutation()
            if random.random()<MUTATION_RATE:
                children[1].Mutation()
            geneChildren.append(children[0])
            geneChildren.append(children[1])
    Gene.EvaluateGenes(geneChildren,idPositionTable)
    geneChildren=Gene.SortGenesInEvaluation(geneChildren)
    return geneChildren



idPositionTable=GetMasterData()
print(idPositionTable)
genes=[]
InitializeGene(genes,idPositionTable)
for count in range(0,GENERATION):
    genes=AdvanceGeneration(genes)
    print(genes[0].evaluation)
