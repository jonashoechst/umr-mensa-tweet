from xml.dom import minidom
import urllib.request
import re, tweepy, json

def removeBracketText(string):
    return re.sub("[\(].*?[\)]", "", string)
    
def replacePrice(string):
    string = re.sub("nur ", "(", string)
    string = re.sub(" Euro", "€)", string)
    return string
    
def reformatString(string):
    string = " ".join([line.strip() for line in string.splitlines()])
    string = re.sub(" , ",", ", string) # remove blanks in front of commas
    string = re.sub("- | -"," - ", string) # create double blanks for single blanked dashes
    string = re.sub(" +"," ", string) # remove double blanks
    return string
    
def getFeedMenues(feedUrl):
    feedConnection = urllib.request.urlopen(feedUrl)
    menues = []
    xmlData = feedConnection.read()
    xml = minidom.parseString(xmlData)
    for item in xml.getElementsByTagName("item"):
        menue = item.getElementsByTagName("description")[0].childNodes[0].nodeValue + ": "
        menue += item.getElementsByTagName("title")[0].childNodes[0].nodeValue
        menue = removeBracketText(menue)
        menue = replacePrice(menue)
        menue = reformatString(menue)
        menues.append(menue)
        
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
    
def timelineIsOutdated(api, menues, tweet_count=3):
    for tweet in api.home_timeline(count=tweet_count):
        if tweet.text in menues:
            return False
    return True
    
def tweetMenues(api, menues):
    for menu in reversed(menues):
        api.update_status(menu)
    
if __name__ == "__main__":
    services = loadServices("config.json")
    
    for s in services:
        menues = getFeedMenues(s.feed_url)
        api = getApi(s)
        if timelineIsOutdated(api, menues):
            print("Timeline outdated! Updating...")
            tweetMenues(api, menues)
        else:
            print("Timeline is up-to-date.")
        
    print("umr-mensa-tweet finished successfully.")