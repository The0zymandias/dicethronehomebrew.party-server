from websockets.asyncio.server import Server
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError, ConnectionClosed
import asyncio

from json import loads, JSONDecodeError

import roomManager
from utils import sendJsonToSocket

class Client:
    def __init__(self):
        pass

async def clientHandler(client) -> None:
    print(f"From {client.id}: connected to server")
    currentRoomName: str = ""
    try:
        async for message in client:
            print(f"From {client.id}: {message}")
            messageJson = None
            try: 
                messageJson = loads(message)
            except JSONDecodeError:
                await sendJsonToSocket(client, {
                    "head": "UNKOWN_MESSAGE",
                    "data": {}
                })
            else:
                if currentRoomName != "":
                    await roomManager.handleMessageFromClient(client, currentRoomName, messageJson)
                else:
                    if messageJson["head"] == "MAKE_ROOM":
                        currentRoomName = await roomManager.tryMakeNewRoom(client, messageJson)
                    elif messageJson["head"] == "JOIN_ROOM":
                        currentRoomName = await roomManager.tryJoinRoom(client, messageJson)
                    else:
                        pass

    except ConnectionClosed:
        print(f"From {client.id}: closing")
    except ConnectionClosedOK:
        print(f"From {client.id}: closing with status ok")
    except ConnectionClosedError as e:
        print(f"From {client.id}: closing with error {e.reason}")
    finally:
        if currentRoomName != "":
            roomManager.removeClientFromRoom(currentRoomName, client)
    
async def main() -> None:
    server: Server = await serve(clientHandler, "localhost", 8765, server_header="DICE")
    await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
