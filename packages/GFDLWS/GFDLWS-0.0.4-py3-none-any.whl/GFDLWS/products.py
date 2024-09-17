import asyncio
import websockets
import json

exg = None
ist = None


def get(ws,Exchange, InstrumentType=None):
    exg = Exchange
    ist = InstrumentType
    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, ist))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, ist):
    try:
        req_msg = '{"MessageType":"GetProducts","Exchange":"' + exg
        if ist is not None:
            req_msg = req_msg + '",InstrumentType":"' + ist

        req_msg = str(req_msg + '"}')
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
            if rslt["MessageType"] == 'ProductsResult':
                return message
        except websockets.ConnectionClosedOK:
            break