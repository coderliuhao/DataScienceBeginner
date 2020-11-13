import threading
import time

class mythread(threading.Thread):
    def __init__(self,thread_id,name,delay):
        threading.Thread.__init__(self)
        self.thread_id=thread_id
        self.name=name
        self.delay=delay
    def run(self):
        print("start thread"+self.name)
        #获取锁，线程同步    thread1完成后释放锁，开启thread2
        threadLock.acquire()
        print_time(self.name,self.delay,3)
        #释放锁，开启下一线程
        threadLock.release()

def print_time(thread_name,delay,counter):
    while counter:
        time.sleep(delay)
        print("%s:%s"%(thread_name,time.ctime(time.time())))
        counter-=1

threadLock=threading.Lock()
threads=[]

thread1=mythread(1,"thread1",1)
thread2=mythread(2,"thread2",2)

threads.append(thread1)
threads.append(thread2)

thread1.start()
thread2.start()

for t in threads:  #thread1.join(),thread2.join()
    t.join()
print("main thread exited")



