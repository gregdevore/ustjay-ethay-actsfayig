import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


@app.route('/')
def home():
    # URL for pig latinizer
    url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    # Get a random fact from the fact website
    fact = get_fact()
    # Submit post request to pig latinizer
    response = requests.post(url, {'input_text': fact}, allow_redirects=False)
    # Retrieve redirect url
    redirect = response.headers['Location']
    return redirect


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
