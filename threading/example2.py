#!/bin/env python

import threading
import Queue


def echo(i):
    return i


class myThread(threading.Thread):

    def __init__(self, in_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue

    def run(self):
        while True:
            data = self.in_queue.get()
            mylist.append(echo(data))
            self.in_queue.task_done()


def main():
    max_thread_num = 100
    list = [i for i in xrange(1000000)]

    for i in xrange(max_thread_num):
        t = myThread(in_queue)
        t.setDaemon(True)
        t.start()

    for l in list:
        in_queue.put(l)

    in_queue.join()

    # print mylist
    print len(mylist)

if __name__ == "__main__":
    mylist = []

    in_queue = Queue.Queue()

    main()
