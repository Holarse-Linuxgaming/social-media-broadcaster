import feedparser
import time
from datetime import datetime

'''
TODO: Implement fallbacks for RSS Feeds, where the 'created' or 'published' tags are missing
'''

class RSSFeed:
	def __init__(self,rssfeed):
		self.rssfeed = feedparser.parse(rssfeed)
	def getTitle(self):
		return self.rssfeed.feed.title
	def getInfo(self):
		return self.rssfeed.feed.description
	def getFeedUpdateTime(self):
		try:
			return self.rssfeed.published_parsed
		except AttributeError:
			# If theres no lastBuildDate or similiar in the RSSFeed
			return self.rssfeed.updated_parsed
	def checkFeedUpdateTime(self, UpdateTime):
		localTime = time.gmtime()
		FeedUpdateTime = self.getFeedUpdateTime()
		
		Difference = time.mktime(FeedUpdateTime)-time.mktime(localTime)
		Difference = int((Difference / 60)) * -1
		
		if (Difference <= UpdateTime and Difference >= 0):
			return True
	def checkUpdate(self, Intervall):
		ArticleNews = {}
		if (self.checkFeedUpdateTime(Intervall)):
			for entries in self.rssfeed.entries:				
				ArticleTime 	= entries.published_parsed
				localTime	= time.gmtime()
				
				Difference 	= time.mktime(ArticleTime)-time.mktime(localTime)
				Difference 	= int((Difference / 60)) * -1
				
				if(Difference <= Intervall and Difference >= 0):
					ArticleTitle			= entries.title
					ArticleShortDescription		= entries.summary
					ArticleURL			= entries.link
					
					ArticleNews[ArticleTitle] 	= [ArticleURL, ArticleShortDescription]
			if (ArticleNews == {}):
				ArticleNews = False
			return ArticleNews
		else:
			return False
	def debugOutput(self):
		print(self.getTitle())
		print(self.getInfo())
		Articles = 1;
		for entries in self.rssfeed.entries:
			if(Articles <= 5):
				print(entries.title)
				print(time.strftime('Date: %d.%m.%Y Time: %H:%M:%S', entries.published_parsed))
				Articles = Articles + 1