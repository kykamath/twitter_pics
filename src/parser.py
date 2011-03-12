'''
Created on Mar 11, 2011

@author: kykamath
'''
import cjson, sys, gzip
from settings import Settings

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


class Parser:
    @staticmethod
    def getTweetsForJapan():
        japan_bb=[30, 42, 129, 145]
        for f in ['2011_3_10.gz']:
            for tweet in Utilities.iterateTweetsFromGzip(Settings.filter_folder+f):
                if Utilities.tweetInBoundingBox(tweet, japan_bb):
                    if 'http' in tweet['text']:
                        print cjson.encode(tweet)

if __name__ == '__main__':
    Parser.getTweetsForJapan()