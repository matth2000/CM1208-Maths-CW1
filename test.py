import numpy as np
import heapq as hq
import math
import time
start_time = time.time()
#--Queries--
def Queries(file, dictVec, positiveEnteries, averageAngle):
	print("Positive entries: %d" %positiveEnteries)
	print("Average angle: %s" %averageAngle)

	cartList = list()
	queries = open(file)
	dataTemp = queries.readlines()
	data = [word.replace("\n","") for word in dataTemp]

	for i in data:
		shoppingCart = i
		recList = list()
		print("Shopping cart: %s" %shoppingCart)
		shoppingCart = i.split()

		for items in shoppingCart:
			items = int(items)
			cartTemp = shoppingCart
			cartList = list(map(int, cartTemp))

			if (items > 0):
				k = 1
				if (dictVec[items][hq.nsmallest(k, dictVec[items].keys())[-1]] not in cartList):
					minAngle = hq.nsmallest(k, dictVec[items].keys())[-1]
					recommendItem = dictVec[items][minAngle]

					if (minAngle < 90):
						print("Item: %s"%items+"; match: %d"%recommendItem+"; angle: %.2f"%minAngle)
						recList.append(recommendItem)

					else:
						print("Item: %s"%items+" no match")

				else:
					while dictVec[items][hq.nsmallest(k, dictVec[items].keys())[-1]] in cartList and k < len(dictVec):
						k += 1
						minAngle = hq.nsmallest(k, dictVec[items].keys())[-1]
						recItem = dictVec[items][minAngle]

					if (minAngle < 90):
						print("Item: %s"%items+"; match: %d"%recItem+"; angle: %.2f"%minAngle)
						recList.append(recItem)

					else:
						print("Item: %s"%items+" no match")

		recTemp = sorted(recList, key=lambda x:minAngle)
		recommended = list(set(recTemp))

		print("Recommend:"," ".join(map(str, recommended)))


#--History--

def History(file):
	dictVec = dict()
	averageList = list()
	dictVec2 = dict()

	historyData = open(file)
	cusNum, itemNum, transNum = historyData.readline().split(" ")
	cusNum = int(cusNum)
	itemNum = int(itemNum)

	for i in range(1, itemNum+1):
		dictVec2[i]=[0 for i in range(1, cusNum+1)]

	for line in historyData:
		custID, itemID = line.split()
		custID = int(custID)
		itemID = int(itemID)
		dictVec2[itemID][custID - 1] = 1

	historyData.close()

	vecTemp = [dictVec2[k] for k in dictVec2]
	positiveEnteries = int(np.count_nonzero(vecTemp))


	def displayAvg(averageAngle):
		Queries("queries.txt", dictVec, positiveEnteries, averageAngle)
		return


	def calcAverage(averageList):
		floatSum = sum(averageList)
		div = len(averageList)
		calAverageAngle = (floatSum / div)
		avgAngle = round(calAverageAngle, 2)
		displayAvg(avgAngle)
		return


	def calAngles(x,y):
		normX = np.linalg.norm(x)
		normY = np.linalg.norm(y)
		cosTheta = (np.dot(x, y) / (normX * normY))
		theta = math.degrees(math.acos(cosTheta))
		thetaR = round(theta,2)
		return thetaR

	for i in dictVec2:
		VecApp1 = dictVec2[i]
		dictVec[i] = dict()
		for z in dictVec2:
			VecApp2 = dictVec2[z]
			if (i != z):
				dictVec[i][calAngles(VecApp1, VecApp2)] = z

	for k in range(1, len(dictVec2)):
		for t in range(k, len(dictVec2)):
			normX2 = np.linalg.norm(dictVec2 [k])
			normY2 = np.linalg.norm(dictVec2 [t + 1])
			cosTheta = np.dot(dictVec2 [k], dictVec2 [t + 1]) / (normX2 * normY2)
			theta = math.degrees(math.acos(cosTheta))
			thetaR2 = round(theta, 2)
			averageList.append(thetaR2)
	calcAverage(averageList)
	return

History("history.txt")
print(("--- %s seconds ---" % (time.time() - start_time)))
