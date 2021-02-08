import feedparser
from flask import Flask, render_template


app = Flask(__name__)

RSS_FEEDS = {"bbc": "https://feeds.bbci.co.uk/news/rss.xml",
             "cnn": "http://rss.cnn.com/rss/edition.rss",
             "fox": "http://feeds.foxnews.com/foxnews/latest",
             "fontanka": "https://www.fontanka.ru/fontanka.rss",
             "iol": "https://www.iol.co.za/cmlink/1.640"}


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html",
                           articles=feed["entries"],
                           publication=publication)


if __name__ == '__main__':
    app.run(port=5008, debug=True)
