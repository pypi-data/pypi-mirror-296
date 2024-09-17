import asyncio
import websockets
import json

exg = None


def get(ws, exchange, instrumenttype=None, product=None, expiry=None, optiontype=None):
    if exchange == "":
        return "Exchange is mandatory."
    else:
        exg = exchange
    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws, exg, instrumenttype, product, expiry, optiontype))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, ist, prd, exp, opt):
    try:
        req_msg = '{"MessageType":"GetStrikePrices", "Exchange":"' + exg + '"'
        if ist is not None:
            req_msg = req_msg + ',"InstrumentType":"' + ist + '"'
        if prd is not None:
            req_msg = req_msg + ',"Product":"' + prd + '"'
        if exp is not None:
            req_msg = req_msg + ',"Expiry":"' + exp + '"'

        req_msg = str(req_msg + '}')
        print("Request : " + req_msg)
        await ws.send(req_msg)
        rmsg = await get_msg(ws)
        return rmsg
    except:
        return "Error"


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'StrikePricesResult':
                return message
        except websockets.ConnectionClosedOK:
            break
