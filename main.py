import botpy
import requests
import json
import jsonpath
from botpy.message import Message
def request_status():
    url = "https://ali-esi.evepc.163.com/legacy/status/"
    response = requests.get(url)
    return str(response.json())
def request_jita():
    url="https://ali-esi.evepc.163.com/legacy/markets/10000002/orders/"
    params = {'order_type': 'all','region_id': '10000002'}
    response=requests.get(url, data=params)
    return str(response.json())
class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="收到你的消息了，爱你！")
    async def on_message_create(self, message: Message):
        if message.content[0:6] == "status":
            await self.api.post_message(channel_id=message.channel_id, content=request_status())
        if message.content[0:4]=="jita":
            await self.api.post_message(channel_id=message.channel_id, content=request_jita())
        else:
            await self.api.post_message(channel_id=message.channel_id, content=message.content)
intents = botpy.Intents(public_guild_messages=True,guild_messages=True)
client = MyClient(intents=intents)
client.run(appid="102092477",secret="9YxNnDd3TtJjAb2TuLmDf7Z1TvNpHkDg")
