import random as rnd
import tree as tr
import generator as gtr

# No side effects
def crossover(firstTree, secondTree):
	""" It produces a new tree, that is the result of
	a random crossover of firstTree and secondTree """
	def substituteSubtree(tree, height, subtree):
		if tree.height() == height:
			return subtree

		if tree.op1.height() >= height and tree.op2.height() >= height:
			choice = rnd.randint(0, 1)
			if choice == 0:
				return tr.BinaryOperatorInternalNode(tree.operator, substituteSubtree(tree.op1, height, subtree), tree.op2)
			else:
				return tr.BinaryOperatorInternalNode(tree.operator, tree.op1, substituteSubtree(tree.op2, height, subtree))

		elif tree.op1.height() >= height:
			return tr.BinaryOperatorInternalNode(tree.operator, substituteSubtree(tree.op1, height, subtree), tree.op2)

		else:
			return tr.BinaryOperatorInternalNode(tree.operator, tree.op1, substituteSubtree(tree.op2, height, subtree))

	split1 = rnd.randint(1, firstTree.height())
	split2 = rnd.randint(1, secondTree.height())
	subtree = getSubtreeAtHeight(secondTree, split2)
	return substituteSubtree(firstTree.clone(), split1, subtree.clone())

# No side effects
def mutateNode(node, minValue, maxValue, variables, operators):
	""" Mutate the node passed as argument. If it's a leaf, than it returns a new random leaf.
	If it's a BynaryOperatorInternalNode, then it changes its operator and copies the children """
	if node.height() == 1:
		return gtr.getLeaf(minValue, maxValue, variables)
	return tr.BinaryOperatorInternalNode(gtr.getOperator(operators), node.op1.clone(), node.op2.clone())

# No side effects
def mutation(tree, minValue, maxValue, variables, operators):
	""" Mutate the tree passed as argument """
	choice = rnd.randint(1,tree.numOfNodes())
	if choice == 1:
		return mutateNode(tree, minValue, maxValue, variables, operators)
	else:
		leftNodes = tree.op1.numOfNodes()
		rightNodes = tree.op2.numOfNodes()
		choice = rnd.randint(1, leftNodes + rightNodes)
		if choice <= leftNodes:
			return tr.BinaryOperatorInternalNode(tree.operator, mutation(tree.op1, minValue, maxValue, variables, operators), tree.op2.clone())
		else:
			return tr.BinaryOperatorInternalNode(tree.operator, tree.op1.clone(), mutation(tree.op2, minValue, maxValue, variables, operators))


# No side effects
def getSubtreeAtHeight(tree, height):
	""" Returns a random subtree taken from the specified tree at the specified height.
	It creates a copy of such subtree """
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
	else:
		return getSubtreeAtHeight(tree.op2, height)

# No side effects
def pruneTreeForMaxHeight(tree, maxHeight, minValue, maxValue, variables):
	""" Returns a new tree that is like the specified tree
	but pruned so that its height is maxHeight """
	def pruneTreeAux(tree, maxHeight, counter, minValue, maxValue, variables):
		if tree.height() == 1:
			return tree.clone()
		if counter == maxHeight:
			return gtr.getLeaf(minValue, maxValue, variables)
		pruned1 = pruneTreeAux(tree.op1, maxHeight, counter + 1, minValue, maxValue, variables)
		pruned2 = pruneTreeAux(tree.op2, maxHeight, counter + 1, minValue, maxValue, variables)
		return tr.BinaryOperatorInternalNode(tree.operator, pruned1, pruned2)
	return pruneTreeAux(tree, maxHeight, 1, minValue, maxValue, variables)

# No side effects
def pruneTree(tree, minValue, maxValue, variables):
	""" Returns a copy of the specified tree with a random branch pruned """
	choice = rnd.randint(0,tree.numOfInternalNodes())
	if choice == 0:
		return gtr.getLeaf(minValue, maxValue, variables)
	else:
		leftInternalNodes = tree.op1.numOfInternalNodes()
		rightInternalNodes = tree.op2.numOfInternalNodes()
		choice = rnd.randint(0, leftInternalNodes + rightInternalNodes)
		if choice <= leftInternalNodes:
			return tr.BinaryOperatorInternalNode(tree.operator, pruneTree(tree.op1, minValue, maxValue, variables), tree.op2.clone())
		else:
			return tr.BinaryOperatorInternalNode(tree.operator, tree.op1.clone(), pruneTree(tree.op2, minValue, maxValue, variables))