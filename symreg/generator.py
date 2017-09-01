import random as rnd
import tree



def getValueLeaf(minValue, maxValue):
	""" Returns a ValueLeaf whose value is a random number between minValue and maxValue """
	return tree.ValueLeaf(rnd.randint(minValue, maxValue))

def getVariableLeaf(variables):
	""" Returns a VariableLeaf with a random variable chosen from the list passed as argument """
	return tree.VariableLeaf(variables[rnd.randint(0, len(variables) - 1)])

def getLeaf(minValue, maxValue, variables):
	""" 50% returns a ValueLeaf, 50% returns a VariableLeaf """
	choice = rnd.randint(0,1)
	if choice == 0:
		return getValueLeaf(minValue, maxValue)
	else:
		return getVariableLeaf(variables)



def getOperator(operators):
	""" Returns a random operator chosen from the list passed as argument """
	return operators[rnd.randint(0, len(operators) - 1)]

def getTree(minHeight, maxHeight, minValue, maxValue, variables, operators):
	""" Returns a random tree where the path between each leaf
	and the root is long at least minHeight and at most maxHeight """
	height = rnd.randint(max(minHeight, 1), maxHeight)
	if height == 1:
		return getLeaf(minValue, maxValue, variables)
	else:
		operator = getOperator(operators)
		leftChild = getTree(minHeight - 1, maxHeight - 1, minValue, maxValue, variables, operators)
		rightChild = getTree(minHeight - 1, maxHeight - 1, minValue, maxValue, variables, operators)
		return tree.BinaryOperatorInternalNode(operator, leftChild, rightChild)