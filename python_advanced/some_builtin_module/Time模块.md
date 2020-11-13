### Time模块

```
struct_time=("year","month","day","hour","minuate","second",
            "day_of_a_week","day_of_a_year","Daylight_saving_time")
```

year                                  including four digits
month                                 range(1,13)
day                                       range(1,32)
hour                                     range(0,24)
minuate                               range(0,60)
second                                 range(0,62)
day_of_a_week                   range(0,7) 0 is equal monday
day_of_a_year                     range(1,367)
"Daylight_saving_time        -1,0,1 whether dst

![timeformat](/home/liuhao/Pictures/timeformat.png)



attributes of struct_time     struct_time included

tm_year                                            year
tm_mon                                         month
tm_mday                                         day
tm_hour                                          hour
tm_min                                          minuate
tm_sec                                           second
tm_wday                                      day_of_a_week
tm_yday                                       day_of_a_year
tm_isdst                                             DST

some bultin functions in time module
time.altzone() 
time.asctime()  return a readable time
time.clock()       return time of current CPU,to measure run time of program
time.ctime()      equal to time.asctime()
time.localtime()     recieve ticks and return struct_time of local time
time.mktime()        recieve a struct_time return time ticks
time.sleep()            recieve seconds to delay call thread to run
time.strftime()       recieve format and struct_time ,return a readable string by format
time.strptime()      recieve a time string and its'format return a struct_time
time.time()             return current time ticks
time.process_time()  return sum of time for current cpu to execute current process,without sleep   time



![calendar](/home/liuhao/Pictures/calendar.png)