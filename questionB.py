# function returning an integer
# 1 if version A > version B
# -1 if version A < version B
# 0 if version A = version B
def questionB(versionA, versionB):
	Alist = versionA.split(".")
	Blist = versionB.split(".")

	minlen = min(len(Alist), len(Blist))
	for i in range(minlen):
		if Alist[i] == Blist[i]:
			pass
		elif Alist[i] > Blist[i]:
			return 1
		elif Alist[i] < Blist[i]:
			return -1

	if (len(Alist) > len(Blist)):
		return 1
	elif (len(Alist) < len(Blist)):
		return -1

	return 0

# here are the test cases
print(questionB("1.1", "1.1"))
print(questionB("1.1", "1.2"))
print(questionB("1.1.1", "1.1"))
print(questionB("2.0", "1.1.1"))
print(questionB("2", "1.2"))