#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/9/3 下午5:11 
# @Author : liu hao 
# @File : thread_priority_queue.py

"""python的queue模块提供同步的线程安全队列类，包括FIFO(先入先出)队列Queue
  LIFO(后入先出)队列LifoQueue,优先级队列priorityQueue"""
"""useful methods in queue method
1 queue.qsize() return length of queue
2 queue.empty() whether a queue is empty
3 queue.full()  whether a queue is full
4 queue.full return maxsize of queue
5 queue.get([block[,timeout]]]) acquire queue and timeout value
6 queue.get_nowait()  equal to queue.get(False)
7 queue.put(item) write item into queue
8 queue.put_nowait(item) equal to queue.put(item,False)
9 queue.task_done() when a tasked finished,send tasked-finished queuea singnal
10 queue.join() execute another task once current queue is empty """

import queue
import threading
import time

exit_flag=0

class mythread(threading.Thread):
    def __init__(self,thread_id,name,q):
        threading.Thread.__init__(self)
        self.thread_id=thread_id
        self.name=name
        self.q=q
    def run(self):
        print("start thread :"+self.name)
        process_data(self.name,self.q)
        print("exit thread"+self.name)

def process_data(thread_name,q):
    while not exit_flag:
        queue_lock.acquire()
        if not active_queue.empty():
            data=q.get()
            queue_lock.release()
            print("%s processing %s" %(thread_name,data))
        else:
            queue_lock.release()
        time.sleep(1)

thread_list=["thread1","thread2","thread3"]
name_list=["one","two","three","four","five"]
queue_lock=threading.Lock()
active_queue=queue.Queue(10)
threads=[]
thread_id=1
for thread_name in thread_list:
    thread=mythread(thread_id,thread_name,active_queue)
    thread.start()
    threads.append(thread)
    thread_id+=1

queue_lock.acquire()
for name in name_list:
    active_queue.put(name)
queue_lock.release()

while not active_queue.empty():
    pass

exit_flag=1

for t in threads:
    t.join()
print("all thhread exited")
