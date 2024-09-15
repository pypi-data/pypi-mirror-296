from setuptools import setup

setup(name='tg_bot_sender',
      version='0.5',
      description='This lib for sending message to tg bots',
      packages=['tg_bot_sender'],
      author_email='poznkirill3@gmail.com',
      long_description="""
      [Link to the documentation](https://magnificent-maamoul-2f7a55.netlify.app/)
# Python
How to install ?
```pip
pip install tg-bot-sender
```
## Imports 
```python
from tg_bot_sender import Data, TelegramSender
```
## Getting started
The logs parameter indicates that logs are saved in json format
```python
tg = TelegramSender(telegramToken, logs = False)
```
Response structure
```json
{ "amount": 0 } // number of messages sent
```
## Options for sending messages
#### sendFromIds - sending to users
```python
tg.sendFromIds([...telegramUserIds], Data(
    text = 'Hello',
    photo = 'Photo link',
    buttons = [{
        buttonTitle: 'Hello',
        buttonUrl: 'https://google.com'
    }]
))
```
#### sendFromId - sending to the user
```python
tg.sendFromIds(telegramUserId, Data(
    text = 'Hello',
    photo = 'Photo link',
    buttons = [{
        buttonTitle: 'Hello',
        buttonUrl: 'https://google.com'
    }]
))
```

      """,
      long_description_content_type='text/markdown',
      zip_safe=False)