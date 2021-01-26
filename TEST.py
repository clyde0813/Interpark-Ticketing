import datetime

full_time = (datetime.datetime.combine(datetime.date(1,1,1), datetime.datetime.now().time()) + datetime.timedelta(seconds=10)).time()

print(str(full_time)[:8])
