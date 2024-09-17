import asyncio
import websockets
import json

url = None
key = None
exg = None
sym = None
msg = None
ity = None

exp = None
otp = None
srp = None
oa = None
dth =None
printed_once = False

def get(ws, exchange,product,expiry, strikeprice,depth,optiontype=None, Unsubscribe=None):
    exg = exchange
    sym = product
    exp= expiry
    srp = strikeprice
    ity = optiontype
    dth =depth
    
    rmsg = asyncio.get_event_loop().run_until_complete(mass_subscribe_n_stream(ws, exg, sym,exp,srp,ity,dth))
    return rmsg


def stop(ws, exchange, product,expiry, strikeprice,depth,optiontype=None, Unsubscribe=None):
    exg = exchange
    sym = product
    exp= expiry
    srp = strikeprice
    ity = optiontype
    dth =depth
    rmsg = asyncio.get_event_loop().run_until_complete(mass_unsubscribe_n_stream(ws, exg, sym,exp,srp,ity,dth))
    return rmsg


async def mass_subscribe_n_stream(ws, exg, sym,exp,srp,ity,dth):
    global  printed_once
    req_msg = str(
        '{"MessageType":"SubscribeOptionChainGreeks","Exchange":"' + exg + '","Unsubscribe":"false","Product":"' + sym + '","Expiry":"' + exp + '","StrikePrice":"' + srp + '","OptionType":"' + ity + '","Depth":"' + dth + '"}')
    await ws.send(req_msg)
    if not printed_once:
        print("Request : " + req_msg)
        printed_once = True
    rmsg = await get_msg(ws)
    return rmsg


async def mass_unsubscribe_n_stream(ws, exg, sym,exp,srp,ity,dth):
    global printed_once
    req_msg = str(
        '{"MessageType":"SubscribeOptionChainGreeks","Exchange":"' + exg + '","Unsubscribe":"true","Product":"' + sym + '","Expiry":"' + exp + '","StrikePrice":"' + srp + '","OptionType":"' + ity + '","Depth":"' + dth + '"}')
    if not printed_once:
        print("Request : " + req_msg)
        printed_once = True
    await ws.send(req_msg)
    rmsg = await get_msg(ws)
    return rmsg


async def get_msg(ws):
    while True:
        try:
            message = await ws.recv()
            rslt = json.loads(message)
            if rslt["MessageType"] == 'RealtimeOptionChainGreeksResult':
                return message
        except websockets.ConnectionClosedOK:
            break
