import asyncio
import websockets
import json
import errno
import os

url = None
key = None
exg = None


def get(ws, exchange):
    if exchange == "":
        print("Exchange is mandatory.")
    else:
        exg = exchange

    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg))
    return rmsg


async def mass_subscribe_n_stream(ws, exg):
    try:
        req_msg = str(
            '{"MessageType":"GetExchangeMessages","Exchange":"' + exg + '"}')
        await ws.send(req_msg)
        print("Request : " + req_msg)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return "Error"


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'ExchangeMessagesItemResult':
                return message
        except websockets.ConnectionClosedOK:
            break
        #print(message)
