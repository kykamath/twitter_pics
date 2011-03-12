'''
Created on Mar 11, 2011

@author: kykamath
'''
import cjson, sys, gzip
from settings import Settings
from datetime import datetime

class Utilities:
    @staticmethod
    def tweetInBoundingBox(tweet, bb=[30, 42, 129, 145]):                                                                                                                                            
        if not tweet.get('coordinates'): return False                                                                                                                        
        lng,lat = tweet['coordinates']['coordinates']                                                                                                                    
        if bb[0]<lat<bb[1] and bb[2]<lng<bb[3]: return True
    @staticmethod
    def iterateTweetsFromGzip(file):
        for line in gzip.open(file, 'rb'): 
            try:
                data = cjson.decode(line)
                if 'text' in data: yield data
            except: pass
    @staticmethod
    def writeToFileAsJson(data, file):
        try:
            f = open('%s'%file, 'a')
            f.write(cjson.encode(data)+'\n')
            f.close()
        except: pass
    @staticmethod
    def getDataFile(t):
        return '_'.join([str(t.year), str(t.month), str(t.day)])

class Parser:
    @staticmethod
    def getTweetsForJapan():
        japan_bb=[30, 42, 129, 145]
        for f in ['2011_3_11.gz']:
            for tweet in Utilities.iterateTweetsFromGzip(Settings.filter_folder+f):
                if Utilities.tweetInBoundingBox(tweet, japan_bb):
                    for site in Settings.pic_sites:
                        if site in tweet['text']: 
                            d = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
                            print d
                            Utilities.writeToFileAsJson(tweet, Settings.japan_pics_folder+'tweets/'+Utilities.getDataFile(d))

if __name__ == '__main__':
    Parser.getTweetsForJapan()
