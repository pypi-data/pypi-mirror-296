import asyncio
import websockets
import json
import errno
import os

url = None
key = None
exg = None
dth = None
printed_once = False


def get(ws, exchange, Count):
    if exchange == "":
        return "Exchange is mandatory."
    else:
        exg = exchange

    if Count == "":
        return "product is mandatory."

    else:
        prd = Count

    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, prd))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, prd):
    global printed_once
    try:
        req_msg = '{"MessageType":"GetTopGainersLosers",'
        if exg is not None:
            req_msg = req_msg + '"Exchange":"' + exg + '"'
        if prd is not None:
            req_msg = req_msg + ',"Count":"' + str(prd) + '"'
        req_msg = str(req_msg + '}')
        if not printed_once:
            print("Request : " + req_msg)
            printed_once = True
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
            if rslt["MessageType"] == 'LastQuoteArrayResult':
                return message
        except websockets.ConnectionClosedOK:
            break
