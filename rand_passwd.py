#!/usr/bin/env python


import random


def rand_passwd():
    '''
    @summary: generate a random passwd with 30 chars.
    @result: a passwd str with at least one number, one special char, and one letter
    '''
    total_len = 30
    base_str1 = ['!', '@', '#', '=', '-', '_', '+']
    base_str2 = [str(i) for i in range(0, 10)]
    base_str3 = [chr(i)
                 for i in range(ord('A'), ord('Z') + 1) + range(ord('a'), ord('z') + 1)]
    random.seed()
    total_sample = []
    total_sample += random.sample(base_str1, random.randint(1, len(base_str1)))
    total_sample += random.sample(base_str2, random.randint(1, len(base_str2)))
    total_sample += random.sample(base_str3, total_len - len(total_sample))
    random.shuffle(total_sample)
    passwd = ''.join(total_sample)
    return passwd


if __name__ == '__main__':
    print rand_passwd()
