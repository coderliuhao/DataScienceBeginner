#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/9/3 下午6:17 
# @Author : liu hao 
# @File : date_time.py

import time
import calendar

#acquire current time ticks
ticks=time.time()
print("cur time tick:",ticks)
#time before 1970 year  or after 2038 year cannot calculate ticks

#tupletime
struct_time=("year","month","day","hour","minuate","second",
            "day_of_a_week","day_of_a_year","Daylight_saving_time")
"""
year            including four digits
month           range(1,13)
day             range(1,32)
hour            range(0,24)
minuate         range(0,60)
second          range(0,62)
day_of_a_week   range(0,7) 0 is equal monday
day_of_a_year   range(1,367)
"Daylight_saving_time  -1,0,1 whether dst

"""

"""we can acquire value which we want by visiting its'index and using
  correct attributes of struct_time to visit accordingly value directly
"""
"""
attributes of struct_time     struct_time included

tm_year                             year
tm_mon                              month
tm_mday                             day
tm_hour                             hour
tm_min                              minuate
tm_sec                              second
tm_wday                             day_of_a_week
tm_yday                             day_of_a_year
tm_isdst                            DST

"""

#use localtime() to convert time ticks(float) to struct_time

localtime=time.localtime(time.time())
print("local time :",localtime)

# use asctime get format time
localtime_format=time.asctime(time.localtime(time.time()))
print("local time :",localtime_format)

#format date  Year-month-day Hour:minuate:second
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))

#format data week_name month_name day Hour:minuate:second YEAR
print(time.strftime("%a %b %d %H:%M:%S %Y",time.localtime(time.time())))


#format date string convert to ticks
a="Thu Sep  3 19:00:39 2020"
print(time.strptime(a,"%a %b  %d %H:%M:%S %Y"))

print(time.mktime(time.strptime(a,"%a %b  %d %H:%M:%S %Y")))


#get some years and some month claendar
cal=calendar.month(2020,10)
print(cal)

"""
some bultin functions in time module
time.altzone() 
time.asctime() return a readable time
time.clock()   return time of current CPU,to measure run time of program
time.ctime()   equal to time.asctime()
time.localtime()  recieve ticks and return struct_time of local time
time.mktime()  recieve a struct_time return time ticks
time.sleep()   recieve seconds to delay call thread to run
time.strftime() recieve format and struct_time ,return a readable string by format
time.strptime() recieve a time string and its'format return a struct_time
time.time()     return current time ticks
time.process_time()  return sum of time for current cpu to execute current process,without sleep time
"""

"""
atributes of time module
time.timezone  seconds between local time and Greenwich
time.tzname    local time with DST and local time without DST 
"""

