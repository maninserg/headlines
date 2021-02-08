import feedparser
from flask import Flask, render_template, request
import json
import urllib3


app = Flask(__name__)

RSS_FEEDS = {"bbc": "https://feeds.bbci.co.uk/news/rss.xml",
             "cnn": "http://rss.cnn.com/rss/edition.rss",
             "fox": "http://feeds.foxnews.com/foxnews/latest",
             "fontanka": "https://www.fontanka.ru/fontanka.rss",
             "iol": "https://www.iol.co.za/cmlink/1.640"}

DEFAULTS = {'publication': 'bbc',
            'city': 'Saint Petersburg,RU'}


@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get("publication")
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get("city")
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles,
                           weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f70330d2dcb552910e27d79718ebb2fc"
    url = api_url.format(query)
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    data = r.data
    parsed = json.loads(data)
    weather = {"description": parsed["weather"][0]["description"],
               "temperature": parsed["main"]["temp"],
               "city": parsed["name"]
               }
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)
