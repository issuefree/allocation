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
		stockDollars = self.dollarValue*(sum(self.allocation[0:5]))
		return [x*stockDollars for x in self.style]

	def __add__(self, otherStock):
		myDollars = self.toDollars()
		otherDollars = otherStock.toDollars()

		totalDollars = sum(myDollars) + sum(otherDollars)

		newAllocation = []
		newStyle = []
		for i in range(len(Stock.allocationLabels)):
			newAllocation += [(myDollars[i] + otherDollars[i])/float(totalDollars)]

		myStyleDollars = self.styleToDollars()
		otherStyleDollars = otherStock.styleToDollars()
		styleDollars = sum(myStyleDollars) + sum(otherStyleDollars)
		if styleDollars > 0:
			for i in range(9):	
				newStyle += [(myStyleDollars[i] + otherStyleDollars[i])/styleDollars]
		else:
			newStyle = [0]*9
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

def getError(allocationA, allocationB):
	allocationError = getAllocationError(allocationA, allocationB)
	styleError = getStyleError(allocationA, allocationB)
	return allocationError + styleError/4
		
def getAllocationError(allocationA, allocationB):
	error = 0
	for i in range(len(Stock.allocationLabels)):
		error += (allocationA.allocation[i]-allocationB.allocation[i])**2
	return math.sqrt(error)

def getStyleError(allocationA, allocationB):
	if allocationA.style == None or current.style == None:
		return 0

	style = [allocationA.style[i] - allocationB.style[i] for i in range(len(allocationA.style))]

	error = 0
	# large cap
	error += sum(style[0:3])**2
	# medium cap
	error += sum(style[3:6])**2
	# small cap
	error += sum(style[6:9])**2

	# value
	error += (sum(style[0::3])**2)/2
	# blend
	error += (sum(style[1::3])**2)/4
	# growth
	error += (sum(style[2::3])**2)/2

	return math.sqrt(error)


stocks = {}
stocks["VTSAX"] = Stock("VTSAX", [.97,.03,0,0,0,0], [.25,.25,.23,.06,.06,.06,.03,.03,.03])
stocks["VTV"]   = Stock("VTV",   [.98,.02,0,0,0,0], [.51,.25,.09,.09,.05,.01,0,0,0])
stocks["VSMAX"] = Stock("VSMAX", [.96,.02,.02,0,0,0], [0,0,0,.09,.13,.20,.20,.20,.19])
stocks["VO"] = Stock("VO",       [.94,.04,.02,0,0,0], [.0,.05,.09,.28,.30,.27,.01,0,0])
stocks["VOE"] = Stock("VOE",     [.94,.04,.02,0,0,0], [.01,.07,0,.49,.34,.08,.01,0,0])
stocks["VIEIX"] = Stock("VIEIX", [.95,.03,.02,0,0,0], [.01,.01,.02,.11,.13,.21,.17,.17,.17])
stocks["VGSLX"] = Stock("VGSLX", [0,0,0,1,0,0], [.0,.23,.07,.12,.24,.12,.08,.10,.03])
stocks["VFFVX"] = Stock("VFFVX", [.53,.31,.06,0,.10,0], [.26,.25,.25,.06,.06,.06,.02,.02,.02])
stocks["VIPIX"] = Stock("VIPIX", [0,0,0,0,0,1], [0]*9)
stocks["VBTLX"] = Stock("VBTLX", [0,0,0,0,1,0], [0]*9)
# stocks["PTTRX"] = Stock("PTTRX", [0,0,0,0,.88,.12])
stocks["VXUS"] = Stock("VXUS",   [0,.84,.16,0,0,0], [0]*9)
stocks["VTSNX"] = Stock("VTSNX",   [0,.84,.16,0,0,0], [0]*9)
stocks["VWO"] = Stock("VWO",     [0,.21,.79,0,0,0], [0]*9)


target = Stock("Target Allocation", [.512, .184, .0640, .04, .16, .04], [.1667,.1667,.1667,.1111,.1111,.1111,.0556,.0556,.0556])
current = Stock("Current Allocation", [.5210, .1870, .0614, .0375, .1523, .0409], [.1723,.1704,.1597,.0990,.1084,.1169,.0594,.0579,.0560])
current.dollarValue = 463316

print(current)

