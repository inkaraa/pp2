from datetime import datetime,timedelta
current_date=datetime.now()
substract=current_date-timedelta(days=5)
print(substract)