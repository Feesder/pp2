import datetime
from datetime import timedelta

now = datetime.datetime.now()

new_date = now - timedelta(days=5)

print(new_date.date())