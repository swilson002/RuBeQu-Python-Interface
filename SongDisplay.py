import RuBeQuWrapper
import datetime

class SongDisplay:
	inputTimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
	outputTimeFormat = '%m/%d/%Y %H:%M'
	
	def __init__(self, wrapper):
		self.wrapper = wrapper
		
	def displayQueue(self):
		print 'Playing:'
		self.displaySingleSong(self.wrapper.getCurrentSong(), None)
		print 'Queued:'
		self.displaySongs(self.wrapper.getQueue(), None)
	
	def topX(self, songs, amount):
		if songs == None:
			return
		sortedList = sorted(songs, key=lambda count: count['play_count'], reverse=True)
		
		self.displaySongs(sortedList[:int(amount)], self.getSongCount)
			
	def displaySongs(self, songs, extraDisplay):
		if songs == None:
			return
		for song in songs:
			self.displaySingleSong(song, extraDisplay)
		
		#print 'Found %s song(s)' % len(songs)
			
	def displaySingleSong(self, song, extraDisplay):
		if song == None:
			return
		
		output = '{0} - {1}'.format(song['band'], song['name'])

		if extraDisplay != None:
			output += extraDisplay(song)
		print output
		
	def getDetails(self, song):
		detailed_song = self.wrapper.getSongDetails(self.wrapper.getId(song['url']))
		output = '\nAlbum: {0}'.format(detailed_song['album'])
		output += '\nPlay Count: {0}'.format(detailed_song['play_count'])
		output += '\nLast Played: {0}'.format(self.formatDate(detailed_song['updated_at']))
		output += '\nUploaded: {0}'.format(self.formatDate(detailed_song['created_at']))
		return output
		
	def getSongCount(self, song):
		return ', Played {0} times'.format(song['play_count'])
		
	def getLastPlayed(self, song):
		detailed_song = self.wrapper.getSongDetails(self.wrapper.getId(song['url']))
		return ', Last Played: {0}'.format(self.formatDate(detailed_song['updated_at']))
		
	def formatDate(self, date):
		return datetime.datetime.strftime(datetime.datetime.strptime(date, self.inputTimeFormat), self.outputTimeFormat)