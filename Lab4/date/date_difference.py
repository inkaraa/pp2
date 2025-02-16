from datetime import datetime
date1=datetime(2025,1,12,12,5,6)
date2=datetime(2025,2,12,14,5,7)
difference=date2-date1
print(difference.total_seconds())
