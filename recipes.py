import requests
from secrets import app_id, app_num

class Recipe():
    def __init__(self):
        self.app_id = app_id
        self.app_num = app_num 

    def search_recipe(self, query="steak"):
        url = 'https://api.edamam.com/search?q=' + query + '&app_id=' + self.app_id + \
            '&app_key=' + self.app_num

        r = requests.get(url)
        if r.status_code == 401:
            print("URL not found!")
            return
        return r.json() 