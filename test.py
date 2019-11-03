from time import strftime, localtime

real_time = strftime("%H:%M", localtime())
hour = int(real_time[:2])*60 + int(real_time[4:6])
print(hour)