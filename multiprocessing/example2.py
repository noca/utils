#!/bin/env python

from multiprocessing import Pool as ThreadPool


def echo(i):
    return i


def main():
    # Make the Pool of workers
    pool = ThreadPool(100)

    # Open the urls in their own threads and return the results
    results = pool.map(echo, xrange(100000))

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()

    print results


if __name__ == '__main__':
    main()
