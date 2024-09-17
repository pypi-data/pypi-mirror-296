import asyncio
import websockets
from datetime import datetime
import json
import time
import errno

url = None
key = None
exg = None
sym = None
msg = None
res = None
message = None


def get(ws):
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws))
    return rmsg


async def mass_subscribe_n_stream(ws):
    try:
        req_msg = str('{"MessageType":"GetExchanges"}')
        await ws.send(req_msg)
        print("Request : " + req_msg)
        rmsg = await get_msg(ws)  # Listens for the tick data until market close
        return rmsg
    except:
        return msg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'ExchangesResult':
                return message
        except websockets.ConnectionClosedOK:
            break

