'''
Created on Mar 17, 2011

@author: kykamath
'''
import glob, commands, copy
from datetime import datetime
from settings import Settings
import numpy as np
import  matplotlib.pyplot as plt

class Analysis:
#    @staticmethod
#    def format_date(x, pos=None):
#        thisind = np.clip(int(x+0.5), 0, N-1)
#        return r.date[thisind].strftime('%Y-%m-%d')
    
    @staticmethod
    def imageDistribution():
        data = {}
        for f in glob.glob(Settings.japan_pics_folder+'/tweets/*'):
            d = datetime.strptime(f.split('/')[-1], '%Y_%m_%d')
            data[copy.copy(d)]=int(commands.getoutput('wc -l %s'%f).split()[0])
        dataX = sorted(data)[2:]
        dataY = [data[x] for x in dataX]
#        print dataX
#        print dataY
#        for k in sorted(data): print k, data[k]
        fig = plt.figure()
        plt.title('Image distribution on Twitter for Japan.')
        plt.ylabel('Number of images.')
        plt.plot(dataX, dataY, 'o-', color='m')
        fig.autofmt_xdate()
        plt.show()

if __name__ == '__main__':
    Analysis.imageDistribution()