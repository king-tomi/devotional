import calendar
from flask import Flask, jsonify
from flask_restful import Resource, Api
from scrape import *

app = Flask(__name__)
api = Api(app)

URL = "https://flatimes.com"

TAGS = {
        "trem-devotional": "TREM",
        "rccg": "Open Heaven",
        "anglican-communion": "Anglican",
        "open-heavens-daily-devotional": "Open Heaven",
        "seeds-of-destiny": "Seeds Of Destiny",
        "dclm-daily-manna": "DCLM",
        "kenneth-copeland": "Kenneth Copeland",
        "andrew-wommack": "Andrew Wommack" 
    }

class List_Posts(Resource):
    """The API that makes get request to access devotionals"""

    TAGS = {
        "trem-devotional": "TREM",
        "rccg": "Open Heaven",
        "anglican-communion": "Anglican",
        "open-heavens-daily-devotional": "Open Heaven",
        "seeds-of-destiny": "Seeds Of Destiny",
        "dclm-daily-manna": "DCLM",
        "kenneth-copeland": "Kenneth Copeland",
        "andrew-wommack": "Andrew Wommack" 
    }
    def get(self, category: str):
        res = get_all_posts(URL, category=category, church=self.TAGS.get(category))
        if res is not None:
            return jsonify(res)
        else:
            return jsonify({"message": "Error! Invalid Tag"})


class Post(Resource):
    """gets info about a particular post"""
    TAGS = {
        "trem-devotional": get_data_trem,
        "rccg": get_data_open_teens,
        "anglican-communion": get_data_anglican,
        "open-heavens-daily-devotional": get_data_open_teens,
        "seeds-of-destiny": get_data_dunamis,
        "dclm-daily-manna": get_data_dlcm,
        "kenneth-copeland": get_data_kenneth,
        "andrew-wommack": get_data_andrew 
    }
    def get(self, dat: str, category: str):
        dat_full = dat.split("-")
        mon = calendar.month_name[int(dat_full[1])]
        new_date = dat_full[0] + " " + mon + " " + dat_full[-1]
        posts = get_all_posts(URL, category, TAGS.get(category), new_date)
        final = {}
        if posts is not None:
            for name, post in posts.items():
                res = self.TAGS[category](post, TAGS[category])
                final[name] = res
            if final != {}:
                return jsonify(final)
            else:
                print("Error here")
                return jsonify({"message": "Error! Invalid Request"})
        else:
            print("No Here")
            return jsonify({"message": "Error! Invalid Request"})

api.add_resource(List_Posts, '/api/v1/devotional/daily/all_posts/<category>')
api.add_resource(Post, "/api/v1/devotional/daily/post/<dat>/<category>")


if __name__ == "__main__":
    app.run(debug=True)