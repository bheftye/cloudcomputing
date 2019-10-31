from worker import parse
from flask import Flask, jsonify
import subprocess
import sys
import os
import copy

app = Flask(__name__)

pronouns = {
    "Tweets": 0,
    "han": 0,
    "hon": 0,
    "den": 0,
    "det": 0,
    "denna": 0,
    "denne": 0,
    "hen": 0
}


@app.route('/', methods=['GET'])
def getPronouns():
    response = copy.copy(pronouns)
    tasks = []
    for filename in os.listdir('data'):
        tasks.append(parse.delay("data/" + filename, copy.copy(pronouns)))
    for task in tasks:
        add(response, task.get(timeout=60))
    return jsonify(response)


def add(pronouns, pronCount):
    pronouns["Tweets"] += pronCount["Tweets"]
    pronouns["han"] += pronCount["han"]
    pronouns["hon"] += pronCount["hon"]
    pronouns["den"] += pronCount["den"]
    pronouns["det"] += pronCount["det"]
    pronouns["denna"] += pronCount["denna"]
    pronouns["denne"] += pronCount["denne"]
    pronouns["hen"] += pronCount["hen"]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000 ,debug=True)