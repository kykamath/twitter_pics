'''
Created on Mar 11, 2011

@author: kykamath
'''
import cjson, sys, gzip, os, time, glob
from settings import Settings
from datetime import datetime
from lxml.html import parse

class Utilities:
    @staticmethod
    def tweetInBoundingBox(tweet, bb):                                                                                                                                            
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
    @staticmethod
    def parseYfrog(url, output_file):
        doc = parse(url).getroot()
        row = doc.cssselect('#main_image')[0]
        os.system('curl "%s" > %s'%(row.get('src'), output_file))
    @staticmethod
    def parseTwitrpix(url, output_file):
        id = url.split('/')[-1]
        os.system('curl "http://img.twitrpix.com/%s" > %s'%(id, output_file))

class Parser:
    @staticmethod
    def getTweetsForJapan():
        japan_bb=[30, 42, 129, 145]
#        for f in glob.glob1(Settings.geo_folder, '*'):
        for f in ['2011_3_%s.gz'%i for i in range(5, 16)]:
            for tweet in Utilities.iterateTweetsFromGzip(Settings.geo_folder+f):
                if Utilities.tweetInBoundingBox(tweet, japan_bb):
                    for site in Settings.pic_sites:
                        if site in tweet['text']: 
                            d = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
                            print d
                            Utilities.writeToFileAsJson(tweet, Settings.japan_pics_folder+'tweets/'+Utilities.getDataFile(d))
    @staticmethod
    def getTweetsForNewZealand():
        nz_bb=[-48.0, -32.0, 165.0, 179.0]
#        for f in glob.glob1(Settings.geo_folder, '*'):
        for f in ['2011_2_%s.gz'%i for i in range(20, 26)]:
            for tweet in Utilities.iterateTweetsFromGzip(Settings.geo_folder+f):
                if Utilities.tweetInBoundingBox(tweet, nz_bb):
                    for site in Settings.pic_sites:
                        if site in tweet['text']: 
                            d = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
                            print d
#                            print tweet, Settings.new_zealand_pics_folder+'tweets/'+Utilities.getDataFile(d)
                            Utilities.writeToFileAsJson(tweet, Settings.new_zealand_pics_folder+'tweets/'+Utilities.getDataFile(d))
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
        services = {'twitpic': HTMLParsers.parseTwitpic, 'yfrog': HTMLParsers.parseYfrog, 'twitrpix': HTMLParsers.parseTwitrpix}
        for f in ['2011_2_%s'%i for i in range(20, 26)]:
            for tweet in Utilities.iterateTweetsFromFile(Settings.new_zealand_pics_folder+'tweets/'+f):
                d = datetime.strptime(tweet['created_at'], Settings.twitter_api_time_format)
                print d
                print cjson.encode(tweet)
                
                service, url = 'twitpic', ''
                if len(tweet['entities']['urls'])>0: url = tweet['entities']['urls'][0]['url']
                else:
                    for service, parseMethod in services.iteritems():
                        if service in tweet['text']:
                            for term in tweet['text'].split():
                                if service in term: 
                                    url = term
                                    break
                url = url.replace('\\', '')
                if not url.startswith('http'): url = 'http://'+url
                for service, parseMethod in services.iteritems():
                    if service in url:
                        id = tweet['id']
                        fileName = Settings.new_zealand_pics_folder+Utilities.getDataFile(d)+'/%s_%s.jpeg'%(str(d).replace(' ', '_'), id)
                        print url, fileName
                        folder = '/'.join(fileName.split('/')[:-1])
                        if not os.path.exists(folder): os.makedirs(folder, 0777)
                        if not os.path.exists(fileName):
                            retry, notParsed = 0, True
                            while retry<3 and notParsed:
                                try:
                                    parseMethod(url, fileName)
                                    notParsed = False
                                    time.sleep(3)
                                except: retry+=1
                    
if __name__ == '__main__':
#    Parser.getTweetsForJapan()
#    Parser.getTweetsForNewZealand()
    
    Parser.downloadImages()
