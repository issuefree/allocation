import math

class Stock:
	allocationLabels = [
		"Domestic",
		"Foreign ",
		"Emerging",
		"REIT    ",
		"Bonds   ",
		"TIPS    "
	]

	def __init__(self, name, allocation):
		self.dollarValue = 0
		self.name = name
		self.allocation = allocation

		# if abs(sum(self.allocation) - 1) > .01:
		# 	print("Possible incomplete stock " + self.name + " " + str(self.allocation))

	def __str__(self):
		out = self.name + ":"
		if self.dollarValue > 0:
			out += " ("+str(self.dollarValue) + ")\n"
		else:
			out += "\n"

		for i in range(len(Stock.allocationLabels)):			
			out += "  " + Stock.allocationLabels[i]  + "\t" + str(self.allocation[i]) + "\n"
		return out

	def toDollars(self):
		return [x*self.dollarValue for x in self.allocation]

	def __add__(self, otherStock):
		myDollars = self.toDollars()
		otherDollars = otherStock.toDollars()
		totalDollars = sum(myDollars) + sum(otherDollars)
		# dollarAllocation = []
		newAllocation = []
		for i in range(len(Stock.allocationLabels)):
			newAllocation += [(myDollars[i] + otherDollars[i])/totalDollars]
		newStock = Stock(self.name, newAllocation)
		newStock.dollarValue = totalDollars
		return newStock

	def __mul__(self, dollarValue):
		newStock = Stock(self.name, self.allocation)		
		newStock.dollarValue = dollarValue
		return newStock
		
def getError(target, current):
	error = 0
	for i in range(len(Stock.allocationLabels)):
		error += (target.allocation[i]-current.allocation[i])**2
	return math.sqrt(error)


stocks = {}
stocks["VTSAX"] = Stock("VTSAX", [.97,.03,0,0,0,0])
stocks["VTV"]   = Stock("VTV", [.98,.02,0,0,0,0])
stocks["VSMAX"] = Stock("VSMAX", [.96,.02,.02,0,0,0])
stocks["VO"] = Stock("VO", [.94,.04,.02,0,0,0])
stocks["VOE"] = Stock("VOE", [.94,.04,.02,0,0,0])
stocks["VIEIX"] = Stock("VIEIX", [.93,.03,.02,0,0,0])
stocks["VGSLX"] = Stock("VGSLX", [0,0,0,1,0,0])
stocks["VFFVX"] = Stock("VFFVX", [.52,.32,.06,0,.1,0])
stocks["VIPIX"] = Stock("VIPIX", [0,0,0,0,0,1])
stocks["VBTLX"] = Stock("VBTLX", [0,0,0,0,1,0])
# stocks["PTTRX"] = Stock("PTTRX", [0,0,0,0,.88,.12])
stocks["VXUS"] = Stock("VXUS", [0,.84,.16,0,0,0])
stocks["VWO"] = Stock("VWO", [0,.21,.79,0,0,0])


target = Stock("Target Allocation", [.512, .184, .0640, .04, .16, .04])
current = Stock("Current Allocation", [.5154, .1852, .0597, .0370, .1602, .0425])
current.dollarValue = 456816


def runAllInOne():
	print(getError(target, current))
	contribution = Stock("contribution", [0,0,0,0,0,0])
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
	print(getError(target, current))

	contribution = Stock("contribution", [0,0,0,0,0,0])
	baseIncrement = 100

	buckets = {}
	buckets["rachelRoth"] = {
		"contribution":5500*.9389,
		"stockOptions":["VFFVX"],
		"allocation":{}
	}
	buckets["timRoth"] = {
		"contribution":5500*.9389,
		"stockOptions":["VGSLX", "VBTLX"],
		"allocation":{}
	}
	buckets["401k"] = {
		"contribution":1818*6,
		"stockOptions":["VIEIX", "VBTLX", "VIPIX", "VBTLX", "VTSAX"],
		"allocation":{}
	}
	buckets["HSA"] = {
		"contribution":479*6,
		"stockOptions":["VBTLX"],
		"allocation":{}
	}
	buckets["vanguard"] = {
		"contribution":2500*6,
		"stockOptions":["VTSAX", "VSMAX", "VO", "VWO", "VXUS"],
		"allocation":{}
	}

	runCount = 0
	lastError = 1
	while True:
		increment = baseIncrement
		runCount += 1
		minError = None
		minStock = None
		maxBucket = None
		maxBucketName = None
		canContribute = False

		for bucketName in buckets:
			bucket = buckets[bucketName]
			if bucket["contribution"] > 0:
				increment = min(increment, bucket["contribution"])
				canContribute = True
				for stockName in bucket["stockOptions"]:
					stock = stocks[stockName]
					error = getError(target, current+contribution+stock*increment)
					if minError == None or error < minError:
						minError = error
						minStock = stock
						minBucket = bucket
						minBucketName = bucketName
		if not canContribute:
			print("No more money")
			break
		contribution += minStock*increment
		minBucket["contribution"] -= increment
		if not minStock.name in minBucket["allocation"]:
			minBucket["allocation"][minStock.name] = 0
		minBucket["allocation"][minStock.name] += increment
		
		# print(lastError)
		# error = getError(target, current+contribution)
		# if error > lastError:
		# 	print("increasing error")
		# 	print(minStock.name + " -> " + minBucketName)
		# 	for bucketName in buckets:
		# 		print(bucketName)
		# 		bucket = buckets[bucketName]
		# 		print("  " + str(bucket["contribution"]))
		# 		print("  " + str(bucket["allocation"]))
		# 	break
		# lastError = error


		if runCount > 10000:
			print("TOO MANY RUNS")
			break

	for bucketName in buckets:
		print(buckets[bucketName]["allocation"])
	print(getError(target, current+contribution))
	print(current+contribution)


runBuckets()