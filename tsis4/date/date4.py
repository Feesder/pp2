import datetime

now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)

print((now - yesterday).total_seconds())