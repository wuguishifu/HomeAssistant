from pyControl4.account import C4Account
from pyControl4.director import C4Director
from pyControl4.light import C4Light
import asyncio
import dotenv
import os
import time
import random

bedroom_controls = {
    'lights': 80,
    'bed_lights': 83,
    'sink_lights': 86,
    # 'shower_lights': 89,
    # 'shower_fan': 92,
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

lights = {}
for [key, value] in bedroom_controls.items():
    lights[key] = C4Light(director, value)

# for i in range(10):
#     for [key, value] in lights.items():
#         asyncio.run(value.rampToLevel(random.randint(0, 100), 100))
#     time.sleep(1)

# for [key, value] in lights.items():
#     asyncio.run(value.rampToLevel(0, 100))

asyncio.run(lights['lights'].rampToLevel(100, 100))
