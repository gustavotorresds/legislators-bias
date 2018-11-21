import csv
from tabulate import tabulate
import math

# This is example code that loads each of the CSV files.
# Feel free to use this code in your solution. Don't forget
# to import csv
def main():
	repsToParties = loadRepsToProperty('data/repsParties.csv')
	repsToStates = loadRepsToProperty('data/repsStates.csv')

	repsToVotes = loadVotes('data/repsVotes.csv')
	partiesToVotes = loadVotes('data/partiesVotes.csv')
	companiesToVotes = loadVotes('data/companiesVotes.csv')
	citizensToVotes = loadVotes('data/citizensVotes.csv')

	getCompaniesInfluence(repsToVotes, companiesToVotes)
	getPartyInfluence(repsToParties, partiesToVotes, repsToVotes)
	getCitizensInfluence(repsToStates, repsToVotes, citizensToVotes)

def getCitizensInfluence(repsToStates, repsToVotes, citizensToVotes):
	print ''
	print 'USERS INFLUENCE'
	countryVotes = citizensToVotes['Total']
	for rep in repsToVotes:
		table = []
		print '--------------------------------------------------------------------------REP: ' + rep + '-----------------------------------------------------------------'
		repVotes = repsToVotes[rep]
		repState = repsToStates[rep]
		stateVotes = citizensToVotes[repState]

		stateRow = [repState]
		stateRow.extend(findElementInfluence(repVotes, stateVotes, 7))
		countryRow = ['Total']
		countryRow.extend(findElementInfluence(repVotes, countryVotes, 7))

		table.append(stateRow)
		table.append(countryRow)

		print tabulate(table, headers=["Region", "P(R = 1 | P = 0)", "P(R = 1 | P = 1)", "P(R = 1 | P = 2)", 
			"P(R = 1 | P = 3)", "P(R = 1 | P = 4)", "P(R = 1 | P = 5)", "P(R = 1 | P = 6)"])
		print ''

def findElementInfluence(repVotes, elementVotes, numOptions=2):
	repAndElement = numOptions * [0]
	elementCounts = numOptions * [0]

	for i in range(len(repVotes)):
		elementVote = elementVotes[i]
		if elementVote == -1: continue
		repVote = repVotes[i]
		elementCounts[elementVote] += 1
		if repVote == 1: repAndElement[elementVote] += 1

	# TODO: fix this. Shouldn't just return 0. -1 maybe?
	probs = [(round(float(repAndElement[i])/elementCounts[i], 2) if elementCounts[i] > 0 else 0.0) for i in range(numOptions)]
	return probs

def getPopulationInfluence(citizensVotes, repsToVotes):
	print ''
	print 'POPULATION INFLUENCE'
	table = []

	for rep in repsToVotes:
		row = [rep]
		repVotes = repsToVotes[rep]

		numerator = 0
		denominator = 0

		for i in range(len(citizensVotes)):
			citizensVote = citizensVotes[i][0]
			numCitizens = citizensVotes[i][1]
			repVote = repVotes[i]

			if(repVote == citizensVote): numerator += (math.log(numCitizens))
			denominator += math.log(numCitizens)

		prob = float(numerator)/denominator
		row.append(prob)
		table.append(row)

	print tabulate(table, headers=["REP", "P(R = P)"])

def getCompaniesInfluence(repsToVotes, companiesToVotes):
	print 'COMPANIES INFLUENCE'

	for rep in repsToVotes:
		print '--------------------REP: ' + rep + '-------------------'
		repVotes = repsToVotes[rep]

		table = []
		for company in companiesToVotes:
			companyVotes = companiesToVotes[company]
			influence = findElementInfluence(repVotes, companyVotes)
			
			row = [company]
			row.extend(influence)
			table.append(row)
		print tabulate(table, headers=["Company", "P(R = 1 | C = 1)", "P(R = 1 | C = 0)"])
		print ''

def getPartyInfluence(repsToParties, partiesToVotes, repsToVotes):
	print 'PARTIES INFLUENCE'
	table = []

	for rep in repsToVotes:
		repVotes = repsToVotes[rep]
		party = repsToParties[rep]
		partyVotes = partiesToVotes[party]

		influence = findElementInfluence(repVotes, partyVotes)
		row = [rep]
		row.extend(influence)
		table.append(row)

	print tabulate(table, headers=["Rep","P(R = 1 | P = 1)","P(R = 1 | P = 0)"])

def loadRepsToProperty(filename):
	repsToProperty = {}
	reader = csv.reader(open(filename))
	for row in reader:
		repsToProperty[row[0]] = row[1]
	return repsToProperty

def loadVotes(filename):
	smthToVotes = {}
	reader = csv.reader(open(filename))
	for index, row in enumerate(reader):
		if index == 0: continue # skip header
		smthToVotes[row[0]] = [int(i) for i in row[1::]]
	return smthToVotes

if __name__ == '__main__':
	main()
