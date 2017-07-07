#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading
import time

Thread_id = 1
Thread_num = 3
class myThread (threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.Thread_id = Thread_id
        Thread_id = Thread_id + 1
    def run(self):
        while True:
            task = self.q.get(block = True, timeout = 1) #不设置阻塞的话会一直去尝试获取资源
        except Queue.Empty:
            print 'Thread' +  self.Thread_id + 'end'
            break
        print "Starting " + self.Thread_id
        print task
        self.q.task_down()
        

q = Queue.Queue(10)
# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"
