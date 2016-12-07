
from datetime import datetime

timeNow = datetime.utcnow()

print datetime.utcnow().strftime('%d_%H_%M_%S_%f')

newFile = open ('timestamp.txt','a')

newFile.write ('\nHello world again')

timeAfter = datetime.utcnow()


print timeNow
print timeAfter

print timeAfter - timeNow