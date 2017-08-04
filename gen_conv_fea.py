import os
import time
import sys

SEP1='\x01'
SEP2='\x02'
SEP3='_'
LINE_NUM = 100000

def gen_kernel(kernel_len, mask_len):
    def _helper(result_list, result_tmp, cur_i, n):
        if cur_i >= n:
            result_list.append(result_tmp[:])
            return
        result_tmp[cur_i] = 0
        _helper(result_list, result_tmp, cur_i + 1, n)
        result_tmp[cur_i] = 1
        _helper(result_list, result_tmp, cur_i + 1, n)

    result_list = []
    result_tmp = [0] * kernel_len
    _helper(result_list, result_tmp, 0, kernel_len)
    return [kernel for kernel in result_list if sum(kernel) == mask_len]


def format_feature(srcfile):
    #1000003183^A20170612_2^B20170611_2^B20170610_9
    with open(srcfile) as fi:
        min, max = 30000000, 0 
        i = 0
        for line in fi: 
            if i % LINE_NUM == 0:
                print str(i) + '\t',
            i += 1
            passid, ts_all = line.strip().split(SEP1)
            ts_list = ts_all.split(SEP2)
            for kv in ts_list:
                k, v = kv.split(SEP3)
                k = int(k)
                max = k if k > max else max
                min = k if k < min else min
        print '\nmin = %d, max = %d'%(min, max)

    with open(srcfile) as fi:
        i = 0
        for line in fi: 
            if i % LINE_NUM == 0:
                print str(i) + '\t',
            i += 1
            passid, ts_all = line.strip().split(SEP1)
            ts_list = ts_all.split(SEP2)
            ts_value = [0] * (max - min + 1)
            for kv in ts_list:
                k, v = kv.split(SEP3)
                k = int(k)
                ts_value[k - min] = int(v)
            print ts_value       
            extract_conv(ts_value, gen_kernel(7, 4))


def extract_conv(ts_data_in, kernel_list):
    #conv padding
    kernel_len = len(kernel_list[0])
    ts_data = [0] *  (len(ts_data_in) + 2 * kernel_len - 2)
    for i,v in enumerate(ts_data_in):
        ts_data[kernel_len - 1 + i] = ts_data_in[i]
        
    d = {}
    for kernel in kernel_list:
        max_pooling = 0
        for base, v1 in enumerate(ts_data):
            sum = 0
            if base + kernel_len - 1 > len(ts_data) - 1:
                break
            for offset, v2 in enumerate(kernel):
                sum += ts_data[base + offset] * kernel[offset]
            max_pooling = sum if sum > max_pooling else max_pooling
        d[str(kernel)] = max_pooling
    for k in d:
        print k, d[k]


def do_test(infile):
    format_feature(infile) 


if __name__ == '__main__':
    if len(sys.argv)!=2:
        print 'Usage:'
        print sys.argv[0],' src_file'
        exit(-1)
    do_test(sys.argv[1])
