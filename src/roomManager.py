from websockets.asyncio.server import ServerConnection

from classes import Room

from utils import sendJsonToSocket

activeRooms: dict[str, Room] = {}

async def tryMakeNewRoom(client, messageJson) -> str:
    roomName = messageJson["data"]["name"]
    roomPassword = messageJson["data"]["password"]
    if roomName not in activeRooms:
        activeRooms[roomName] = Room(roomName, roomPassword, client)
        await sendJsonToSocket(client, {
            "head": "MADE_ROOM",
            "data": {}
        })
        print("Made room, total rooms: " + str(len(activeRooms)))
        return roomName
    else:
        await sendJsonToSocket(client, {
            "head": "FAILED_MAKE_ROOM",
            "data": {
                "message": f"Room '{roomName}' already exists"
            }
        })
    

async def tryJoinRoom(client, messageJson) -> str:
    roomName = messageJson["data"]["name"]
    roomPassword = messageJson["data"]["password"]
    if roomName in activeRooms:
        if activeRooms[roomName].isPassword(roomPassword):
            activeRooms[roomName].addClient(client)
            await sendJsonToSocket(client, {
                "head": "JOINED_ROOM",
                "data": {}
            })
    else:
        await sendJsonToSocket(client, {
            "head": "FAILED_MAKE_ROOM",
            "data": {
                "message": f"'{roomName}' already exists"
            }
        })

async def handleMessageFromClient(client: ServerConnection, roomName: str, messageJson: dict):
    activeRooms[roomName].handleMessageFromClient(client, messageJson)

def removeClientFromRoom(roomName: str, client: ServerConnection):
    activeRooms[roomName].removeClient(client)
    if activeRooms[roomName].numClients() == 0:
        del activeRooms[roomName]
