from flask import Flask
from routes import pages
from pymongo import MongoClient

app = Flask(__name__)
app.register_blueprint(pages)
client = MongoClient("mongodb://localhost:#####")
app.db = client.habittracker

if __name__ == "__main__":
    app.run(debug=True)
