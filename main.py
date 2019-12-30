import os

import requests
from flask import Flask, send_file, Response, render_template
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
    # Get translation from redirect URL
    response = requests.get(redirect)
    # Use BeautifulSoup to get translated fact
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('body').getText().strip()
    # Reponse body always starts with the following text, translation follows
    helper_string = 'Pig Latin\nEsultray\n\t\n'
    translation = body[len(helper_string):].strip()
    # Render page
    return render_template('translation.jinja2', input=fact, output=translation, url=redirect)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
