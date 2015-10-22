import configparser
import modules.rssfeed
import socialplugins.twitter

'''
TODO: Fix Lenght of a Tweet!'
'''

# Main / btw start
Config = configparser.ConfigParser()
Config.read('config.yml')
Intervall = Config.get('General', 'Timer', fallback='30')
Intervall = int(Intervall)

def main():
	module = {
		'rssfeed' : readrss(Intervall),
	}
	for entries in Config.sections():
		if (Config.has_option(entries, 'plugin') and Config.get(entries, 'plugin')):
			entry = Config.get(entries, 'plugin')
			Array = module[entry]
			if (Array != False):
				print('There is an update!')
				sendtoTwitter(Array)
			else:
				print('There is currently no updates.')
# Modules: Functions
def readrss(Intervall):
	for entries in Config.sections():
		url = Config.get(entries, 'url', fallback='no')
		if(url != 'no'):
			rssfeed = modules.rssfeed.RSSFeed(url)
			return rssfeed.checkUpdate(Intervall)

# Social Media Plugins: Functions
def sendtoTwitter(Array):
	CONSUMER_KEY 	= Config.get('Twitter', 'CONSUMER_KEY')
	CONSUMER_SECRET	= Config.get('Twitter', 'CONSUMER_SECRET')
	ACCESS_KEY 	= Config.get('Twitter', 'ACCESS_KEY')
	ACCESS_SECRET 	= Config.get('Twitter', 'ACCESS_SECRET')
	
	for TitleKey, RSSEntries in Array.items():
		Tweet = TitleKey + ': ' +  RSSEntries[0]
		if (len(Tweet) > 140):
			print('TODO: Fix Lenght of a Tweet!')
		else:
			print(Tweet)
			twitter = socialplugins.twitter.Twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
			twitter.sendTweet(Tweet)

if __name__ == "__main__":
    main()