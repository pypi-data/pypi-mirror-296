import asyncio
import websockets
import json
import errno
import os

url = None
key = None
exg = None


def get(ws, exchange, instrumenttype=None, product=None):
    if exchange == "":
        print("Exchange is mandatory.")
    else:
        exg = exchange

    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg,instrumenttype, product))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, ist, prd):
    try:
        req_msg = '{"MessageType":"GetExpiryDates","Exchange":"' + exg + '"'
        if ist is not None:
            req_msg = req_msg + '"InstrumentType":"' + ist + '"'
        if prd is not None:
            req_msg = req_msg + '"Product":"' + prd + '"'
        req_msg = str(req_msg + '}')
        print("Request : " + req_msg)
        await ws.send(req_msg)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return 'In Exception...' + os.error


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'ExpiryDatesResult':
                return message
        except websockets.ConnectionClosedOK:
            break
        print(message)
