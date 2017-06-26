import math
import random

class Stock:
	allocationLabels = [
		"Domestic",
		"Foreign ",
		"Emerging",
		"REIT    ",
		"Bonds   ",
		"TIPS    "
	]

	def __init__(self, name, allocation, style):
		self.dollarValue = 0
		self.name = name
		self.allocation = allocation
		self.style = style

		# if abs(sum(self.allocation) - 1) > .01:
		# 	print("Possible incomplete stock " + self.name + " " + str(self.allocation))

	def __str__(self):
		out = self.name + ":"
		if self.dollarValue > 0:
			out += " ("+str(self.dollarValue) + ")\n"
		else:
			out += "\n"

		for i in range(len(Stock.allocationLabels)):			
			out += "  %s\t%0.2f%%\t(%d)\n"%(Stock.allocationLabels[i], self.allocation[i]*100, self.allocation[i]*self.dollarValue) 
		return out

	def toDollars(self):
		return [x*self.dollarValue for x in self.allocation]

	def styleToDollars(self):
		return [x*self.dollarValue for x in self.style]		

	def __add__(self, otherStock):
		myDollars = self.toDollars()
		otherDollars = otherStock.toDollars()

		totalDollars = sum(myDollars) + sum(otherDollars)
		# dollarAllocation = []
		newAllocation = []
		newStyle = []
		for i in range(len(Stock.allocationLabels)):
			newAllocation += [(myDollars[i] + otherDollars[i])/totalDollars]
		myStyleDollars = self.styleToDollars()
		otherStyleDollars = otherStock.styleToDollars()
		for i in range(9):			
			newStyle += [(myStyleDollars[i] + otherStyleDollars[i])/totalDollars]
		newStock = Stock(self.name, newAllocation, newStyle)
		newStock.dollarValue = totalDollars
		return newStock

	def __mul__(self, dollarValue):
		newStock = Stock(self.name, self.allocation, self.style)		
		newStock.dollarValue = dollarValue
		return newStock

def getBucketMinError(bucket, target, current, increment):
	if increment > 0:
		increment = min(bucket["contribution"], increment)
	minError = None
	minStock = None
	for stockName in bucket["stockOptions"]:
		stock = stocks[stockName]
		error = getError(target, current+stock*increment)/getError(target, current)
		if minError == None or error < minError:
			minError = error
			minStock = stock
	return minError, minStock

def getError(target, current):
	allocationError = getAllocationError(target, current)
	styleError = getStyleError(target, current)
	return allocationError + styleError/4
		
def getAllocationError(target, current):
	error = 0
	newTarget = target*current.dollarValue
	for i in range(len(Stock.allocationLabels)):
		error += (newTarget.toDollars()[i]-current.toDollars()[i])**2
	return math.sqrt(error)/sum(newTarget.toDollars())

def getStyleError(target, current):
	error = 0
	for i in range(9):
		if target.style != None and current.style != None:
			error += (target.style[i]-current.style[i])**2
	return math.sqrt(error)


stocks = {}
stocks["VTSAX"] = Stock("VTSAX", [.97,.03,0,0,0,0], [.23,.25,.24,.06,.06,.06,.03,.03,.03])
stocks["VTV"]   = Stock("VTV",   [.98,.02,0,0,0,0], [.46,.32,.07,.09,.04,.01,0,0,0])
stocks["VSMAX"] = Stock("VSMAX", [.96,.02,.02,0,0,0], [0,0,0,.11,.13,.18,.19,.20,.18])
stocks["VO"] = Stock("VO",       [.94,.04,.02,0,0,0], [.02,.05,.07,.28,.29,.28,0,0,0])
stocks["VOE"] = Stock("VOE",     [.94,.04,.02,0,0,0], [.03,.09,0,.50,.31,.07,0,0,0])
stocks["VIEIX"] = Stock("VIEIX", [.95,.03,.02,0,0,0], [0,.01,.03,.11,.13,.21,.16,.17,.17])
stocks["VGSLX"] = Stock("VGSLX", [0,0,0,1,0,0], [.03,.09,.24,.09,.22,.12,.07,.11,.03])
stocks["VFFVX"] = Stock("VFFVX", [.52,.32,.06,0,.1,0], [.26,.25,.25,.06,.06,.06,.02,.02,.02])
stocks["VIPIX"] = Stock("VIPIX", [0,0,0,0,0,1], [0]*9)
stocks["VBTLX"] = Stock("VBTLX", [0,0,0,0,1,0], [0]*9)
# stocks["PTTRX"] = Stock("PTTRX", [0,0,0,0,.88,.12])
stocks["VXUS"] = Stock("VXUS",   [0,.84,.16,0,0,0], [0]*9)
stocks["VWO"] = Stock("VWO",     [0,.21,.79,0,0,0], [0]*9)


target = Stock("Target Allocation", [.512, .184, .0640, .04, .16, .04], [.17,.17,.17,.11,.11,.11,.06,.06,.06])
current = Stock("Current Allocation", [.5154, .1852, .0597, .0370, .1602, .0425], [.17,.18,.17,.10,.11,.11,.06,.06,.05])
current.dollarValue = 456816


