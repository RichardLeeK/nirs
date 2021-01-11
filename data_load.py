import numpy as np
from utils import fni, moving_correlation, moving_average, moving_average_with_null

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
    # art_ylist, sco2_ylist = moving_average(fart, fsco2, avg_siz=avg_siz)

    # v = moving_correlation(art_ylist, sco2_ylist, win_siz=win_siz, mov_siz=win_siz)
    
    # sentence = path + ',' + str(win_siz) + ',' + str(avg_siz)
    # for vv in v:
    #     sentence += ',' + str(vv)
    # file = open('result.csv', 'a')
    # file.write(sentence + '\n')
    # file.close()

    art_x, sco2_x, art_y, sco2_y = moving_average_with_null(fart, fsco2, avg_siz=avg_siz)
     

    import matplotlib.pyplot as plt
    # x = list(range(0, len(art_ylist)))
    # x2 = np.linspace(15, x[-1]-15, len(v))
    _, ax = plt.subplots(nrows=2, ncols=1, constrained_layout=True)
    ax[0].set_title('MAP')
    ax[0].scatter(art_x, art_y, c='red', s=3)
    ax[1].set_title('SCO2')
    ax[1].scatter(sco2_x, sco2_y, c='green', s=3)
    plt.savefig('img/' + path.split('/')[-1].split('.')[0])

import os
if __name__ == '__main__':
    
    files = os.listdir('data')
    for file in files:
        batch('data/' + file)


    # for file in files:
    #     for i in range(5, 50, 5):
    #         for j in range(10, 100, 10):
    #             batch('data/'+file, i, j)
