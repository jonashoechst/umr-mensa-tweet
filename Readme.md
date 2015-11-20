

# umr-mensa-tweet
... is a quick python3 weekend project to crawl a mensa feed and tweet the revealed menues. 

The script queries the last tweets in your timeline and compares them to the crawled menues, in order to avoid duplicated tweets.

## flow description
The python script gets this job done in this steps:

 - load a config.json file
 - crawl the given urls
 - parse the revealed rss feed and extract the menues
 - reformat the extracted descriptions
 - connect to the given twitter account
 - check if the feed is outdated
 - if true: tweet all menue descriptions
 
## dependencies

umr-mensa-tweet relies onto the tweepy python twitter library: [https://github.com/tweepy/tweepy](https://github.com/tweepy/tweepy)

## licenses

 - "THE BEER-WARE LICENSE" (Revision 42): <uni@jonashoechst.de> wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return. Jonas Höchst

 - Studentenwerk.png is taken from http://www.studentenwerk-marburg.de

![alt text](Studentenwerk.png "Logo Title Text 1")

