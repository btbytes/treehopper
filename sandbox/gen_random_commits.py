from random import randint
from datetime import datetime, timedelta
base = datetime.today()
dateList = [ base - timedelta(days=x) for x in range(0,465) ]

print "Date,Commits"

for d in dateList:
	if d.weekday in (5,6):
		MIN = -3
		MAX = 0
	else:
		MIN = 0
		MAX = 10
	print "%s,%s" % (d.strftime("%Y-%m-%d"), randint(MIN, MAX))

