import urllib. request, json, os.path
from random import choice
from shazamio.user_agent import USER_AGENTS
from shazamio import Shazam
from modules.database import Database


class Audio:
    def download(self, coub_data):
        if (
            'file_versions' not in coub_data
            and 'html5' not in coub_data['file_versions']
            and 'audio' not in coub_data['file_versions']['html5']
            and 'med' not in coub_data['file_versions']['html5']['audio']
            and 'url' not in coub_data['file_versions']['html5']['audio']['med']
        ):
            raise Exception("Cannot find audio url link")

        file_path = None
        url = coub_data['file_versions']['html5']['audio']['med']['url']

        try:
            opener = urllib.request.build_opener()
            opener.addheaders=[("User-agent", choice(USER_AGENTS))]
            urllib.request.install_opener(opener)
            dldata=opener.open(url)
        
        except:
            raise Exception("Unable to download track")
        
        file_name = os.path.basename(url)
        file_path = os.path.join('tmp/tracks', file_name)

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

    def delete(self, file_path):
        try:
            os.remove(file_path)
        except:
            raise Exception("Unable to delete track")

    async def search(self, coub_id, coub_data):
        shazam_data = None
        file_path =self.download(coub_data)

        if file_path:
            shazam = Shazam()
            shazam_data = await shazam.recognize_song(file_path)

            if not shazam_data or 'track' not in shazam_data:
                shazam_data = None

        self.delete(file_path)

        if shazam_data:
            try:
                db = Database()
                db.insert('INSERT INTO coubs (coub_id, shazam_data) VALUES(%s, %s)', (coub_id, json.dumps(shazam_data)))
                db.close()
            except:
                return shazam_data

        return shazam_data
