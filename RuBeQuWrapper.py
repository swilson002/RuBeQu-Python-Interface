import json
import urllib2
import urllib

class RuBeQuWrapper:
	baseurl = 'http://xxx.xxx.xxx.xxx'
	
	def __init__(self, preview):
		self.preview = preview
	
	def getSongList(self):
		path = '/songs.json'
		response = urllib2.urlopen(self.baseurl + path).read()
		
		return json.loads(response)

	def getVolume(self):
		path = '/volume.json'
		
		return json.loads(urllib2.urlopen(self.baseurl + path).read())
		
	def setVolume(self, volume):
		if self.preview:
			return
			
		sessioninit = urllib2.Request(self.baseurl + '/')
		response = urllib2.urlopen(sessioninit)
		cookie = response.headers.get('Set-Cookie')
		token = '' #TODO: fiqure out how to get the proper X-CSRF Token
		
		path = '/volume/%s' % volume
		params = urllib.urlencode({})
		req = urllib2.Request(self.baseurl + path, params, {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
		req.add_header('cookie', cookie)
		req.add_header('Accept', '*/*')
		req.add_header('X-CSRF-Token', token)
		return urllib2.urlopen(req)
		
	def playSong(self, id):
		if self.preview:
			return
		path = '/songs/' + id + '/add_to_queue.json'
		return json.loads(urllib2.urlopen(self.baseurl + path).read())
		
	def playNext(self):
		if self.preview:
			return
		
		path = '/next.json'
		return json.loads(urllib2.urlopen(self.baseurl + path).read())
		
	def pause(self):
		if self.preview:
			return
		
		path = '/pause.json'
		return json.loads(urllib2.urlopen(self.baseurl + path).read())
		
	def resume(self):
		if self.preview:
			return
		
		path = '/play.json'
		return json.loads(urllib2.urlopen(self.baseurl + path).read())
	
	def getId(self, url):
		urlfront = self.baseurl + '/songs/'
		urlend = '.json'
		endlength = -1*len(urlend)
		return url[len(urlfront):endlength]
		
	def getCurrentSong(self):
		currentSongUrl = self.baseurl + '/current_song.json'
		return json.loads(urllib2.urlopen(currentSongUrl).read())
		
	songCache = dict()
	def getSongDetails(self, id):
		if id in self.songCache:
			return self.songCache[id]
			
		songUrl = self.baseurl + '/songs/' + id + '.json'
		song = json.loads(urllib2.urlopen(songUrl).read())
		self.songCache[id] = song
		return song
		
	def getQueue(self):
		queueUrl = self.baseurl + '/songs_in_queue.json'
		return json.loads(urllib2.urlopen(queueUrl).read())
		
	def getUnavailableSongs(self):
		currentSong = self.getCurrentSong()
		if currentSong == None:
			return None
		
		queue = self.getQueue()
		if queue == None:
			queue = list()
		
		queue.append(currentSong)
		return queue