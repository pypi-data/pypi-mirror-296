import asyncio
import websockets
import json

url = None
key = None
exg = None
tkn = None
msg = None


def get(ws, exchange, token):
    exg = exchange
    tkn = token
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, tkn))
    return rmsg


def stop(ws, exchange, token):
    exg = exchange
    tkn = token
    asyncio.get_event_loop().run_until_complete(mass_unsubscribe_n_stream(ws, exg, tkn))
    return


async def mass_subscribe_n_stream(ws, exg, tkn):
    req_msg = str('{"MessageType":"SubscribeRealtimeGreeks","Exchange":"' + exg + '","Unsubscribe":"false","Token":"' + tkn + '"}')
    await ws.send(req_msg)
    rmsg = await get_msg(ws)
    return rmsg


async def mass_unsubscribe_n_stream(ws, exg, sym):
    req_msg = str('{"MessageType":"SubscribeRealtimeGreeks","Exchange":"' + exg + '","Unsubscribe":"true","Token":"' + tkn + '"}')
    print("Request : " + req_msg)
    await ws.send(req_msg)
    rmsg = await get_msg(ws)
    return rmsg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'SubscribeRealtimeGreeks':
                return message
        except websockets.ConnectionClosedOK:
            break