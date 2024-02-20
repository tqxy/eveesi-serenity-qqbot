import botpy
import requests
import json
from datetime import timezone,timedelta
import datetime
from botpy.message import Message
def request_status():
    url = "https://ali-esi.evepc.163.com/legacy/status/"
    response = requests.get(url).content
    dic=json.loads(response)
    players_count=dic['players']
    server_version=dic['server_version']
    T=dic['start_time'][0:10]
    Z=dic['start_time'][11:19]
    start_time=T+' '+Z
    #字符串合并
    start_time=datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    utc=timezone.utc
    utc_time = start_time.replace(tzinfo=utc)
    start_time = utc_time.astimezone(timezone(timedelta(hours=8)))
    #+8时区开服时间已处理完毕
    return '晨曦在线人数：'+str(players_count)+'，服务器版本号：'+str(server_version)+'，开服时间：'+str(start_time)+'，播报完毕'
def request_jita(type):
    url="https://ali-esi.evepc.163.com/legacy/markets/10000002/orders/"
    params = {'order_type': 'all','region_id': '10000002','type_id':request_typeid(type)}
    response = requests.get(url, data=params)
    return str(response.json())
def request_typeid(type):
    url="https://ali-esi.evepc.163.com/legacy/universe/ids/"
    params={'datasource':'serenity','language':'zh'}
    body= {'names':'[%s%s%s]' % ("\"", type, "\"")}
    print(params)
    #print(body)
    #print(json.dumps(body,ensure_ascii=False))
    response=requests.post(url,data=body, params=params).content
    dic=json.loads(response)
    print(dic)
    typeid=dic['inventory_types'][0]['id']
    return typeid
class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="收到你的消息了，爱你！")
    async def on_message_create(self, message: Message):
        if message.content[0:6] == "status":
            await self.api.post_message(channel_id=message.channel_id, content=request_status())
        if message.content[0:4] == "jita":
            type=message.content[5:]
            await self.api.post_message(channel_id=message.channel_id, content=request_jita(type))
        else:
            await self.api.post_message(channel_id=message.channel_id, content=message.content)

intents = botpy.Intents(public_guild_messages=True,guild_messages=True)
client = MyClient(intents=intents)
client.run(appid="102092477",secret="9YxNnDd3TtJjAb2TuLmDf7Z1TvNpHkDg")
