from random import randint
import tree as tr

def getTree(minHeight, maxHeight, minValue, maxValue, variables, operators):
	height = randint(minHeight, maxHeight)
	if height <= 1:
		return getLeaf(minValue, maxValue, variables)
	else:
		operator = getOperator(operators)
		leftChild = getTree(minHeight - 1, maxHeight - 1, minValue, maxValue, variables, operators)
		rightChild = getTree(minHeight - 1, maxHeight - 1, minValue, maxValue, variables, operators)
		return tr.BinaryOperatorInternalNode(operator, leftChild, rightChild)

def getLeaf(minValue, maxValue, variables):
	choice = randint(0,1)
	if choice == 0:
		return getValueLeaf(minValue, maxValue)
	else:
		return getVariableLeaf(variables)

def getValueLeaf(minValue, maxValue):
	return tr.ValueLeaf(randint(minValue, maxValue))

def getVariableLeaf(variables):
	return tr.VariableLeaf(variables[randint(0, len(variables) - 1)])

def getOperator(operators):
	return operators[randint(0, len(operators) - 1)]