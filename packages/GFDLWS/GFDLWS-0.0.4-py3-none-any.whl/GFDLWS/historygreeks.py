import asyncio
import websockets
import json
import errno
import os

url = None
key = None
exg = None
prd = None
exp = None
otp = None
srp = None
oa = None

printed_once = False


def get(ws, exchange, InstrumentIdentifier, isShortIdentifier, max=None, From=None, To=None):
    if exchange == "":
        return "Exchange is mandatory."
    else:
        exg = exchange

    if InstrumentIdentifier == "":
        return "InstrumentIdentifier is mandatory."

    else:
        prd = InstrumentIdentifier

    if isShortIdentifier == "":
        return "isShortIdentifier is mandatory."

    else:
        exp = isShortIdentifier

    if max == "":
        otp = ''
    else:
        otp = max
    if From == "":
        srp = ''
    else:
        srp = From
    if To == "":
        oa = ''
    else:
        oa = To


    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, prd, exp, otp, srp, oa))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, prd, exp, otp, srp, oa):
    global printed_once
    try:
        req_msg = '{"MessageType":"GetHistoryGreeks",'
        if exg is not None:
            req_msg = req_msg + '"Exchange":"' + exg + '"'
        if prd is not None:
            req_msg = req_msg + ',"InstrumentIdentifier":"' + prd + '"'
        if exp is not None:
            req_msg = req_msg + ',"isShortIdentifier":"' + exp + '"'
        if otp is not None:
            req_msg = req_msg + ',"Max":"' +str(otp)  + '"'
        if srp is not None:
            req_msg = req_msg + ',"From":"' + str(srp) + '"'
        if oa is not None:
            req_msg = req_msg + ',"To":"' + str(oa) + '"'
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
            if rslt["MessageType"] == 'HistoryGreeksResult':
                return message
        except websockets.ConnectionClosedOK:
            break
