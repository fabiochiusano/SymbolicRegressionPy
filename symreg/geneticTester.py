from subprocess import call
from random import randint
import pandas as pd

# Pure
def mayChange(oldValue, newValue):
	choice = randint(1,4)
	if choice == 1:
		return newValue
	return oldValue

# Pure
def changePercentages(percentages):
	newPercentages = [p for p in percentages]
	index1 = randint(0, len(newPercentages) - 1)
	index2 = randint(0, len(newPercentages) - 1)
	while index1 == index2:
		index2 = randint(0, len(newPercentages) - 1)
	newPercentages[index1] += 0.05
	newPercentages[index2] -= 0.05
	return standardizePercentages(newPercentages)

# Pure
def standardizePercentages(percentages):
	total = sum(percentages)
	return [p / total for p in percentages]

# Pure
def selectNearInList(member, list):
	index = list.index(member)
	if index == 0:
		return 1
	elif index == len(list) - 1:
		return len(list) - 2
	else:
		choice = randint(0,1)
		if choice == 0:
			return index - 1
		else:
			return index + 1

numMembersList = [150]
probList = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
shouldPruneForMaxHeightList = ["n", "y"]
verbose = "n"
shouldWriteToFile = "y"
outputFile = "results.csv"

numOfSearches = 100
numOfTriesForSearches = 10

bestMean = 500

bestNumMembers = 150
bestPercentages = [0.5, 0.35, 0.1, 0.05] # crossover, mutation, random, copy
bestPruneProb = 0.1
bestShouldPruneForMaxHeight = "n"

for i in range(0, numOfSearches):
	if i == 0:
		bestNumMembers = 150
		numMembers = bestNumMembers
		bestPercentages = [0.5, 0.35, 0.1, 0.05] # crossover, mutation, random, copy
		percentages = bestPercentages
		bestPruneProb = 0.1
		pruneProb = bestPruneProb
		bestShouldPruneForMaxHeight = "n"
		shouldPruneForMaxHeight = bestShouldPruneForMaxHeight

	numMembers = 150
	percentages = mayChange(percentages, changePercentages(bestPercentages))
	pruneProb = mayChange(pruneProb, selectNearInList(bestPruneProb, probList))
	shouldPruneForMaxHeight = mayChange(shouldPruneForMaxHeight, shouldPruneForMaxHeightList[randint(0, 1)])

	for j in range(0, numOfTriesForSearches):
		call(["python", "symreg.py", str(numMembers), str(percentages[0]), str(percentages[1]), str(percentages[2]), str(percentages[3]), str(pruneProb), shouldPruneForMaxHeight, verbose, shouldWriteToFile, outputFile])

	dataset = pd.read_csv(outputFile)
	mean = sum(dataset.result) / len(dataset.result)

	if mean < bestMean:
		bestMean = mean
		bestNumMembers = numMembers
		bestPercentages = percentages
		bestPruneProb = pruneProb
		bestShouldPruneForMaxHeight = shouldPruneForMaxHeight
		print("Current best mean is " + str(bestMean) + " for nm " + str(numMembers) + " p " + str(percentages) + " pr " + str(pruneProb) + " shp " + str(shouldPruneForMaxHeight))

	output = open(outputFile,"w") # Empties the file
	output.write("members,crossover,mutation,random,copy,prune,pruneForHeight,result\n")
	output.close()