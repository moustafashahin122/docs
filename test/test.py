import datetime
from dateutil.relativedelta import relativedelta, SA

# today = datetime.today()
# Calculate the number of days to subtract to get to the last Saturday 5
# days_to_subtract = 
last_saturday = (datetime.datetime.today() + relativedelta( days=-7,weekday=5)).strftime('%Y-%m-%d 00:00:00')
x=relativedelta( days=-7,weekday=5)
# [('create_date', '&gt;=',(datetime.datetime.today() - datetime.timedelta(days=(datetime.datetime.today().weekday() +1 ) % 6)).strftime('%Y-%m-%d 00:00:00'))]


print("Last Saturday was:", last_saturday)