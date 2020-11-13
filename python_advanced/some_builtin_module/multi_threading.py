#python3常用的线程模块：_thread,threading

"""调用_thread模块中的start_new_thread(function,args[,kwargs])
参数：function:线程函数
      args: 传给线程函数的参数tuple类型
      kwargs:可选参数"""

import _thread
import time

# def print_time(thread_name,delay):
#     cnt=0
#     while cnt<0:
#         time.sleep(delay)
#         cnt+=1
#         print("%s: %s"%(thread_name,time.ctime(time.time())))


# """创建两个线程"""
# try:
#     _thread.start_new_thread(print_time("thread-1",1))
#     #_thread.start_new_thread(print_time("thread-2",4))
# except:
#     print("Error : 无法启动线程")

import threading
"""threading模块包含_thread的所有方法外还提供以下方法：
 1、threading.currentThread()返回当前线程变量
 2、threading.enumerate()返回一个包含正在运行(线程启动后，结束前。不包括启动前和终止后的线程)的线程 的list.
 3、threading.activeCount()返回正在运行的线程数量，与len(threading.enumerate())有相同结果"""

"""除以上方法，threading模块中提供了Thread类来处理线程，Thread类中提供如下方法：
  1、run() 用以表示线程活动的方法
  2、start() 启动线程活动
  3、join([time]) 等待至线程中止。指阻塞调用线程直至线程的join()方法被调用中止-正常退出或者抛出未处理的异常，或者是可选的超时发生
  4、isALive():判断线程是否是活动的
  5、getName() 返回线程名
  6、setName() 设置线程名"""


exit_flag=0
class myThread(threading.Thread):
    def __init__(self,thread_id,name,counter):
        threading.Thread.__init__(self)
        self.thread_id=thread_id
        self.name=name
        self.counter=counter
    def run(self):
        print("开始线程:"+self.name)
        print_time2(self.name,self.counter,5)
        print("退出线程 :"+self.name)

def print_time2(thread_name,delay,counter):
    while counter:
        time.sleep(delay)
        print("%s:%s"%(thread_name,time.ctime(time.time())))
        counter-=1

if __name__ == '__main__':
    #创建新线程
    thread1=myThread(1,"thread-1",1)
    thread2=myThread(2,"thread-2",2)

    #开启新线程
    thread1.start()
    thread2.start()


    thread1.join()
    thread2.join()
    print("退出主线程")




