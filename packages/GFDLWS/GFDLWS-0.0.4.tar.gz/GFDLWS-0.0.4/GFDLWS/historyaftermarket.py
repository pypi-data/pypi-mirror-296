import asyncio
import websockets
import json
import errno

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
rmsg = None


def get(endpoint, apikey, exchange, symbol, periodicity, period, fromtime, totime, isShortIdentifiers, recno, usertag):
    if endpoint is None:
        print("Endpoint is mandatory.")
    else:
        url = endpoint

    if apikey is None:
        print("APIkey is mandatory.")
    else:
        key = apikey

    if exchange is None:
        print("Exchange is mandatory.")
    else:
        exg = exchange

    if symbol is None:
        print("Symbol is mandatory.")
    else:
        sym = symbol

    if periodicity is None:
        prc = 'MINUTE'
    else:
        prc = periodicity

    if period is None:
        prd = '1'
    else:
        prd = period

    frm = fromtime
    to = totime

    rno = recno

    if isShortIdentifiers == "":
        iss = 'false'
    else:
        iss = isShortIdentifiers

    if usertag is None:
        utg = ' '
    else:
        utg = usertag

    print("iss : " + iss)

    asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(url, key, exg, sym, prc, prd, frm, to, iss, rno, utg))
    return


async def mass_subscribe_n_stream(url, key, exg, sym, prc, prd, frm, to, iss, rno, utg):
    try:
        ws = await asyncio.wait_for(websockets.connect(url), timeout=60)

        await authenticate(ws, key, exg, sym, prc, prd, frm, to, iss, rno, utg)
        await get_msg(ws)
    except:
        return msg


async def authenticate(ws, key, exg, sym, prc, prd, frm, to, iss, rno, utg):
    try:
        msg = 'Performing Authentication'
        print(msg)
        authentication_msg = json.dumps({
            "MessageType": "Authenticate",
            "Password": key
        })
        authenticated = False
        await ws.send(authentication_msg)
        while not authenticated:
            response = await ws.recv()
            response = json.loads(response)
            print(response)
            if response['MessageType'] == "AuthenticateResult":
                if response['Complete']:
                    rmsg = await subscribe_n_stream(ws, key, exg, sym, prc, prd, frm, to, iss, rno, utg)
                else:
                    await ws.send(authentication_msg)
        #msg = authenticated
        return rmsg
    except:
        return msg


async def subscribe_n_stream(ws, key, exg, sym, prc, prd, frm, to, iss, rno, utg):
    try:
        if frm != "" and to != "" and to != "" and rno != "" and utg != "":
            req_msg = str(
                '{"MessageType":"GetHistoryAfterMarket","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym
                + '","Periodicity":"' + prc + '","Period":"' + str(prd) + '","From":"' + frm + '","To":"' + to
                + '", "Max":"' + str(rno) + '","UserTag":"' + utg + '","isShortIdentifier":"' + iss + '"}')
        elif frm != "" and to != "" and to != "" and rno != "" and utg == "":
            req_msg = str(
                '{"MessageType":"GetHistoryAfterMarket","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym
                + '","Periodicity":"' + prc + '","Period":"' + str(prd) + '","From":"' + frm + '","To":"' + to
                + '", "Max":"' + str(rno) + '","isShortIdentifier":"' + iss + '"}')
            await ws.send(req_msg)
        elif frm != "" and to != "" and to != "" and rno == "" and utg == "":
            req_msg = str(
                '{"MessageType":"GetHistoryAfterMarket","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym
                + '","Periodicity":"' + prc + '","Period":"' + str(prd) + '","From":' + frm + ',"To":' + to
                + ',"isShortIdentifier":' + iss + '}')
            await ws.send(req_msg)
        elif frm != "" and to == "" and rno == "" and utg == "":
            req_msg = str(
                '{"MessageType":"GetHistoryAfterMarket","Exchange":"' + exg + '","InstrumentIdentifier":"' + sym
                + '","Periodicity":"' + prc + '","Period":' + str(prd) + ',"From":' + frm + '}')
            await ws.send(req_msg)
            print("Request : " + req_msg)
            rmsg = await get_msg(ws)
            return rmsg
    except:
        print(msg)
        return


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'HistoryOHLCResult' or rslt["MessageType"] == 'HistoryTickResult':
                return message
        except websockets.ConnectionClosedOK:
            break
