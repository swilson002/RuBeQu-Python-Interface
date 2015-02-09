
class SongSearch:

	def __init__(self, exact):
		self.exact = exact

	def search(self, songs, criteria):
		if songs == None:
			return None
			
		if self.exact:
			return self.searchExact(songs, criteria)
		
		found = list()
		splitCriteria = criteria.split(' ')
		
		for song in songs:
			meetsCriteria = True
			for term in splitCriteria:
				if term.upper() not in song['band'].upper() and term.upper() not in song['name'].upper():
					meetsCriteria = False
					break
			if meetsCriteria:
				found.append(song)
				
		return found
	
	def searchExact(self, songs, criteria):
		if songs == None:
			return None
			
		found = list()
		
		for song in songs:
			if criteria.upper() == song['band'].upper() or criteria.upper() == song['name'].upper():
				found.append(song)
			
		return found

	def findNeverPlayed(self, songs):
		found = list()
		
		for song in songs:
			if int(song['play_count']) == 0:
				found.append(song)
				
		return found