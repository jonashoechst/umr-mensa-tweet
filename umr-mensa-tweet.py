#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.dom import minidom
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
import re, tweepy, json, sys, logging, os
from datetime import date

def removeBracketText(string):
    return re.sub("[\(].*?[\)]", "", string)
    
def replacePrice(string):
    string = re.sub("nur ", "(", string)
    string = re.sub(" Euro", u"€)", string)
    return string
    
def reformatString(string):
    string = " ".join([line.strip() for line in string.splitlines()])
    string = re.sub(" , ",", ", string) # remove blanks in front of commas
    string = re.sub("- | -"," - ", string) # create double blanks for single blanked dashes
    string = re.sub(" +"," ", string) # remove double blanks
    string += u" #Marburg #Mensa #"+dayOfWeekString()
    string = " ".join(string[:140].split(' ')[:-1]) if len(string)>140 else string
    return string

def dayOfWeekString():
    return ("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag")[date.today().weekday()]

def getFeedMenues(feedUrl):
    feedConnection = urlopen(feedUrl)
    menues = []
    xmlData = feedConnection.read()
    xml = minidom.parseString(xmlData)
    for item in xml.getElementsByTagName("item"):
        try:
            menue = item.getElementsByTagName("description")[0].childNodes[0].nodeValue + ": "
            menue += item.getElementsByTagName("title")[0].childNodes[0].nodeValue
            menue = removeBracketText(menue)
            menue = replacePrice(menue)
            menue = reformatString(menue)
            menues.append(menue)
        except IndexError:
            logging.warn("No description/title found for item: "+item.toxml())
        
    return menues

def loadServices(config_filename):
    class DictStruct:
        def __init__(self, data): self.__dict__.update(data)
        
    with open(config_filename, "r") as config_file:
        config = json.load(config_file)
        return [DictStruct(service) for service in config]

def getApi(service):
    auth = tweepy.OAuthHandler(s.consumer_key, s.consumer_secret)
    auth.set_access_token(s.access_token, s.access_token_secret)
    api = tweepy.API(auth)
    return api
    
def tweetMenues(api, menues):
    count = 0
    for menu in reversed(menues):
        try: api.update_status(menu); count += 1
        except tweepy.error.TweepError as e: 
            logging.warn("Tweet could not be send: "+str(e)) #+"("+str(e[0][0]["code"])+")")
    return count
    
if __name__ == "__main__":
    # create & save a print logger
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    printLog = logging.getLogger().handlers[0]
    
    # create a file logger and add print logger
    logging.basicConfig(filename='umr-mensa-tweet.log', level=logging.INFO, datefmt='%Y-%m-%d %H:%M', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logging.getLogger().addHandler(printLog)
    
    services = loadServices("/".join(os.path.realpath(__file__).split("/")[:-1])+"/config.json")
    
    for s in services:
        menues = getFeedMenues(s.feed_url)
        api = getApi(s)
        new_tweets = tweetMenues(api, menues)
        logging.info("Inserted "+str(new_tweets)+" tweets for "+s.name if hasattr(s, 'name') else s.feed_url)
        
    logging.info("umr-mensa-tweet finished successfully.")