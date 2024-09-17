import asyncio
import websockets
import json

url = None
key = None
exg = None
sym = None
msg = None
prc = None
prd = None
frm = None
to = None
iss = None
rno = None
utg = None


def getbyperiod(ws, exchange, InstrumentIdentifier, periodicity, period, fromtime, totime, usertag, isShortIdentifiers):
    if exchange is None:
        return "Exchange is mandatory."
    else:
        exg = exchange

    if InstrumentIdentifier is None:
        return "InstrumentIdentifier / Symbol is mandatory."
    else:
        sym = InstrumentIdentifier

    if periodicity is None:
        prc = 'MINUTE'
    else:
        prc = periodicity

    if period is None:
        prd = '1'
    else:
        prd = period

    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_streamft(ws, exg, sym, prc, prd, fromtime, totime, isShortIdentifiers, usertag))
    return rmsg


def getcaldle(ws, exchange, InstrumentIdentifier, periodicity, period, max, usertag, isShortIdentifiers):
    if exchange is None:
        return "Exchange is mandatory."
    else:
        exg = exchange

    if InstrumentIdentifier is None:
        return "Symbol is mandatory."
    else:
        sym = InstrumentIdentifier

    if periodicity is None:
        prc = 'MINUTE'
    else:
        prc = periodicity

    if period is None:
        prd = '1'
    else:
        prd = period

    if max is None:
        rno = max
    else:
        rno = 10

    if isShortIdentifiers == "":
        iss = 'false'
    else:
        iss = isShortIdentifiers

    if usertag is None:
        utg = ''
    else:
        utg = usertag

    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, sym, prc, prd, iss, rno, utg))
    return rmsg


async def mass_subscribe_n_streamft(ws, exg, sym, prc, prd, frm, to, iss, utg):
    try:
        if iss != "" and utg != "":
            req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
                prd) + ',"From":"' + frm + '","To":"' + to + '","isShortIdentifier":"' + iss + '","UserTag":"' + utg + '"}'
        elif iss == "" and utg != "":
            req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
                prd) + ',"From":"' + frm + '","To":"' + to + '","isShortIdentifier":"false","UserTag":"' + utg + '"}'
        elif iss == "" and utg == "":
            req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
                prd) + ',"From":"' + frm + '","To":"' + to + '","isShortIdentifier":"false"}'
        elif iss != "" and utg == "":
            req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
                prd) + ',"From":"' + frm + '","To":"' + to + '","isShortIdentifier":"' + iss + '"}'
        await ws.send(req_msg)
        print("Request : " + req_msg)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return msg


async def mass_subscribe_n_stream(ws, exg, sym, prc, prd, iss, rno, utg):
    req_msg = None
    try:
        if iss != "" and utg != "":
            req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
                prd) + ',"Max":' + str(rno) + ',"isShortIdentifier":"' + iss + '","UserTag":"' + utg + '"} '
        elif iss != "" and utg == "":
            req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
                prd) + ',"Max":' + str(rno) + ',"isShortIdentifier":"' + iss + '"}'
        elif iss == "" and utg == "":
            req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
                prd) + ',"Max":' + str(rno) + ',"isShortIdentifier":"false"' + '"}'
        elif iss == "" and utg != "":
            req_msg = '{"MessageType":"GetHistory","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym + '","Periodicity":"' + prc + '","Period":' + str(
                prd) + ',"Max":' + str(rno) + ',"isShortIdentifier":"false"' + '","UserTag":"' + utg + '"}'
        await ws.send(str(req_msg))
        print("Request : " + req_msg)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return "Exception : " + str(msg)


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'HistoryOHLCResult' or rslt["MessageType"] == 'HistoryTickResult':
                return message
        except websockets.ConnectionClosedOK:
            break
        # print(message)
