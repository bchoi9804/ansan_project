import json
import random
import time
from datetime import datetime
from unicodedata import category

from flask import Flask, Response, render_template

application = Flask(__name__)
random.seed()  # Initialize the random number generator


@application.route("/")
def index():
    return render_template("index.html")


def read_result_data():    
    count =  0
    mask = 0
    nomask = 0
    while True:
        with open("result.json", "r") as result_json:
            json_data = json.load(result_json)
        index = len(json_data)
        if index >0 and count < index :
            print(json_data[count])
            categroy_value = int(json_data[count]["category"])
            score = json_data[count]["score"]
            if categroy_value == 0:
                mask = score
                nomask = 60
            else :
                mask = 60
                nomask = score
        json_data = json.dumps(
            {
                "index": count,
                "nomask": nomask,
                "mask":mask,
            }
        )
        yield f"data:{json_data}\n\n"
        time.sleep(2)
        count += 1

def generate_random_data():
    i = 0.5
    while True:
        nomask = int(random.random() * 5+80)
        mask = int(random.random() * 5+95)
        if nomask > mask :
            temp = mask
            mask = nomask; lowmask = mask
        json_data = json.dumps(
            {
                "index": i,
                "nomask": int(random.random() * 10+80),
                "mask":int(random.random() * 10+90),
            }
        )
        yield f"data:{json_data}\n\n"
        time.sleep(2)
        i += 0.5

@application.route("/chart-data")
def chart_data():
    return Response(generate_random_data(), mimetype="text/event-stream")

@application.route("/chart-json")
def chart_json():
    return Response(read_result_data(), mimetype="text/event-stream")


if __name__ == "__main__":
    application.run(host="127.0.0.1", debug=True, threaded=True)
