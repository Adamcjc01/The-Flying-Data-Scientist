import datetime
now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))
b = now + datetime.timedelta(0,620)
print (b.strftime("%Y-%m-%d %H:%M:%S"))
