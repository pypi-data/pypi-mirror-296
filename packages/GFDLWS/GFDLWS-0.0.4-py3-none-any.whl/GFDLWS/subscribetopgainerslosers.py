import asyncio
import websockets
import json
import errno
import os

url = None
key = None
exg = None
src = None
ity = None
prd = None
exp = None
otp = None
srp = None
oa = None
dth = None
printed_once = False


def get(ws, exchange, Count, Unsubscribe=None):
    if exchange == "":
        return "Exchange is mandatory."
    else:
        exg = exchange

    if Count == "":
        return "product is mandatory."

    else:
        prd = Count

    if Unsubscribe == "":
        oa = ''
    else:
        oa = Unsubscribe

    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, prd, oa))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, prd, oa):
    global printed_once
    try:
        req_msg = '{"MessageType":"SubscribeTopGainersLosers",'
        if exg is not None:
            req_msg = req_msg + '"Exchange":"' + exg + '"'
        if prd is not None:
            req_msg = req_msg + ',"Count":"' + str(prd) + '"'

        if oa is not None:
            req_msg = req_msg + ',"Unsubscribe":"' + oa + '"'
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
            if rslt["MessageType"] == 'RealtimeGainersLosersResult':
                return message
        except websockets.ConnectionClosedOK:
            break
