from pyControl4.account import C4Account
from pyControl4.director import C4Director
from pyControl4.light import C4Light

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

def get_lights():
    items = json.loads(asyncio.run(director.getAllItemInfo()))
    lights = [C4Light(director, item["id"]) for item in items if ("categories" in item.keys() and "light" in item["categories"])]
    for light in lights:
        light["current_state"] = asyncio.run(light.getstate())
    return lights

print(get_lights())