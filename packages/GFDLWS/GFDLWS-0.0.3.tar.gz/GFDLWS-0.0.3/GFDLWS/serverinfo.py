import asyncio
import websockets
import json


def get(ws):
    rmsg = asyncio.get_event_loop().run_until_complete(
        mass_subscribe_n_stream(ws))
    return rmsg


async def mass_subscribe_n_stream(ws):
    try:
        req_msg = str('{"MessageType":"GetServerInfo"}')
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
            if rslt["MessageType"] == 'ServerInfoResult':
                return message
        except websockets.ConnectionClosedOK:
            break