def runAllInOne():
	print(getError(target, current))
	contribution = Stock("contribution", [0]*6, [0]*9)
	contributionTotal = (2500+1818)*6+11000*.9389
	increment = 100
	contributionStockWeights = {}

	contributed = 0
	while contributed < contributionTotal:
		minError = None
		minStock = None
		for stock in stocks.values():
			error = getError(target, current+contribution+stock*increment)
			if minError == None or error < minError:
				minError = error
				minStock = stock
		contribution += minStock*increment
		contributed += increment
		if not minStock.name in contributionStockWeights:
			contributionStockWeights[minStock.name] = 0
		contributionStockWeights[minStock.name] += increment

	print(contributionStockWeights)
	print(contribution)
	print(current+contribution)

	print(getError(target, current+contribution))


def runBuckets():
	print("AE: %0.2f%%\tSE: %0.2f%%"%(getAllocationError(target, current)*100, getStyleError(target,current)*100))

	contribution = Stock("contribution", [0]*6, [0]*9)
	baseIncrement = 100

	buckets = [
		{
			"name":"rachelRoth",
			"contribution":5500*.9389,
			"stockOptions":["VFFVX"],
			"allocation":{}
		},
		{
			"name":"timRoth",
			"contribution":5500*.9389,
			"stockOptions":["VGSLX", "VBTLX"],
			"allocation":{}
		},
		{
			"name":"401k",
			"contribution":1818*6,
			"stockOptions":["VIEIX", "VBTLX", "VIPIX", "VBTLX", "VTSAX", "VXUS"],
			"allocation":{}
		},
		{
			"name":"HSA",
			"contribution":479*6,
			"stockOptions":["VBTLX"],
			"allocation":{}
		},
		{
			"name":"vanguard",
			"contribution":2500*6,
			"stockOptions":["VTSAX", "VSMAX", "VO", "VWO", "VXUS"],
			"allocation":{}
		}
	]

	# print(getBucketMinError(buckets["vanguard"], target, current, -1))

	runCount = 0
	lastError = 1
	while True:
		increment = baseIncrement		
		runCount += 1

		if runCount % 5 == 0:
			increment = -increment

		newTarget = target*(current+contribution).dollarValue
		for i in range(len(Stock.allocationLabels)):
			print("%s : %0.2f"%(Stock.allocationLabels[i], (newTarget.toDollars()[i] - (current+contribution).toDollars()[i])))

		bucketErrors = sorted([(bucket, getBucketMinError(bucket, target, current+contribution, increment)) for bucket in buckets], key=lambda bucket: bucket[1][0], reverse=False)
		if increment > 0:
			bucketErrors = [bucketError for bucketError in bucketErrors if bucketError[0]["contribution"] > 0]
		else:
			bucketErrors = [bucketError for bucketError in bucketErrors if bucketError[1][1].name in bucketError[0]["allocation"]]
			bucketErrors = [bucketError for bucketError in bucketErrors if not bucketError[0]["name"] in ["rachelRoth", "HSA"]]

		if len(bucketErrors) == 0:
			if increment < 0:
				continue
			print("No more money")
			break

		maxBucketError = bucketErrors[0]
		maxBucket = maxBucketError[0]
		mbStock = maxBucketError[1][1]

		if increment > 0:
			increment = min(maxBucket["contribution"], baseIncrement)

		error = getError(target, current+contribution)
		lastError = error

		print(str(increment) + " -> " + maxBucket["name"] + ":" + mbStock.name)
		print("  %0.2f%% -> %0.2f%%"%(lastError*100, error*100))
		# if error > lastError:
		# 	print("increasing error")
		# 	print(mbStock.name + " -> " + minBucketName)
		# 	for bucketName in buckets:
		# 		print(bucketName)
		# 		bucket = buckets[bucketName]
		# 		print("  " + str(bucket["contribution"]))
		# 		print("  " + str(bucket["allocation"]))
		# 	break

		contribution += mbStock*increment
		maxBucket["contribution"] -= increment
		if not mbStock.name in maxBucket["allocation"]:
			maxBucket["allocation"][mbStock.name] = 0
		maxBucket["allocation"][mbStock.name] += increment
		


		if runCount > 10000:
			print("TOO MANY RUNS")
			break

	for bucket in buckets:
		print(bucket["name"])
		# print(buckets[bucketName]["allocation"])
		total = 0
		for stock in bucket["allocation"].values():
			total += stock
		for stock in bucket["allocation"]:
			perc = float(bucket["allocation"][stock])/total*100			
			print("  %s\t:\t%2.2f%%\t(%d)"%(stock,perc,bucket["allocation"][stock]))
	print("AE: %0.2f%%\tSE: %0.2f%%"%(getAllocationError(target, current+contribution)*100, getStyleError(target,current+contribution)*100))
	print(current+contribution)

runBuckets()