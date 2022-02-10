from time import sleep

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

api_id = 17689891 #Enter Your 7 Digit Telegram API ID.
api_hash = 'fa93937e18d10ddb95441ad7cbb2813d'   #Enter Yor 32 Character API Hash
phone = '+84 973475967'   #Enter Your Mobilr Number With Country Code.
proxy = ('http', '176.88.6.235', 8080, True)
client = TelegramClient(phone, api_id, api_hash)

offset = 0
limit = 100
all_participants = []

while True:
    participants = client(GetParticipantsRequest(
         ChannelParticipantsSearch(''), offset, limit,
        hash=0
    ))
    if not participants.users:
        break
    all_participants.extend(participants.users)
    offset += len(participants.users)
print(all_participants)
