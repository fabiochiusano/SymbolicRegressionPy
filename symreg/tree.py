import math
import generator as gtr

class Tree(object):
	def __init__(self):
		""" Do nothing """



class Leaf(Tree):
	def __init__(self):
		""" Do nothing """

	def height(self):
		""" The height of a leaf is always 1 """
		return 1

	def numOfNodes(self):
		""" Returns the number of nodes, both internal
		and leaves, of the subtree with this node as root """
		return 1

	def numOfLeaves(self):
		""" Returns the number of leaves of the subtree with this node as root """
		return 1

	def numOfInternalNodes(self):
		""" Returns the number of internal nodes of the subtree with this node as root """
		return 0

class ValueLeaf(Leaf):
	def __init__(self, value):
		""" A ValueLeaf is a leaf that contains a constant value, e.g. ValueLeaf(3) """
		self.value = value

	def eval(self, d):
		""" The evaluation of a ValueLeaf returns the value it stores """
		return self.value

	def __str__(self):
		return str(self.value)

	def clone(self):
		return ValueLeaf(self.value)

class VariableLeaf(Leaf):
	def __init__(self, variable):
		""" A VariableLeaf is a leaf that contains a variable, e.g. VariableLeaf("x") """
		self.variable = variable

	def eval(self, d):
		""" The evaluation of a VariableLeaf returns the value
		associated to the variable that the VariableLeaf contains """
		return d[self.variable]

	def __str__(self):
		return str(self.variable)

	def clone(self):
		return VariableLeaf(self.variable)



class InternalNode(Tree):
	def __init__(self):
		""" Do nothing """

class BinaryOperatorInternalNode(InternalNode):
	def __init__(self, operator, op1, op2):
		""" A BinaryOperatorInternalNode is an internal node that has an operator and two operands """
		self.operator = operator
		self.op1 = op1
		self.op2 = op2

	def height(self):
		return 1 + max(self.op1.height(), self.op2.height())

	def numOfNodes(self):
		""" Returns the number of nodes, both internal
		and leaves, of the subtree with this node as root """
		return 1 + self.op1.numOfNodes() + self.op2.numOfNodes()

	def numOfLeaves(self):
		""" Returns the number of leaves of the subtree with this node as root """
		return self.op1.numOfLeaves() + self.op2.numOfLeaves()

	def numOfInternalNodes(self):
		""" Returns the number of internal nodes of the subtree with this node as root """
		return 1 + self.op1.numOfInternalNodes() + self.op2.numOfInternalNodes()

	def eval(self, d):
		""" Returns the result of the operator applied to the two operands """
		if self.operator == "+":
			return self.op1.eval(d) + self.op2.eval(d)
		elif self.operator == "*":
			return self.op1.eval(d) * self.op2.eval(d)
		else:
			return self.op1.eval(d) - self.op2.eval(d)

	def __str__(self):
		return "(" + str(self.op1) + str(self.operator) + str(self.op2) + ")"

	def clone(self):
		return BinaryOperatorInternalNode(self.operator, self.op1.clone(), self.op2.clone())