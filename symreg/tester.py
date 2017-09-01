from subprocess import call

timesForCase = 20
tryMembers = [10,20,30,50,100,200]

for numMembers in tryMembers:
	for i in range(0, timesForCase):
		call(["python", "symreg.py", str(numMembers), "0.5", "0.3", "0.1"])