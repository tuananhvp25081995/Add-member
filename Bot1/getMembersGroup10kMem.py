import csv
from time import sleep

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputPeerEmpty

api_id = 17689891 #Enter Your 7 Digit Telegram API ID.
api_hash = 'fa93937e18d10ddb95441ad7cbb2813d'   #Enter Yor 32 Character API Hash
phone = '+84 973475967'   #Enter Your Mobilr Number With Country Code.
# proxy = ('http', '176.88.6.235', 8080, True)
client = TelegramClient(phone, api_id, api_hash)
async def main():
    # Now you can use all client methods listed below, like for example...
    with client:
        client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter verification code: '))


chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('From Which Group Yow Want To Scrap A Members:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Please! Enter a Number: ")
target_group=groups[int(g_index)]
channel = target_group.username
group_name = target_group.title
offset = 0
limit = 100
all_participants = []
while True:
    participants = client(GetParticipantsRequest(
        channel,
        ChannelParticipantsSearch(''),
        offset,
        limit,
        hash=0
    ))
    if not participants.users:
        break
    all_participants.extend(participants.users)
    offset += len(participants.users)
    sleep(5)
with open("Scrapped.csv","w",encoding='UTF-8') as f:#Enter your file name.
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user_id', 'access_hash','name'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        if username != '':
            writer.writerow([username,user.id,user.access_hash,name])
print('Members scraped successfully.......')