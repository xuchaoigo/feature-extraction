from __future__ import division
import os
import sys
import csv
import feature_evaluation


def calc_ig(bapp_wapp_bcnt_wcnt):
    black_num = 50000
    white_num = 500000
    ig_black_list = []
    ig_white_list = []
    with open(bapp_wapp_bcnt_wcnt, 'r') as fin:
        r = csv.reader(fin)
        first = True
        for line in r:
            if first:
                first = False
                continue
            bapp = line[0]
            wapp = line[1]
            bcnt = line[2]
            wcnt = line[3]
            app_name = bapp if bapp != "NULL" else wapp
            bcnt = int(bcnt) if bcnt != "NULL" else 0
            wcnt = int(wcnt) if wcnt != "NULL" else 0

            #score = feature_evaluation.information_gain(bcnt, wcnt, black_num, white_num)
            #score = feature_evaluation.information_gain_ratio([(bcnt, wcnt),(black_num-bcnt, white_num-wcnt)])
            #print 'call, this fet, bcnt = %d,  black_num-bcnt= %d'%(bcnt, wcnt)
            score = feature_evaluation.gini([(bcnt, wcnt),(black_num-bcnt, white_num-wcnt)])
            if feature_evaluation.black_or_white(bcnt, wcnt, black_num, white_num) == "black":
                ig_black_list.append((app_name, score))
            else:
                ig_white_list.append((app_name, score))
    
    ig_black_list.sort(key=lambda d:d[1], reverse = True)
    ig_white_list.sort(key=lambda d:d[1], reverse = True)

    TOP_BLACK = 3000
    TOP_WHITE = 5000
    #ig_black_list = ig_black_list[:TOP_BLACK]
    #ig_white_list = ig_white_list[:TOP_WHITE]
    ig_black_list = ig_black_list
    ig_white_list = ig_white_list
    with open("b.tmp3", 'w') as fo:
        for v1, v2 in ig_black_list:
            fo.write(v1 + ',' + str(v2) + '\n')
    with open("w.tmp3", 'w') as fo:
        for v1, v2 in ig_white_list:
            fo.write(v1 + ',' + str(v2) + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python .py inputfile'
        sys.exit()

    fin = sys.argv[1]
    calc_ig(fin)
