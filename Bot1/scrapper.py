print ("")
print ("++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++")
print ("+  ____                                    ____ _           _    _         + ")
print ("- / ___|  __ _ _ __ ___   ___  ___ _ __   / ___| |__   ___ | | _| |_   _   -  ")
print ("+ \___ \ / _` | '_ ` _ \ / _ \/ _ \ '__| | |   | '_ \ / _ \| |/ / | | |    + ")
print ("-  ___) | (_| | | | | | |  __/  __/ |    | |___| | | | (_) |   <| | |_| |  -  ")
print ("+ |____/ \__,_|_| |_| |_|\___|\___|_|     \____|_| |_|\___/|_|\_\_|\__, |  +  ")
print ("-                                                                  |___/   -  ")
print ("++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++")
print ("")

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.contacts import ResolveUsernameRequest
import csv
#6305419,e48908e1e2c1cd9f1db222ce809f268e,+84 377200557
api_id = 8487818 #Enter Your 7 Digit Telegram API ID. 6052768
api_hash = 'f7d32017b6954f9d342df1d474b56c12'   #Enter Yor 32 Character API Hash 904a955db8c7e2e02ac76299015a29ce
phone = '+84 364416627'   #Enter Your Mobilr Number With Country Code.776941851
client = TelegramClient(phone, api_id, api_hash)
async def main():
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'Hello !!!!')
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter verification code: '))

for u in client.get_participants('ufc_mma'):
    print(u.id, u.first_name, u.last_name, u.username)
# chats = []
# last_date = None
# chunk_size = 200
# groups=[]

# result = client(GetDialogsRequest(
#              offset_date=last_date,
#              offset_id=0,
#              offset_peer=InputPeerEmpty(),
#              limit=chunk_size,
#              hash = 0
#          ))
# chats.extend(result.chats)

# for chat in chats:
#     try:
#         if chat.megagroup== True:
#             groups.append(chat)
#     except:
#         continue

# print('From Which Group Yow Want To Scrap A Members:')
# i=0
# for g in groups:
#     print(str(i) + '- ' + g.title)
#     i+=1

# g_index = input("Please! Enter a Number: ")
# target_group=groups[int(g_index)]

# print('Fetching Members...')
# all_participants = []
# all_participants = client.get_participants(target_group, aggressive=True)

# print('Saving In file...')
# with open("Scrapped.csv","w",encoding='UTF-8') as f:#Enter your file name.
#     writer = csv.writer(f,delimiter=",",lineterminator="\n")
#     writer.writerow(['username','user_id', 'access_hash','name','group', 'group_id'])
#     for user in all_participants:
#         if user.username:
#             username= user.username
#         else:
#             username= ""
#         if user.first_name:
#             first_name= user.first_name
#         else:
#             first_name= ""
#         if user.last_name:
#             last_name= user.last_name
#         else:
#             last_name= ""
#         name= (first_name + ' ' + last_name).strip()
#         if username != '':
#             writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
# print('Members scraped successfully.......')