'''
Created on Mar 11, 2011

@author: kykamath
'''
import cjson, sys, gzip, os, time
from settings import Settings
from datetime import datetime
from lxml.html import parse

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
    def iterateTweetsFromFile(file):
        for line in open(file): 
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
    
class HTMLParsers:
    @staticmethod
    def parseTwitpic(url, output_file):
        doc = parse(url).getroot()
        row = doc.cssselect('#photo-display')[0]
        os.system('curl "%s" > %s'%(row.get('src'), output_file))
            
            

class Parser:
    @staticmethod
    def getTweetsForJapan():
        japan_bb=[30, 42, 129, 145]
        for f in ['2011_3_10.gz']:
            for tweet in Utilities.iterateTweetsFromGzip(Settings.geo_folder+f):
                if Utilities.tweetInBoundingBox(tweet, japan_bb):
                    for site in Settings.pic_sites:
                        if site in tweet['text']: 
                            d = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
                            print d
                            Utilities.writeToFileAsJson(tweet, Settings.japan_pics_folder+'tweets/'+Utilities.getDataFile(d))
    @staticmethod
    def searchKeywords():
        keywords = sys.argv[1:]
        japan_bb=[30, 42, 129, 145]
        for f in ['2011_3_10.gz', '2011_3_11.gz']:
            for tweet in Utilities.iterateTweetsFromGzip(Settings.geo_folder+f):
                if Utilities.tweetInBoundingBox(tweet, japan_bb):
                    for k in keywords:
                        if k in tweet['text']: 
                            print cjson.encode(tweet)
    @staticmethod
    def downloadImages():
        for f in ['2011_3_10', '2011_3_11', '2011_3_12']:
            for tweet in Utilities.iterateTweetsFromGzip(Settings.japan_pics_folder+'tweets/'+f):
                d = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
                print d
                service, url = 'twitpic', tweet['urls']['url']
                if service in url:
                    id = url.split('/')[-1]
                    fileName = Settings.japan_pics_folder+Utilities.getDataFile(d)+'/%s_%s'%(str(d).replace(' ', '_'), id)
                    print fileName
                    HTMLParsers.parseTwitpic(url, fileName)
                    time.sleep(3)
                    
if __name__ == '__main__':
#    Parser.getTweetsForJapan()
    Parser.downloadImages()