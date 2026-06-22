import asyncio
import websockets
import json

async def test():
    async with websockets.connect("ws://127.0.0.1:8000/ws/live/brazil_vs_france") as ws:

        print(await ws.recv())  # connected

        await ws.send(json.dumps({
            "minute": 23,
            "type": "goal",
            "team": "Brazil"
        }))

        print(await ws.recv())

asyncio.run(test())