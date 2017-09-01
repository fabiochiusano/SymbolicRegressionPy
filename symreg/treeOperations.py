import random as rnd
from tree import BinaryOperatorInternalNode
import generator as gtr

# Pure
def crossover(firstTree, secondTree):
	def substituteSubtree(tree, height, subtree):
		if tree.height() == height:
			return subtree

		if tree.op1.height() >= height and tree.op2.height() >= height:
			choice = rnd.randint(0, 1)
			if choice == 0:
				return BinaryOperatorInternalNode(tree.operator, substituteSubtree(tree.op1, height, subtree), tree.op2)
			else:
				return BinaryOperatorInternalNode(tree.operator, tree.op1, substituteSubtree(tree.op2, height, subtree))
		elif tree.op1.height() >= height:
			return BinaryOperatorInternalNode(tree.operator, substituteSubtree(tree.op1, height, subtree), tree.op2)
		elif tree.op2.height() >= height:
			return BinaryOperatorInternalNode(tree.operator, tree.op1, substituteSubtree(tree.op2, height, subtree))
		print("Problem in substitute subtree")
		return None

	split1 = rnd.randint(1, firstTree.height())
	split2 = rnd.randint(1, secondTree.height())
	subtree = getSubtreeAtHeight(secondTree, split2)
	return substituteSubtree(firstTree.clone(), split1, subtree.clone())

# Pure
def mutateNode(node, minValue, maxValue, variables, operators):
	if node.height() == 1:
		return gtr.getLeaf(minValue, maxValue, variables)
	return BinaryOperatorInternalNode(gtr.getOperator(operators), node.op1.clone(), node.op2.clone())

# Pure
def mutation(tree, minValue, maxValue, variables, operators):
	choice = rnd.randint(1,tree.numOfNodes())
	if choice == 1:
		return mutateNode(tree, minValue, maxValue, variables, operators)
	else:
		leftNodes = tree.op1.numOfNodes()
		rightNodes = tree.op2.numOfNodes()
		choice = rnd.randint(1, leftNodes + rightNodes)
		if choice <= leftNodes:
			return BinaryOperatorInternalNode(tree.operator, mutation(tree.op1, minValue, maxValue, variables, operators), tree.op2.clone())
		else:
			return BinaryOperatorInternalNode(tree.operator, tree.op1.clone(), mutation(tree.op2, minValue, maxValue, variables, operators))


# Pure
def getSubtreeAtHeight(tree, height):
	if tree.height() == height:
		return tree.clone()

	if tree.op1.height() >= height and tree.op2.height() >= height:
		choice = rnd.randint(0, 1)
		if choice == 0:
			return getSubtreeAtHeight(tree.op1, height)
		else:
			return getSubtreeAtHeight(tree.op2, height)
	elif tree.op1.height() >= height:
		return getSubtreeAtHeight(tree.op1, height)
	elif tree.op2.height() >= height:
		return getSubtreeAtHeight(tree.op2, height)
	print("Problem in get subtree: self.height = " + str(tree.height()) + " and height = " + str(height))
	print("self.op1.height = " + str(tree.op1.height()) + " and self.op2.height = " + str(tree.op2.height()))
	return None

# Pure
def pruneTreeForMaxHeight(tree, maxHeight, minValue, maxValue, variables):
	def pruneTreeAux(tree, maxHeight, counter, minValue, maxValue, variables):
		if tree.height() == 1:
			return tree.clone()
		if counter == maxHeight:
			return gtr.getLeaf(minValue, maxValue, variables)
		pruned1 = pruneTreeAux(tree.op1, maxHeight, counter + 1, minValue, maxValue, variables)
		pruned2 = pruneTreeAux(tree.op2, maxHeight, counter + 1, minValue, maxValue, variables)
		return BinaryOperatorInternalNode(tree.operator, pruned1, pruned2)
	return pruneTreeAux(tree, maxHeight, 1, minValue, maxValue, variables)

# Pure
def pruneTree(tree, minValue, maxValue, variables):
	choice = rnd.randint(0,tree.numOfInternalNodes())
	if choice == 0:
		return gtr.getLeaf(minValue, maxValue, variables)
	else:
		leftInternalNodes = tree.op1.numOfInternalNodes()
		rightInternalNodes = tree.op2.numOfInternalNodes()
		choice = rnd.randint(0, leftInternalNodes + rightInternalNodes)
		if choice <= leftInternalNodes:
			return BinaryOperatorInternalNode(tree.operator, pruneTree(tree.op1, minValue, maxValue, variables), tree.op2.clone())
		else:
			return BinaryOperatorInternalNode(tree.operator, tree.op1.clone(), pruneTree(tree.op2, minValue, maxValue, variables))