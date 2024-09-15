import time
import asyncio
import aiohttp
from typing import List, TypedDict, Awaitable
from tg_bot_sender.saveFile import saveFile
from tg_bot_sender.sendMessage import sendMessage, Data
from tg_bot_sender.conf import DIVIDER_AMOUNT

class Response(TypedDict):
    amount: str
class TelegramSender():
    def __init__(self, token, logs = False):
        self.token = token
        self.loop = asyncio.get_event_loop()
        self.logs = logs
        
    def groupUser(self, idsArray) -> List[List[int]]:
        return [idsArray[d:d+DIVIDER_AMOUNT] for d in range(0, len(idsArray), DIVIDER_AMOUNT)]
    
    def saveExecuter(self, gatherTasks) -> None:
        if self.logs:
            return saveFile(str(round(time.time())), gatherTasks)
    
    async def sendFromIds(self, idsArray: List[int], data: Data) -> Awaitable[Response]:
        slicedIdArray = self.groupUser(idsArray)
        tasks = []
        for idArray in slicedIdArray:
            async with aiohttp.ClientSession(loop=self.loop,connector=aiohttp.TCPConnector(ssl=False),trust_env=True) as session:
                print('LOG: start sending')
                tasks = [
                    asyncio.create_task(
                        sendMessage(session, userId, data, self.token)) for userId in idArray
                ]
                gatherTasks = await asyncio.gather(*tasks)
                self.saveExecuter(gatherTasks)
                print('LOG: end sending')
                
        return Response(amount=len(gatherTasks))

    async def sendFromId(self, id: int, data: Data) -> Awaitable[Response]:
        async with aiohttp.ClientSession(loop=self.loop,connector=aiohttp.TCPConnector(ssl=False),trust_env=True) as session:
            print('LOG: start sending')
            data = await asyncio.create_task(sendMessage(session, id, data, self.token))
            self.saveExecuter(data)
            print('LOG: end sending')
            return Response(amount=1)
            


if __name__=='__main__':
    loop=asyncio.get_event_loop()
    tg = TelegramSender('*')
    
    startTime = time.time()
    data = loop.run_until_complete(tg.sendFromId('*', Data(text='Hello')))
    d = loop.run_until_complete(tg.sendFromIds(['*', '*', '*'], Data(text='Hello')))
    print(f'LOG: time {time.time() - startTime}')
