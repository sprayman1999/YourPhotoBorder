from datetime import datetime
import time
def percent2float(percent):
    if isinstance(percent,str):
        if percent.endswith("%"):
            return float(percent[:-1]) / 100.0
        elif percent.isdigit():
            return float(percent) / 1.0
    elif isinstance(percent,int):
        return float(percent) / 1.0
    
def timestamp2str(timestamp,time_format = "%Y-%m-%d %H:%M:%S") -> str:
    dt = datetime.fromtimestamp(timestamp)
    s = dt.strftime(time_format)
    return s 

def str2timestamp(time_str,time_format = "%Y-%m-%d %H:%M:%S") -> str:
    timeArray = time.strptime(time_str, time_format)
    return int(time.mktime(timeArray)) 
