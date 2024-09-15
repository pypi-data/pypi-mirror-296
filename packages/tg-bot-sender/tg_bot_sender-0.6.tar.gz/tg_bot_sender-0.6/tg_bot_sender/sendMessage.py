import json
import asyncio
from typing import TypedDict, List, Dict, Union, Awaitable, Any
from aiogram import  types
from tg_bot_sender.conf import TELEGRAM_API_URL

class Button(TypedDict):
    buttonTitle: str
    buttonUrl: str
    
class Data(TypedDict):
    photo: str
    text: str
    buttons: List[Button]
    
async def sendMessage(session, user: int, pushData: Data, token: str) -> Awaitable[Any]:
    url: str = f"{TELEGRAM_API_URL}{token}/"
    data: Dict[str, Union[str, int]] = {
        "chat_id": user,
        'parse_mode': types.ParseMode.HTML,
    }
 
    if pushData.get('photo', None):
        data['caption'] = pushData.get('caption','')
        data['photo'] = pushData.get('photo', '')
        url += 'sendPhoto'
    else: 
        data['text'] = pushData.get('text','')
        url += 'sendMessage'

    if pushData.get('buttons',None):
        res = { "inline_keyboard": [] }
        for button in pushData.get('buttons',None):
            res.get('inline_keyboard').append([{
                "text": button["buttonTitle"], 
                "url": button["buttonUrl"],
            }])
       
        data['reply_markup'] = json.dumps(res)


    async with session.post(url, data=data, ssl=False) as response:
        await asyncio.sleep(1)
        return await response.json()
    
if __name__ == '__main__':
    pass