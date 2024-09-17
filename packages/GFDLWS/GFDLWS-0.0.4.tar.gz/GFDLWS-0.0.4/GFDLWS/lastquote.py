import asyncio
import websockets
import json

exg = None
sym = None
msg = None
ws = None


def get(ws, exchange, symbol, isShortIdentifier):
    exg = exchange
    sym = symbol
    isi = isShortIdentifier
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym, isi))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, sym, isi):
    try:
        req_msg = str(
            '{"MessageType":"GetLastQuote","Exchange":"' + exg + '","isShortIdentifier":"' + isi + '","InstrumentIdentifier":"' + sym + '"}')
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
            if rslt["MessageType"] == 'LastQuoteResult':
                return message
        except websockets.ConnectionClosedOK:
            break
        #return message
