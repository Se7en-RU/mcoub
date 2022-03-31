import urllib. request, json, os.path, asyncio
from random import choice
from shazamio.user_agent import USER_AGENTS
from shazamio import Shazam

class Coub:
    def getCoubSongUrl(self, url):
        url = url.replace("https://coub.com/view/","http://coub.com/api/v2/coubs/")

        try:
            opener = urllib.request.build_opener()
            opener.addheaders=[("User-agent", choice(USER_AGENTS))]
            urllib.request.install_opener(opener)
            response = urllib.request.urlopen(url)
        
        except:
            raise Exception("Unable to connect to coub.com")

        data = json.load(response)

        if (
            'file_versions' not in data
            and 'html5' not in data['file_versions']
            and 'audio' not in data['file_versions']['html5']
            and 'med' not in data['file_versions']['html5']['audio']
            and 'url' not in data['file_versions']['html5']['audio']['med']
        ):
            raise Exception("Cannot parse response")
        
        return data

    def downloadFile(self, url):
        try:
            opener = urllib.request.build_opener()
            opener.addheaders=[("User-agent", choice(USER_AGENTS))]
            urllib.request.install_opener(opener)
            dldata=opener.open(url)
        
        except:
            raise Exception("Unable to download track")
        
        file_name = os.path.basename(url)
        file_path = os.path.join('tracks/', file_name)

        try:
            if file_name[-3:] == 'mp4':
                with open(file_path, 'wb') as f:
                    f.write(b'\x00\x00' + dldata.read()[2:])
            if file_name[-3:] == 'mp3':
                with open(file_path, 'wb') as f:
                    f.write(dldata.read())
        except:
            raise Exception("Unable to save track")

        return file_path

    def deleteFile(self, file_path):
        try:
            os.remove(file_path)
        except:
            raise Exception("Unable to delete track")

    async def search(self, url):
        file_path = self.downloadFile(url)

        shazam = Shazam()
        data = await shazam.recognize_song(file_path)

        self.deleteFile(file_path)

        return data

        


if __name__ == "__main__":
    url = 'https://github.com/Se7en-RU/coub_music_searcher'
    coub = Coub()
    coub.search(url)
