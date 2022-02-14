print ("NGUYEN TUAN ANH")

import csv
from csv import DictWriter

import numpy as np
from telethon import errors
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

api_id = 17689891 #Enter Your 7 Digit Telegram API ID.
api_hash = 'fa93937e18d10ddb95441ad7cbb2813d'   #Enter Yor 32 Character API Hash
phone = '+84 973475967'   #Enter Your Mobilr Number With Country Code.
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

print('Fetching Members...')
all_participants = []
try:
    all_participants = client.get_participants(target_group, aggressive=True)
except errors.FloodWaitError as e:
    print('Flood wait for', e.seconds)

print('Saving In file...')
field_names = ['username','user_id','access_hash','name']

# Dictionary
# Open your CSV file in append mode
# Create a file object for this file
allDataMembers = []
doubleUser = []
with open('Myaccount.csv', "r", newline="") as f_object:
    reader = csv.reader(f_object)
    for row in reader:
        dataProxy = {}
        dataProxy['username']  =  row
        allDataMembers.append(dataProxy)
for user in allDataMembers:
    doubleUser.append(user['username'][0])
np_array = np.array(doubleUser)
with open('Myaccount.csv', 'a', encoding='UTF-8') as f_object:
    for user in all_participants:
        if user.username and user.username != '':
            item_index = np.where(np_array==user.username)
            if len(item_index[0]) == 0:
                dict={'username':user.username,'user_id':user.id,'access_hash':user.access_hash,'name':target_group.title}
                # Pass the file object and a list
                # of column names to DictWriter()
                # You will get a object of DictWriter
                dictwriter_object = DictWriter(f_object, fieldnames=field_names,lineterminator="\n")
                # #Pass the dictionary as an argument to the Writerow()
                dictwriter_object.writerow(dict)
                # #Close the file object
                # f_object.close()
print('Members scraped successfully.......')
