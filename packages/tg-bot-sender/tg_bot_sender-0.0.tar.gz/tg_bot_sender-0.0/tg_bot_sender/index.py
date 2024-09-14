import time
import asyncio
import aiohttp
from .module.saveFile import saveFile
from .module.sendMessage import sendMessage, Data
from .module.conf import DIVIDER_AMOUNT

class TelegramSender():
    def __init__(self, token, logs = False):
        self.token = token
        self.loop = asyncio.get_event_loop()
        self.logs = logs
        
    def groupUser(self, idsArray):
        return [idsArray[d:d+DIVIDER_AMOUNT] for d in range(0, len(idsArray), DIVIDER_AMOUNT)]
    
    def saveExecuter(self, gatherTasks):
        if self.logs:
            return saveFile(str(round(time.time())), gatherTasks)
    
    async def sendFromIds(self, idsArray, data: Data):
        slicedIdArray = self.groupUser(idsArray)
        
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

    async def sendFromId(self, id, data: Data):
        async with aiohttp.ClientSession(loop=self.loop,connector=aiohttp.TCPConnector(ssl=False),trust_env=True) as session:
            print('LOG: start sending')
            data = await asyncio.create_task(sendMessage(session, id, data, self.token))
            self.saveExecuter(data)
            print('LOG: end sending')

            


if __name__=='__main__':
    loop=asyncio.get_event_loop()
    tg = TelegramSender('*')
    
    startTime = time.time()
    loop.run_until_complete(tg.sendFromId('*', Data(text='Hello')))
    loop.run_until_complete(tg.sendFromIds(['*', '*', '*'], Data(text='Hello')))
    print(f'LOG: time {time.time() - startTime}')
