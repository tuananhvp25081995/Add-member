import csv
from time import sleep

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

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
offset = 0
limit = 100
all_participants = []

while True:
    participants = client(GetParticipantsRequest(
        'MrCryptoXCommunity',
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
print(len(all_participants))
with open("Scrapped.csv","w",encoding='UTF-8') as f:#Enter your file name.
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user_id', 'access_hash','name','group', 'group_id'])
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
            writer.writerow([username,user.id,user.access_hash,name,"1", "2"])
print('Members scraped successfully.......')
