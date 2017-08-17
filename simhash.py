#!/bin/env python
# coding=utf-8
import hashlib

def ELFHash(key):
    hash = 0
    x = 0
    for i in range(len(key)):
        hash = (hash << 4) + ord(key[i])
        x = hash & 0xF0000000
        if x != 0:
            hash ^= (x >> 24)
        hash &= ~x
    return hash

	
SIMHN = 32
def sim_hash(str):
    sim_value = [0]*128
    for char in str:
        hash_node(char, sim_value)
    return sim_value

	
def hash_node(name, simh):
    hash = hashlib.md5(name).hexdigest()
    for i in range(32):
        val = int(hash[i], 16)
        for n in range(4):
            index = i * 4 + n
            delta = val & 1
            simh[index] += (1 if delta > 0 else -1)
            val >>= 1
    return simh


def calc_string_simh_bin(str):
    stat = sim_hash(str)
    for i in range(32):
        byt = 0
        for n in range(4):
            index = i * 4 + n
            value = stat[index]
            byt = '1' if value >= 0 else '0'
            yield byt


def calc_string_simh(str):
    stat = sim_hash(str)
    for i in range(32):
        byt = 0
        for n in range(4):
            index = i * 4 + n
            value = stat[index]
            byt <<= 1
            byt |= (1 if value >= 0 else 0)
        yield '%d' % byt


def test():
    for x in calc_string_simh("example"):
        print x,
    print ''
    for x in calc_string_simh("examples"):
        print x,

    print ''
    for x in calc_string_simh_bin("example"):
        print x,
    print ''
    for x in calc_string_simh_bin("examples"):
        print x,

    print ''
    print ELFHash('example') 
    print ELFHash('examples') 



