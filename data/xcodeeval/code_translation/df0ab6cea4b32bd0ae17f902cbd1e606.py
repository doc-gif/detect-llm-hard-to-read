from datetime import datetime
s = datetime.strptime(input(), '%H:%M')
t = datetime.strptime(input(), '%H:%M')

sec = (s - t).seconds
hours, rem = divmod(sec, 60**2)
minutes, sec = divmod(rem, 60)
print(str(hours).zfill(2) + ':' + str(minutes).zfill(2))
