from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class App(Resource):
    """The API that makes get request to access devotionals"""

    def get(self,date: str):
        return {"Message": f"Went through for {date}"}, 200


api.add_resource(App, '/api/v1/devotional/daily/<string:date>')


if __name__ == "__main__":
    app.run(debug=True)