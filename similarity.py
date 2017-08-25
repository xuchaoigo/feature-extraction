from math import sqrt

def pearson(v1, v2):
    sum1, sum2 = sum(v1), sum(v2)
    sum1sq, sum2sq = sum([pow(v, 2) for v in v1]), sum([pow(v, 2) for v in v2])
    dotsum = sum([v1[i]*v2[i] for i in range(len(v1))])
    num = dotsum - (sum1*sum2/len(v1))
    den = sqrt((sum1sq - pow(sum1, 2)/len(v1)) *(sum2sq - pow(sum2, 2)/len(v1)))
    if den == 0:
        return den
    else:
        return 1.0 - num/den


def tanimoto(v1, v2):
    c1, c2, shr = 0, 0, 0
    for i in range(len(v1)):
        if v1[i] != 0:
            c1 += 1
        if v2[i] != 0:
            c2 += 1
        if v1[i] != 0 and v2[i] != 0:
            shr += 1
    return 1.0 - (float(shr)/(c1 + c2 - shr))
