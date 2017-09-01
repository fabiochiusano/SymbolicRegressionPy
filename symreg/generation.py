import random as rnd
import generator as gtr
import treeOperations as trop

class Generation(object):
	def __init__(self):
		self.membersWithErrors = []

	def addMember(self, member):
		""" Add a tree to the generation """
		self.membersWithErrors.append([member, 0])

	def setMember(self, member, index):
		""" Updates the member at the specified position """
		self.membersWithErrors[index] = member

	def setError(self, index, error):
		""" Sets the error of the member at the specified position """
		self.membersWithErrors[index][1] = error

	def getMember(self, index):
		""" Returns the member at the specified position """
		return self.membersWithErrors[index][0]

	def getError(self, index):
		""" Returns the error of the member at the specified position """
		return self.membersWithErrors[index][1]

	def size(self):
		""" Returns the number of members curently in the generation """
		return len(self.membersWithErrors)

	def clear(self):
		""" Clears the generation, i.e. removes all the members """
		self.membersWithErrors.clear()

	def sort(self, descending):
		""" Sorts the members of the generation according the their score """
		self.membersWithErrors.sort(key = lambda l: l[1], reverse = descending)



	def getMembersForReproduction(self, numMembers, pickProb):
		""" Returns a certain number of distinct members from the generation.
		The first member is selected with probability pickProb. If it's not chosen, the 
		second member is selected with probability pickProb, and so on. """
		selectedMembers = []
		while len(selectedMembers) < numMembers:
			indexSelected = 0
			while rnd.randint(0, 100) > int(pickProb * 100) and indexSelected != len(self.membersWithErrors) - 1:
				indexSelected += 1
			memberWithErrorSelected = self.membersWithErrors[indexSelected]
			if memberWithErrorSelected[0] not in selectedMembers:
				selectedMembers.append(memberWithErrorSelected[0])
		return selectedMembers

	def next(self, crossoverPerc, mutationPerc, randomPerc, copyPerc, shouldPruneForMaxHeight, minHeight, maxHeight, minValue, maxValue, variables, operators):
		""" It proceeds to the next generation with the help of genetic operations """
		oldMembersWithError = self.membersWithErrors
		newMembersWithError = []
		maxMembers = len(oldMembersWithError)

		numCrossover = int(maxMembers * crossoverPerc)
		numMutation = int(maxMembers * mutationPerc)
		numRandom = int(maxMembers * randomPerc)
		numCopy = maxMembers - numCrossover - numMutation - numRandom

		# Crossover
		for i in range(0, numCrossover):
			members = self.getMembersForReproduction(2, 0.3)
			m1 = members[0]
			m2 = members[1]
			newMember = trop.crossover(m1, m2)
			newMembersWithError.append([newMember, 0])

		# Mutation
		for i in range(0, numMutation):
			m1 = self.getMembersForReproduction(1, 0.3)[0]
			newMembersWithError.append([trop.mutation(m1, minValue, maxValue, variables, operators), 0])

		# Random
		for i in range(0, numRandom):
			newMembersWithError.append([gtr.getTree(minHeight, maxHeight, minValue, maxValue, variables, operators), 0])

		# Copy
		members = self.getMembersForReproduction(numCopy, 0.3)
		for m in members:
			newMembersWithError.append([m.clone(), 0])

		self.membersWithErrors = newMembersWithError
