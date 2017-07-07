#!/usr/bin/env python
# -*- coding: utf-8 -*-
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a+b
        n = n + 1

from multiprocessing import Process
import os
import time, threading

def run_proc(name):
    print 'Run child process %s (%s)...' %(name, os.getpid())

def loop():
    print 'thread %s is running...' % threading.current_thread().name
    n = 0
    while n < 5:
        n = n + 1
        print 'thread %s >>> %s' % (threading.current_thread().name, n)
        time.sleep(1)
    print 'thread %s ended.' % threading.current_thread().name
    
if __name__ == '__main__':
    print 'thread %s is running...' % threading.current_thread().name
    t = threading.Thread(target = loop, name = 'LoopThread')
    t.start()
    t.join()
    print 'thread %s ended.' % threading.current_thread().name