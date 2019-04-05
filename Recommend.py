import numpy as np
import math
import time

start_time = time.time()

def angle_calc(vec1, vec2):
	array_vec1 = np.array(vec1)
	array_vec2 = np.array(vec2)
	norm_1 = np.linalg.norm(array_vec1)
	norm_2 = np.linalg.norm(array_vec2)
	cos_theta = (np.dot(array_vec1, array_vec2) / (norm_1 * norm_2))
	if cos_theta < 1.000001 and cos_theta > 1:
		cos_theta = 1
	theta = math.degrees(math.acos(cos_theta))
	return theta

def empty_list(number):
	list = [0] * number
	return list

def sortKey(elem):
        return elem[0]
history_file = ((open("history.txt", "r")).readlines())

info = history_file[0].split()
noOfCus = int(info[0])
noOfItem = int(info[1])
noOfTrans = int(info[2])
positive_entries = 0
history_table = {}

for i in range(1, noOfItem + 1):
	history_table[i] = empty_list(noOfCus)

for i in range(1, noOfTrans + 1):
	cusId = int((history_file[i].split())[0])
	itemId = int((history_file[i].split())[1])
	history_table[itemId][cusId-1] = 1
	
count_table = [history_table[i] for i in history_table]
positive_entries = (np.count_nonzero(count_table))

angle_item = {}
for i in range(1, noOfItem + 1):
	angle_item[i] = empty_list(noOfItem)

all_angles = []
for x in range (1, noOfItem + 1):
	for i in range (1,noOfItem + 1):
		angle_between = angle_calc(history_table[x], history_table[i])
		angle_item[x][i-1] = angle_between
		if x < i:
			all_angles.append(angle_between)

print ("Positive entries:", positive_entries)
print ("Average angle:", round(sum(all_angles)/len(all_angles), 2))


cart_file = ((open("queries.txt", "r")).readlines())
for i in range(len(cart_file)):
        recommend = []
        angles = {}
        sorted_angles =[]
        shopping_cart = cart_file[i].split()
        print("Shopping cart:", *shopping_cart, sep=' ')
        for item in shopping_cart:
                angles[item] = (angle_item[int(item)])[:]
                for ids in shopping_cart:
                        angles[item][int(ids) - 1] = 0
                angle_array = np.array(angles[item])
                min_angle = np.min(angle_array[np.nonzero(angle_array)])
                sorted_angles.append([min_angle, item])
                new_angles = angles[item][:]
                if min_angle != 90:
                        print("Item:", item + "; match:", (str(new_angles.index(min_angle)+1)) + "; angle:", round(min_angle, 2))
                else:
                        print("Item:", item , "no match")
        sorted_angles.sort(key=sortKey)
        for angle in sorted_angles:
                if angle[0] != 90:
                        recommend.append(angles[angle[1]].index(angle[0])+1)
        recommend = list(dict.fromkeys(recommend))
        print("Recommend:", *recommend, sep=' ')


