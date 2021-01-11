import numpy as np
import math

def fni(dl, val):
    # find nearest index: data list, value
    idx = np.searchsorted(np.array(dl), val, side='left')
    if idx > 0 and (idx == len(dl)) or (math.fabs(val - dl[idx - 1]) < math.fabs(val - dl[idx])):
        return idx - 1
    else:
        return idx

def moving_correlation(data1, data2, win_siz=30, mov_siz=30, mode='pearson'):
    i = 0
    mc = []
    while i + win_siz < len(data1):
        cur1 = data1[i:i+win_siz]
        cur2 = data2[i:i+win_siz]
        mc.append(np.corrcoef(cur1, cur2)[0, 1])
        i += mov_siz
    return mc

def moving_average(dlc1, dlc2, avg_siz=10):
    start_pos = dlc1.xlist[0] if dlc1.xlist[0] > dlc2.xlist[0] else dlc2.xlist[0]
    end_pos = dlc1.xlist[-1] if dlc1.xlist[-1] < dlc2.xlist[-1] else dlc2.xlist[-1]
    cur_pos = start_pos
    ylist1 = []
    ylist2 = []
    while cur_pos < end_pos:
        si = fni(dlc1.xlist, cur_pos)
        ei = fni(dlc1.xlist, cur_pos+avg_siz)
        if si != ei: ylist1.append(np.average(dlc1.ylist[si:ei]))
        else: ylist1.append(ylist1[-1])

        si = fni(dlc2.xlist, cur_pos)
        ei = fni(dlc2.xlist, cur_pos+avg_siz)
        if si != ei: ylist2.append(np.average(dlc2.ylist[si:ei]))
        else: ylist2.append(ylist2[-1])

        cur_pos += avg_siz
    return ylist1, ylist2

def moving_average_with_null(dlc1, dlc2, avg_siz=10):
    start_pos = dlc1.xlist[0] if dlc1.xlist[0] > dlc2.xlist[0] else dlc2.xlist[0]
    end_pos = dlc1.xlist[-1] if dlc1.xlist[-1] < dlc2.xlist[-1] else dlc2.xlist[-1]
    cur_pos = start_pos
    xlist1 = []; xlist2 = []; ylist1 = []; ylist2 = []
    while cur_pos < end_pos:
        si = fni(dlc1.xlist, cur_pos)
        ei = fni(dlc1.xlist, cur_pos+avg_siz)
        if si != ei:
            xlist1.append((cur_pos + end_pos)/2)
            ylist1.append(np.average(dlc1.ylist[si:ei]))

        si = fni(dlc2.xlist, cur_pos)
        ei = fni(dlc2.xlist, cur_pos+avg_siz)
        if si != ei:
            xlist2.append((cur_pos + end_pos)/2)
            ylist2.append(np.average(dlc2.ylist[si:ei]))
        
        cur_pos += avg_siz
    return xlist1, xlist2, ylist1, ylist2
