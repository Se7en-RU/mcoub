import urllib. request, json
from random import choice
from shazamio.user_agent import USER_AGENTS

class Coub:
    def get_coub(self, coub_id):
        url = "http://coub.com/api/v2/coubs/" + coub_id
        print(url)

        try:
            opener = urllib.request.build_opener()
            opener.addheaders=[("User-agent", choice(USER_AGENTS))]
            urllib.request.install_opener(opener)
            response = urllib.request.urlopen(url, timeout=5)
        
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
            raise Exception("Cannot parse coub.com response")
        
        return data
