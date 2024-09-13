import asyncio
import websockets
import json

url = None
key = None
exg = None


def get(ws, exchange):
    if exchange == "":
        return "Exchange is mandatory."
    else:
        exg = exchange

    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg))
    return


async def mass_subscribe_n_stream(ws, exg):
    try:
        req_msg = str(
            '{"MessageType":"GetMarketMessages","Exchange":"' + exg + '"}')
        print("Request : " + req_msg)
        await ws.send(req_msg)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return "Error"


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'MarketMessagesResult':
                return message
        except websockets.ConnectionClosedOK:
            break
        print(message)