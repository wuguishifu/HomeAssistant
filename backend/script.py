from pyControl4.account import C4Account
from pyControl4.director import C4Director
from pyControl4.light import C4Light

from flask import Flask, request
from flask_cors import CORS, cross_origin

import asyncio
import dotenv
import os
import json

bedroom_controls = {
    'lights': 80,
    'bed_lights': 83,
    'sink_lights': 86,
    #  'shower_lights': 89,
    #  'shower_fan': 92,
}

dotenv.load_dotenv()
username = os.getenv("C4_USERNAME")
password = os.getenv("C4_PASSWORD")
ip = os.getenv("C4_IP")

account = C4Account(username, password)
asyncio.run(account.getAccountBearerToken())

accountControllers = asyncio.run(account.getAccountControllers())
directorBearerToken = asyncio.run(account.getDirectorBearerToken(
    accountControllers["controllerCommonName"]))["token"]
director = C4Director(ip, directorBearerToken)

#  initialize the app
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

@app.get('/items')
@cross_origin()
def get_items():
    return asyncio.run(director.getAllItemInfo())


@app.get('/lights')
@cross_origin()
def get_lights():
    items = json.loads(asyncio.run(director.getAllItemInfo()))
    lights = [item for item in items if "categories" in item and "lights" in item["categories"] and "user_interface" not in item["categories"]]
    return json.dumps(lights)


@app.post('/light_value')
@cross_origin()
def set_light_value():
    body = request.json
    asyncio.run(C4Light(director, body["light_id"]).rampToLevel(body["value"], 100))
    return json.dumps({"success": True, "newValue": body["value"]})


if __name__ == '__main__':
    app.run(debug=True)