def runBuckets():
	print("AE: %0.2f%%\tSE: %0.2f%%"%(getAllocationError(target, current)*100, getStyleError(target,current)*100))

	contribution = Stock("contribution", [0]*6, [0]*9)
	baseIncrement = 25.0

	buckets = [
		{
			"name":"rachelRoth",
			"contribution":5500*.9861,
			"stockOptions":["VFFVX"],
			"allocation":{}
		},
		{
			"name":"timRoth",
			"contribution":5500*.9861,
			"stockOptions":["VGSLX", "VBTLX"],
			"allocation":{}
		},
		{
			"name":"401k",
			"contribution":1818*6,
			"stockOptions":["VIEIX", "VBTLX", "VIPIX", "VBTLX", "VTSAX", "VTSNX"],
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
			"contribution":3000*6,
			"stockOptions":["VTSAX", "VSMAX", "VO", "VWO", "VXUS"],
			"allocation":{}
		}
	]

	# print(getBucketMinError(buckets["vanguard"], target, current, -1))

	lastDollarValue = 0

	runCount = 0
	lastError = 1
	while True:
		increment = baseIncrement		
		runCount += 1

		# newTarget = target*(current+contribution).dollarValue
		# for i in range(len(Stock.allocationLabels)):
		# 	print("%s : %0.2f"%(Stock.allocationLabels[i], (newTarget.toDollars()[i] - (current+contribution).toDollars()[i])))
	

		bucketErrors = sorted([(bucket, getBucketMinError(bucket, target, current+contribution, increment)) for bucket in buckets], key=lambda bucket: bucket[1][0], reverse=False)
		bucketErrors = [bucketError for bucketError in bucketErrors if bucketError[0]["contribution"] > 0]

		if len(bucketErrors) == 0:
			print("No more money")
			break

		maxBucketError = bucketErrors[0]
		maxBucket = maxBucketError[0]
		mbStock = maxBucketError[1][1]

		increment = min(maxBucket["contribution"], baseIncrement)

		error = getError(target, current+contribution)
		lastError = error

		# print(str(increment) + " -> " + maxBucket["name"] + ":" + mbStock.name)
		# print("  %0.2f%% -> %0.2f%%"%(lastError*100, error*100))

		contribution += mbStock*increment
		maxBucket["contribution"] -= increment

		if not mbStock.name in maxBucket["allocation"]:
			maxBucket["allocation"][mbStock.name] = 0
		maxBucket["allocation"][mbStock.name] += increment

		if runCount > 10000:
			print("TOO MANY RUNS")
			break

	tuneBuckets = True
	tuneUps = 0
	while tuneBuckets and tuneUps < 1000:
		tuneUps += 1
		# print(tuneUps)
		tuneBuckets = False
		for bucket in buckets:
			if len(bucket["stockOptions"]) < 2:
				continue
			error = getError(target, current+contribution)

			bestSell = sorted([(stockName, error-getError(target, current+contribution+stocks[stockName]*-baseIncrement)) for stockName in bucket["allocation"]], key=lambda item: item[1], reverse=True)[0]

			increment = min(baseIncrement, bucket["allocation"][bestSell[0]])

			if increment <= 0:
				continue

			bestBuy = sorted([(stockName, error-getError(target, current+contribution+stocks[stockName]*increment)) for stockName in bucket["stockOptions"]], key=lambda item: item[1], reverse=True)[0]

			if bestSell[1]+bestBuy[1] > 1e-05:
				# print("%s -> %s  (%f)"%(bestSell[0], bestBuy[0], bestSell[1]+bestBuy[1]))
				contribution += stocks[bestSell[0]]*-increment
				bucket["allocation"][bestSell[0]] -= increment
				contribution += stocks[bestBuy[0]]*+increment
				if not bestBuy[0] in bucket["allocation"]:
					bucket["allocation"][bestBuy[0]] = 0
				bucket["allocation"][bestBuy[0]] += increment
				tuneBuckets = True
	print("%d in tuneups"%(tuneUps*baseIncrement))

		# for stockName in bucket["stockOptions"]:
		# 	stock = stocks[stockName]

		# 	newBuyError = getError(target, current+stock*baseIncrement)
		# 	print(stockName + " " + str(error-newBuyError))


	for bucket in buckets:
		print(bucket["name"])
		total = 0
		for stock in bucket["allocation"].values():
			total += stock
		for stock in bucket["allocation"]:
			perc = float(bucket["allocation"][stock])/total*100			
			print("  %s\t:\t%2.2f%%\t(%d)"%(stock,perc,bucket["allocation"][stock]))
	print("AE: %0.2f%%\tSE: %0.2f%%"%(getAllocationError(target, current+contribution)*100, getStyleError(target,current+contribution)*100))
	# print(contribution)
	print(current+contribution)

runBuckets()