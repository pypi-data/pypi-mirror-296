import asyncio
import websockets
import json

exg = None
tkn = None
msg = None
ws = None


def get(ws, exchange, token):
    exg = exchange
    tkn = token
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, tkn))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, tkn):
    try:
        req_msg = str(
            '{"MessageType":"GetLastQuoteOptionGreeks","Exchange":"' + exg + '","Token":"' + tkn + '"}')
        print("Request : " + req_msg)
        await ws.send(req_msg)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return msg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'LastQuoteOptionGreeksResult':
                return message
        except websockets.ConnectionClosedOK:
            break
        print(message)
