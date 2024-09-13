import asyncio
import websockets
import json

url = None
key = None
exg = None
sym = None
msg = None


def get(ws, exchange, symbol):
    exg = exchange
    sym = symbol
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym))
    return rmsg


def stop(ws, exchange, symbol):
    exg = exchange
    sym = symbol
    rmsg = asyncio.get_event_loop().run_until_complete(mass_unsubscribe_n_stream(ws, exg, sym))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, sym):
    req_msg = str(
        '{"MessageType":"SubscribeRealtime","Exchange":"' + exg + '","Unsubscribe":"false","InstrumentIdentifier":"' + sym + '"}')
    await ws.send(req_msg)
    rmsg = await get_msg(ws)
    return rmsg


async def mass_unsubscribe_n_stream(ws, exg, sym):
    req_msg = str(
        '{"MessageType":"SubscribeRealtime","Exchange":"' + exg + '","Unsubscribe":"true","InstrumentIdentifier":"' + sym + '"}')
    print("Request : " + req_msg)
    await ws.send(req_msg)
    rmsg = await get_msg(ws)
    return rmsg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'RealtimeResult':
                return message
        except websockets.ConnectionClosedOK:
            break
