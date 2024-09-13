import asyncio
import websockets
from datetime import datetime
import json
import time
import errno

url = None
key = None
src = None
exg = None
ity = None
prd = None
exp = None
otp = None
srp = None
oa = None


def get(ws, exchange, search, instrumenttype=None, product=None, expiry=None, optiontype=None, strikeprice=None,
        onlyactive=None):

    if exchange == "":
        return "Exchange is mandatory."
    else:
        exg = exchange

    if search == "":
        return "Search is mandatory."
    else:
        src = search

    if instrumenttype == "":
        ity = ''
    else:
        ity = instrumenttype

    if product == "":
        prd = ''
    else:
        prd = product

    if expiry == "":
        exp = ''
    else:
        exp = expiry

    if optiontype == "":
        otp = ''
    else:
        otp = optiontype

    if strikeprice == "":
        srp = ''
    else:
        srp = strikeprice

    if onlyactive == "":
        oa = 'true'
    else:
        oa = onlyactive

    asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, src, ity, prd, exp, otp, srp, oa))
    return


async def mass_subscribe_n_stream(ws, exg, src, ity, prd, exp, otp, srp, oa):
    try:
        req_msg = '{"MessageType":"GetInstrumentsOnSearch",'
        if exg != None:
            req_msg = str(req_msg) + '"Exchange":"' + exg + '"'
        if src != None:
            req_msg = str(req_msg) + ',"Search":"' + src + '"'
        if ity != None:
            req_msg = str(req_msg) + ',"InstrumentType":"' + ity + '"'
        if prd != None:
            req_msg = str(req_msg) + ',"Product":"' + prd + '"'
        if exp != None:
            req_msg = str(req_msg) + ',"Expiry":"' + exp + '"'
        if otp != None:
            req_msg = str(req_msg) + ',"optionType":"' + otp + '"'
        if srp != None:
            req_msg = str(req_msg) + ',"strikePrice":"' + srp + '"'
        if oa != None:
            req_msg = str(req_msg) + ',"onlyActive":"' + oa + '"'
        req_msg = str(req_msg + '}')
        print('Request : ' + req_msg)
        await ws.send(req_msg)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return 'In Exception...' + errno


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'InstrumentsOnSearchResult':
                return message
        except websockets.ConnectionClosedOK:
            break
