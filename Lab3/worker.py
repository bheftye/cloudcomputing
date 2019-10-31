from celery import Celery
import json

app = Celery('tasks', backend='rpc://', broker='pyamqp://workeruser:bheftye@10.10.10.15:5672/parser')


@app.task
def parse(file, pronouns):
    with open(file) as f:
        line = f.readline()
        while line:
            try:
                tweetObj = json.loads(line)
                if "text" in tweetObj and "retweeted_status" not in tweetObj:
                    pronouns["Tweets"] += 1
                    pronounCount(tweetObj["text"], pronouns)
            finally:
                line = f.readline()
                line = f.readline()

    return pronouns


def pronounCount(text, pronouns):
    for key, value in pronouns.items():
        if key != "Tweets":
            pronouns[key] = value + text.count(key)
