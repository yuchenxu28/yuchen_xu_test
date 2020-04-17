# function returning TRUE 
# if (x1, x2) overlaps with (x3, x4)
def questionA(x1, x2, x3, x4):
	if (x2 < x3 or x4 < x1):
		return False
	elif (x1 <= x3 and x3 <= x2):
		return True
	elif (x3 <= x1 and x1 <= x4):
		return True

# here are the test cases
print(questionA(1,2,3,4))
print(questionA(3,4,1,2))
print(questionA(1,3,2,4))
print(questionA(2,4,1,3))
print(questionA(1,4,2,3))
print(questionA(2,3,1,4))