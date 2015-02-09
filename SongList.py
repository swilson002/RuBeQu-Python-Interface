import datetime

class SongList:
	
	def __init__(self, wrapper):
		self.wrapper = wrapper
		self.songs = None
		self.availableSongs = None
		
	def getSongs(self):
		if self.songs == None:
			self.songs = self.wrapper.getSongList()
		
		return self.songs
		
	def getAvailableSongs(self):
		if self.availableSongs == None:
			queuedSongs = self.wrapper.getUnavailableSongs()
			if queuedSongs == None:
				self.availableSongs = self.getSongs()
				return self.availableSongs
				
			self.availableSongs = list()
			for song in self.getSongs():
				found = False
				for queued in queuedSongs:
					if int(self.wrapper.getId(song['url'])) == int(queued['id']):
						found = True
						break
				
				if not found:
					self.availableSongs.append(song)
		
		return self.availableSongs
		
	def cutoff_songs(self, song_list, cutoff):
		if cutoff == None:
			return song_list
		
		cutoff_song_list = list()
		for song in song_list:
			if int(song['play_count']) >= cutoff:
				cutoff_song_list.append(song)
				
		return cutoff_song_list
		
	inputTimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
	def getLatestPlayed(self, lastHours):
		if lastHours == None:
			return None
		
		found = list()
		for song in self.getSongs():
			detailed_song = self.wrapper.getSongDetails(self.wrapper.getId(song['url']))
			if datetime.datetime.strptime(detailed_song['updated_at'], self.inputTimeFormat) + datetime.timedelta(hours=lastHours) >= datetime.datetime.utcnow():
				found.append(song)
		
		return found