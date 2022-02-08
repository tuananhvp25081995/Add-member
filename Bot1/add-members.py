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
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv  
import traceback
import time
import random
import pandas as pd

api_id = 6305419                           #enter here api_id 6305419
api_hash = 'e48908e1e2c1cd9f1db222ce809f268e' #Enter here api_hash id e48908e1e2c1cd9f1db222ce809f268e
phone = '+84 377200557'  #enter here phone number with country code +84 377200557
client = TelegramClient(phone, api_id, api_hash).start()
async def main():
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'Hello !!!!!')


SLEEP_TIME_1 = 100
SLEEP_TIME_2 = 100
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

users = []
allUser = []
with open("Allmembers.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        allUser.append(row)
        if row[6] != 'True':
            user = {}
            user['username'] = row[0]
            user['user_id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            user['group'] = row[4]
            user['group_id'] = row[5]
            user['added'] = row[6]
            users.append(user)
chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

i = 0
print('Choose a group to add members:')
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1
g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]
n=0
target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
for user in users:
    n += 1
    if n % 80 == 0:
        # time.sleep(60)
        break
    try:
        print("Adding {}".format(user['user_id']))
        indexUser = allUser.index([user['username'],str(user['user_id']),str(user['access_hash']),user['name'],user['group'],user['group_id'],user['added']])
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['user_id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))

        # reading the csv file
        df = pd.read_csv("Allmembers.csv")
        
        # updating the column value/data
        df.loc[indexUser, 'added'] = 'True'
        
        # writing into the file
        df.to_csv("Allmembers.csv", index=False)

        print("Waiting for 60-90 Seconds...")
        time.sleep(random.randrange(60, 90))
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        # print("Waiting {} seconds".format(SLEEP_TIME_2))
        break
        # time.sleep(SLEEP_TIME_2)
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
        print("Waiting for 5 Seconds...")
        time.sleep(random.randrange(5, 10))
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue
