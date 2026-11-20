from json import dumps

async def sendJsonToSocket(socket, json) -> None:
    print(f"Sent {socket.id}: {json}")
    await socket.send(dumps(json))