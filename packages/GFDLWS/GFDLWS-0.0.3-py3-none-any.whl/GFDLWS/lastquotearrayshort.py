import asyncio
import websockets
import json

exg = None
sym = None
msg = None
isi = None


def get(ws, exchange, symbols,isShortIdentifiers):
    exg = exchange
    sym = symbols
    isi = isShortIdentifiers
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, sym, isi):
    try:
        req_msg = str('{"MessageType":"GetLastQuoteArrayShort","Exchange":"' + exg + '","isShortIdentifiers":"' + isi + '","InstrumentIdentifiers":' + str(sym) + '}')
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
            if rslt["MessageType"] == 'LastQuoteArrayShortResult':
                return message
        except websockets.ConnectionClosedOK:
            break