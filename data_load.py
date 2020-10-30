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

class Data_list:
    def __init__(self, xlist=None, ylist=None):
        if xlist == None or ylist == None:
            self.xlist = []
            self.ylist = []
        else:
            self.xlist = xlist
            self.ylist = ylist

    def add(self, x, y):
        self.xlist.append(x)
        self.ylist.append(y)

    def count(self):
        return len(self.xlist)

    # def moving_average(self, win_siz=10, mov_siz=10):
    #     ma_xlist = []
    #     ma_ylist = []
    #     pos = self.xlist[0]
    #     idx = 0
    #     while True:
    #         idx = idx + fni(self.xlist[idx:], pos)
    #         win_end_idx = idx + fni(self.xlist[idx:], pos+win_siz)
    #         if idx == win_end_idx:
    #             if idx > len(self.xlist)/10*9: break
    #             else:
    #                 ma_xlist.append(pos + (win_siz/2))
    #                 ma_ylist.append(ma_ylist[-1])
    #                 pos = pos + mov_siz
    #                 continue
    #         cur_y = self.ylist[idx:win_end_idx]
    #         ma_xlist.append(pos + (win_siz/2))
    #         ma_ylist.append(sum(cur_y)/len(cur_y))
    #         pos = pos + mov_siz
    #     return Data_list(ma_xlist, ma_ylist)

    def upper_filtering(self, threshold):
        dl = Data_list()
        for i in range(len(self.xlist)):
            if self.ylist[i] > threshold:
                dl.add(self.xlist[i], self.ylist[i])
        return dl

def file_loader(path='data/C2_180103_073713.csv'):
    file = open(path, 'r')
    lines = file.readlines()
    file.close()
    art = Data_list()
    sco2 = Data_list()
    for line in lines[1:]:
        sl = line.split(',')
        if sl[1] != '':
            sco2.add(float(sl[0]), float(sl[1]))
        if sl[2] != '' and sl[2] != '\n':
            art.add(float(sl[0]), float(sl[2]))
    return art, sco2

def batch(path, avg_siz=10, win_siz=30):
    art, sco2 = file_loader(path)
    fart = art.upper_filtering(30)
    fsco2 = sco2.upper_filtering(10)
    art_ylist, sco2_ylist = moving_average(fart, fsco2, avg_siz=avg_siz)

    v = moving_correlation(art_ylist, sco2_ylist, win_siz=win_siz, mov_siz=win_siz)
    
    # sentence = path + ',' + str(win_siz) + ',' + str(avg_siz)
    # for vv in v:
    #     sentence += ',' + str(vv)
    # file = open('result.csv', 'a')
    # file.write(sentence + '\n')
    # file.close()

    import matplotlib.pyplot as plt
    x = list(range(0, len(art_ylist)))
    x2 = np.linspace(15, x[-1]-15, len(v))
    _, ax = plt.subplots(nrows=3, ncols=1)
    ax[0].set_title('COx')
    
    ax[0].scatter(x2, v, s=10)
    ax[1].set_title('MAP')
    ax[1].scatter(x, art_ylist, c='red', s=3)
    ax[2].set_title('SCO2')
    ax[2].scatter(x, sco2_ylist, c='green', s=3)
    plt.show()

import os
if __name__ == '__main__':
    batch('data/C4_180111_074321.csv')
    # files = os.listdir('data')

    # for file in files:
    #     for i in range(5, 50, 5):
    #         for j in range(10, 100, 10):
    #             batch('data/'+file, i, j)
