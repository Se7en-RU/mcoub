import re
from modules.database import Database
from modules.coub import Coub

class Check:
    def url(self, url):
        id = None
        result = re.search('^https?:\/\/coub\.com\/view\/?(\w+)', url)

        if result:
            id = result.group(1)
        
        return id

    def coub_data(self, coub_id):
        data = None

        try:
            coub = Coub()
            data = coub.get_coub(coub_id)
        except:
            return data
        
        return data

    def coub_exists(self, coub_id):
        data = None
        try:
            db = Database()
            data = db.select('SELECT shazam_data from coubs where coub_id = %(coub_id)s', {'coub_id': coub_id})
            db.close()
        except:
            return data
        
        return data
