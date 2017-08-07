from __future__ import division
import os
import sys
import math
import traceback

def black_or_white(black_in, white_in, black_num,white_num):
    type = "white"
    black_in = float(black_in)
    white_in = float(white_in)
    black_num = float(black_num)
    white_num = float(white_num)
    if black_in == 0:
        type = "white"
    elif white_in == 0:
        type = "black"
    else:
        if black_in * white_num > white_in * black_num:
            type = "black"
        else:
            type = "white"
    return type


def _entropy(p,q):
    if p==0:
        entropy=-q*math.log(q,2)
    elif q==0:
        entropy=-p*math.log(p,2)
    else:    
        entropy=(-p*math.log(p,2)-q*math.log(q,2))
    return entropy


def information_value(value_list):
    #value_list: ((v1_black_num, v1_white_num), (v2_black_num, v2_white_num), ...)
    if len(value_list) == 0:
        print "value error"
        return
    black_all = sum([black_n for black_n, white_n in value_list])
    white_all = sum([white_n for black_n, white_n in value_list])
    sum_all = float(black_all + white_all)
    iv_value= 0.0
    try:
        for black_n, white_n in value_list:
            black_n = 1 if black_n == 0 else black_n
            white_n = 1 if white_n == 0 else white_n
            pyi = black_n/(black_n+white_n)
            pni = white_n/(black_n+white_n)
            iv_value += (pyi-pni)*math.log(pyi/pni, 2)
    except Exception,e:
        print 'black_num=',black_all
        print 'white_num=',white_all 
        traceback.print_exc()
    return iv_value
    

def gini(value_list):
    #value_list: ((v1_black_num, v1_white_num), (v2_black_num, v2_white_num), ...)
    if len(value_list) == 0:
        print "value error"
        return
    black_all = sum([black_n for black_n, white_n in value_list])
    white_all = sum([white_n for black_n, white_n in value_list])
    sum_all = float(black_all + white_all)
    gini = 0.0
    for black_n, white_n in value_list:
        gini += ((black_n+white_n)/sum_all)**2
    return 1 - gini


def information_gain_ratio(value_list):
    #value_list: ((v1_black_num, v1_white_num), (v2_black_num, v2_white_num), ...)
    if len(value_list) == 0:
        print "value error"
        return
    black_all = sum([black_n for black_n, white_n in value_list])
    white_all = sum([white_n for black_n, white_n in value_list])
    sum_all = float(black_all + white_all)
    conditional_entropy = 0.0
    split_info = 0.0
    information_gain_ratio = 0.0
    try:
        system_entropy = _entropy(black_all/sum_all, white_all/sum_all)
        for black_n, white_n in value_list:
            conditional_entropy += ((black_n+white_n)/sum_all) * _entropy(black_n/(black_n+white_n),white_n/(black_n+white_n))
            split_info += _entropy((black_n+white_n)/sum_all, 0)
        information_gain = system_entropy-conditional_entropy
        information_gain_ratio = information_gain/split_info
    except Exception,e:
        print 'black_num=',black_all
        print 'white_num=',white_all 
        traceback.print_exc()
    return information_gain_ratio



def information_gain(value_list):
    #value_list: ((v1_black_num, v1_white_num), (v2_black_num, v2_white_num))
    if len(value_list) == 0:
        print "value error"
        return
    black_all = sum([black_n for black_n, white_n in value_list])
    white_all = sum([white_n for black_n, white_n in value_list])
    sum_all = float(black_all + white_all)
    conditional_entropy = 0.0
    split_info = 0.0
    information_gain_ratio = 0.0
    try:
        system_entropy = _entropy(black_all/sum_all, white_all/sum_all)
        for black_n, white_n in value_list:
            conditional_entropy += ((black_n+white_n)/sum_all) * _entropy(black_n/(black_n+white_n),white_n/(black_n+white_n))
        information_gain = system_entropy-conditional_entropy
    except Exception,e:
        print 'black_num=',black_all
        print 'white_num=',white_all 
        traceback.print_exc()
    return information_gain


def chi2(value_list):
    #value_list: ((v1_black_num, v1_white_num), (v2_black_num, v2_white_num))
    if len(value_list) == 0:
        print "value error"
        return
    black_all = sum([black_n for black_n, white_n in value_list])
    white_all = sum([white_n for black_n, white_n in value_list])
    sum_all = float(black_all + white_all)
    if len(value_list) != 2:
        print 'chi2 only works for 0/1 value.'
        sys.exit(1)
    try:
        black_in =  value_list[0][0]
        black_out = value_list[1][0]
        white_in = value_list[0][1]
        white_out = value_list[1][1]
        chi2 = pow((black_in*white_out-white_in*black_out),2) / ((black_in+white_in)*(black_out+white_out))
    except Exception,e:
        print 'black_num=',black_all
        print 'white_num=',white_all 
        traceback.print_exc()
    return chi2


