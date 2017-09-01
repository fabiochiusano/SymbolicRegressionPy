from random import uniform
from random import randint
import generator as gtr
import treeOperations as trop

class Generation(object):
	def __init__(self):
		self.membersWithErrors = []

	def addMember(self, member):
		self.membersWithErrors.append([member, 0])

	def setMember(self, member, index):
		self.membersWithErrors[index] = member

	def setError(self, index, error):
		self.membersWithErrors[index][1] = error

	def getMember(self, index):
		return self.membersWithErrors[index][0]

	def getError(self, index):
		return self.membersWithErrors[index][1]

	def size(self):
		return len(self.membersWithErrors)

	def clear(self):
		self.membersWithErrors.clear()

	def sort(self, descending):
		self.membersWithErrors.sort(key = lambda l: l[1], reverse = descending)




	def next(self, crossoverPerc, mutationPerc, randomPerc, copyPerc, pruneProb, shouldPruneForMaxHeight, minHeight, maxHeight, minValue, maxValue, variables, operators):
		oldMembersWithError = self.membersWithErrors
		newMembersWithError = []
		maxMembers = len(oldMembersWithError)

		numCrossover = int(maxMembers * crossoverPerc)
		numMutation = int(maxMembers * mutationPerc)
		numRandom = int(maxMembers * randomPerc)
		numCopy = maxMembers - numCrossover - numMutation - numRandom

		for i in range(0, numCrossover):
			index1 = randint(0, maxMembers - 1)
			index2 = randint(0, maxMembers - 1)
			while index1 == index2:
				index2 = randint(0, maxMembers - 1)
			m1 = self.getMember(index1)
			m2 = self.getMember(index2)
			newMember = trop.crossover(m1, m2)
			if shouldPruneForMaxHeight and newMember.height() > maxHeight:
				newMember = trop.pruneTreeForMaxHeight(newMember, maxHeight, minValue, maxValue, variables)
			newMembersWithError.append([newMember, 0])
		for i in range(0, numMutation):
			index1 = randint(0, maxMembers - 1)
			m1 = self.getMember(index1)
			newMembersWithError.append([trop.mutation(m1, minValue, maxValue, variables, operators), 0])
		for i in range(0, numRandom):
			newMembersWithError.append([gtr.getTree(minHeight, maxHeight, minValue, maxValue, variables, operators), 0])
		for i in range(0, numCopy):
			index1 = randint(0, maxMembers - 1)
			m1 = self.getMember(index1)
			newMembersWithError.append([m1.clone(), 0])

		for i in range(0, maxMembers):
			choice = randint(int(pruneProb * 100), 100)
			if choice <= int(pruneProb * 100):
				self.setMember(trop.pruneTree(self.getMember(i), minValue, maxValue, variables), i)

		self.membersWithErrors = newMembersWithError
