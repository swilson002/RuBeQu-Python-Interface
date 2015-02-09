import RuBeQuWrapper
import SongList
import SongSearch
import SongDisplay
import argparse
import random

def main(args):
	wrapper = RuBeQuWrapper.RuBeQuWrapper(args.preview)
	songs = SongList.SongList(wrapper)
	search = SongSearch.SongSearch(args.findExact)
	display = SongDisplay.SongDisplay(wrapper)
	extraMethod = None
	if args.detailed:
		extraMethod = display.getDetails
			
	if args.top != None:
		display.topX(songs.getSongs(), args.top)
		
	if args.neverplayed:
		display.displaySongs(search.findNeverPlayed(songs.getSongs()), None)
		
	if args.getvolume:
		print wrapper.getVolume()
		
	if args.setvolume != None:
		volume = args.setvolume
		print 'Setting volume to %s' % volume
		wrapper.setVolume(volume)
		
	if args.play != None:
		play(getRandom(search.search(songs.getAvailableSongs(), args.play), args.count), wrapper)
	
	if args.random:
		play(getRandom(songs.cutoff_songs(songs.getAvailableSongs(), args.cutoff), args.count), wrapper)
		
	if args.weighted_random:
		play(getWeightedRandom(songs.cutoff_songs(songs.getAvailableSongs(), args.cutoff), args.count), wrapper)
		
	if args.displayQueue:
		display.displayQueue()
		
	if args.findSong != None:
		display.displaySongs(search.search(songs.getSongs(), args.findSong), extraMethod)
		
	if args.songCount:
		print str(len(songs.getSongs())) + " songs"
		
	if args.newest != None:
		display.displaySongs(songs.getSongs()[:args.newest], extraMethod)
		
	if args.latestPlayed != None:
		display.displaySongs(songs.getLatestPlayed(args.latestPlayed), display.getLastPlayed)
	
	if args.pause:
		print "Pausing"
		wrapper.pause()
		
	if args.resume:
		print "Resuming"
		wrapper.resume()
		
	if args.next:
		print "Skipping to next song"
		wrapper.playNext()
	
def play(songs, wrapper):
	if songs == None:
		return
	for item in songs:
		id = wrapper.getId(item['url'])
		print 'Queueing ' + item['band'] + ' - ' + item['name']
		wrapper.playSong(id)
	
def getRandom(songs, amount):
	if songs == None:
		return
	numberOfSongs = len(songs)
	if numberOfSongs < int(amount):
		amount = numberOfSongs
	
	random.seed()
	return random.sample(songs, int(amount))
	
def getWeightedRandom(songs, amount):
	if songs == None:
		return
		
	numberOfSongs = len(songs)
	if numberOfSongs < int(amount):
		amount = numberOfSongs
		
	tmp_list = list(songs)
	selected = list()
	for x in range(0, amount):
		weight = 0
		weight_list = list()
		
		for song in tmp_list:
			weight += int(song['play_count']) + 1
			weight_list.append(weight)
		
		rand = random.randrange(weight)
		
		index = find_index(weight_list, rand)
		selected.append(tmp_list.pop(index))
		
	return selected
	
def find_index(list, seed):
	low = 0
	high = len(list) - 1
	
	while low < high:
		mid = (low + high) / 2
		if(seed > list[mid]):
			low = mid + 1
		else:
			high = mid
			
	return low
	



def parseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('--top', dest='top', type=int, help='Get the most played songs on rubequ', default=None)
	parser.add_argument('--neverplayed', dest='neverplayed', help='Get list of songs that were never played', action='store_true', default=False)
	parser.add_argument('--getvolume', dest='getvolume', help='Get the volume', action='store_true', default=False)
	parser.add_argument('--setvolume', dest='setvolume', type=int, help='Set the volume (UNDER CONSTRUCTION)', default=None)
	parser.add_argument('--find', dest='findSong', help='Finds all songs with the given search criteria', default=None)
	parser.add_argument('--detailed', dest='detailed', help='Displays detailed information for each found song (UNDER CONSTRUCTION)', action='store_true', default=False)
	parser.add_argument('--songcount', dest='songCount', help='Get count of songs', action='store_true', default=False)
	parser.add_argument('--newest', dest='newest', type=int, help='Display newest X songs', default=None)
	parser.add_argument('--latestplayed', dest='latestPlayed', type=int, help='Display songs played in the last X hours (WARNING: SLOW)', default=None)
	parser.add_argument('--play', dest='play', help='Play random song that matches criteria', default=None)
	parser.add_argument('--playrandom', dest='random', help='Play random song', action='store_true', default=False)
	parser.add_argument('--playweightedrandom', dest='weighted_random', help='Play random song.  The more often a song was played, the more likely it will be played', action='store_true', default=False)
	parser.add_argument('--pause', dest='pause', help='Pause rubequ', action='store_true', default=False)
	parser.add_argument('--resume', dest='resume', help='Resumes rubequ', action='store_true', default=False)
	parser.add_argument('--next', dest='next', help='Skips to the next song', action='store_true', default=False)
	parser.add_argument('--queue', dest='displayQueue', help='Display current song and queued up songs', action='store_true', default=False)
	parser.add_argument('--exact', dest='findExact', help='Alters searches to find the exact artist/title instead of keyword', action='store_true', default=False)
	parser.add_argument('--count', dest='count', type=int, help='Play song commands will play X songs', default=1)
	parser.add_argument('--cutoff', dest='cutoff', type=int, help='Do not play songs that have not reached the cutoff count.  Only applies to songs randomly selected', default=None)
	parser.add_argument('--preview', dest='preview', help='Do not actually perform actions on rubequ', action='store_true', default=False)
	return parser.parse_args()
	
if __name__ == "__main__":
	main(parseArguments())