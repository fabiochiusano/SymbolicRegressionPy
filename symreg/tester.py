from subprocess import call

timesForCase = 20
numMembers = 100

percentages = [[0.75,0.1,0.1,0.05], # Lots of crossovers
[0.1,0.75,0.1,0.05], # Lots of mutations
[0.1,0.1,0.75,0.05], # Lots of random
[0.45, 0.45 , 0.05, 0.05], # Both crossovers and mutations
[0.45, 0.05, 0.45, 0.05], # Both crossovers and random
[0.05, 0.45, 0.45, 0.05]] # Both mutations and random

parentSelectionProbList = [0.1, 0.2, 0.3, 0.4]
shouldPruneForMaxHeight = "y"
verbose = "n"
shouldWriteToFile = "y"
outputFile = "results_complex.csv"

output = open(outputFile,"w")
output.write("crossover,mutation,random,copy,parent_selection,should_prune,last_gen\n")

""" One run for each percentage config.
Other parameters are:
- shouldPruneForMaxHeight = y
- parentSelectionProb = 0.2 """
print("Step 1")
for perc in percentages:
	print("1-x")
	for i in range(0, timesForCase):
		call(["python", "symreg.py",
			str(numMembers), str(perc[0]), str(perc[1]), str(perc[2]), str(perc[3]),
			str(parentSelectionProbList[1]), shouldPruneForMaxHeight,
			verbose, shouldWriteToFile, outputFile])


""" For percentages[0], percentages[1] and percentages[3], try all the different
values of parentSelectionProb.
- shouldPruneForMaxHeight = y """
print("Step 2")
for parentSelectionProb in parentSelectionProbList:
	print("2-x")
	# With percentages[0]
	perc = percentages[0]
	for i in range(0, timesForCase):
		call(["python", "symreg.py",
			str(numMembers), str(perc[0]), str(perc[1]), str(perc[2]), str(perc[3]),
			str(parentSelectionProb), shouldPruneForMaxHeight,
			verbose, shouldWriteToFile, outputFile])
	# With percentages[1]
	perc = percentages[1]
	for i in range(0, timesForCase):
		call(["python", "symreg.py",
			str(numMembers), str(perc[0]), str(perc[1]), str(perc[2]), str(perc[3]),
			str(parentSelectionProb), shouldPruneForMaxHeight,
			verbose, shouldWriteToFile, outputFile])
	# With percentages[3]
	perc = percentages[3]
	for i in range(0, timesForCase):
		call(["python", "symreg.py",
			str(numMembers), str(perc[0]), str(perc[1]), str(perc[2]), str(perc[3]),
			str(parentSelectionProb), shouldPruneForMaxHeight,
			verbose, shouldWriteToFile, outputFile])



output.close()