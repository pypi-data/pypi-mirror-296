import asyncio
import websockets
import json
import errno
import os

url = None
key = None
exg = None
src =None
ity = None
prd = None
exp = None
otp = None
srp = None
oa = None


def get(ws, exchange,search, instrumenttype=None, product=None, expiry=None, optiontype=None, strikeprice=None, onlyactive=None):
    if exchange == "":
        return "Exchange is mandatory."
    else:
        exg = exchange
    if search == "":
        return "search is mandatory."
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
        oa = ''
    else:
        oa = onlyactive

    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, src, ity, prd, exp, otp, srp, oa))
    return rmsg


async def mass_subscribe_n_stream(ws, exg,src, ity, prd, exp, otp, srp, oa):
    try:
        req_msg = '{"MessageType":"GetInstrumentsOnSearch",'
        if exg is not None:
            req_msg = req_msg + '"Exchange":"' + exg + '"'
        if src is not None:
            req_msg = req_msg + ',"Search":"' + src + '"'
        if ity is not None:
            req_msg = req_msg + ',"InstrumentType":"' + ity + '"'
        if prd is not None:
            req_msg = req_msg + ',"Product":"' + prd + '"'
        if exp is not None:
            req_msg = req_msg + ',"Expiry":"' + exp + '"'
        if otp is not None:
            req_msg = req_msg + ',"OptionType":"' + otp + '"'
        if srp is not None:
            req_msg = req_msg + ',"StrikePrice":"' + srp + '"'
        if oa is not None:
            req_msg = req_msg + ',"onlyActive":"' + oa + '"'
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
            if rslt["MessageType"] == 'InstrumentsOnSearchResult':
                return message
        except websockets.ConnectionClosedOK:
            break
            return message