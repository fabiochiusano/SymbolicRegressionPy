import generation as gn
import tree as tr
import generator as gtr
import math
import sys

#xs = [-5,-3,-2,-1,2,6,7]
#ys = [64,26,13,4,1,53,76] # 2x^2 - 3x - 1

xs = [-1, 1, 0, 3, -2, 0, -1, 3, 2, -2]
ys = [1, 1, 0, 2, -2, 5, 3, -1, 5, -4]
zs = [3, 3, 1, 12, 3, 6, 5, 9, 10, 1] # x^2 + y + 1

def main():
	minHeight = 1
	maxHeight = 5
	minValue = 1
	maxValue = 3
	variables = ["x", "y"]
	operators = ["+", "-", "*"]
	numOfMembers = int(sys.argv[1])
	maxNumOfGenerations = 500
	currentGen = 1
	crossoverPerc = float(sys.argv[2])
	mutationPerc = float(sys.argv[3])
	randomPerc = float(sys.argv[4])
	copyPerc = float(sys.argv[5])
	parentSelectionProb = float(sys.argv[6])
	shouldPruneForMaxHeight = sys.argv[7] == "y"
	verbose = sys.argv[8] == "y"
	shouldWriteToFile = sys.argv[9] == "y"
	outputFile = sys.argv[10]


	# Step 1: create first generation
	gen = gn.Generation()
	for i in range(0, numOfMembers):
		gen.addMember(gtr.getTree(minHeight, maxHeight, minValue, maxValue, variables, operators))

	d = {
		"crossoverPerc" : crossoverPerc,
		"mutationPerc" : mutationPerc,
		"randomPerc" : randomPerc,
		"copyPerc" : copyPerc,
		"shouldPruneForMaxHeight" : shouldPruneForMaxHeight,
		"parentSelectionProb" : parentSelectionProb
	}

	for genNum in range(0, maxNumOfGenerations):
		""" Step 2: evaluate all members """
		for memberNum in range(0, gen.size()):
			member = gen.getMember(memberNum)
			totalError = 0
			for i in range(0, len(xs)):
				res = member.eval({"x": xs[i], "y": ys[i]})
				error = math.fabs(zs[i] - res)
				totalError += error
			gen.setError(memberNum, totalError)

		""" Step 3: sort solutions according to errors """
		gen.sort(descending = False)

		""" Step 4: if best solution has error zero, then stop """
		if verbose:
			print("Best solution is " + str(gen.getMember(0)) + " with error " + str(gen.getError(0)) + "...")
		if gen.getError(0) == 0:
			break

		""" If limit reached, then stop process """
		if currentGen == maxNumOfGenerations:
			if verbose:
				print("LIMIT REACHED")
			break

		""" Step 5: produce next generation """
		if verbose:
			print("Producing gen number " + str(currentGen) + "...")
		gen.next(minHeight, maxHeight, minValue, maxValue, variables, operators, **d)
		currentGen += 1

	if verbose:
		print("END ~~~~~~~~~~~~~~~~~~~~~~~~")
		print("Best solution found:")
		print(str(gen.getMember(0)))
		print("with error")
		print(str(gen.getError(0)))

	if shouldWriteToFile:
		out_file = open(outputFile, "a")
		out_file.write(
			str(crossoverPerc) + "," +
			str(mutationPerc) + "," +
			str(randomPerc) + "," +
			str(copyPerc) + "," +
			str(parentSelectionProb) + "," +
			str(shouldPruneForMaxHeight) + "," +
			str(currentGen) + "\n")
		out_file.close()

if __name__ == "__main__":
    main()