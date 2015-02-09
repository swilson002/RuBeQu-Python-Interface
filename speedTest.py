import RuBeQuWrapper
import json
import urllib2
import time

def main():
	start = time.time()
	rubequ = RuBeQuWrapper.RuBeQuWrapper(True)
	songList = rubequ.getSongList()
	
	individualStart = time.time()
	
	for song in songList:
		json.loads(urllib2.urlopen(song['url']).read())
		
	end = time.time()
	
	print "Time to get details: " +  str(end - individualStart)
	print "Total elapsed: " + str(end - start)

if __name__ == "__main__":
	main()