print ("NGUYEN TUAN ANH")

import asyncio
import csv
import random
import sys
import time
import traceback
from os import waitpid

import pandas as pd
from telethon.errors.rpcerrorlist import (AuthKeyDuplicatedError,
                                          ChannelPrivateError, FloodWaitError,
                                          PeerFloodError,
                                          PhoneNumberBannedError,
                                          UserBannedInChannelError,
                                          UserChannelsTooMuchError,
                                          UserDeactivatedBanError,
                                          UsernameInvalidError,
                                          UsernameNotOccupiedError,
                                          UserNotMutualContactError,
                                          UserPrivacyRestrictedError)
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import (GetParticipantsRequest,
                                            InviteToChannelRequest)
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import (ChannelParticipantsSearch, InputPeerChannel,
                               InputPeerEmpty, InputPeerUser)

dataAPIs = []
allDataAPI = []
dataProxys = []
allDataProxy = []
numberInput1 = []
numberInput2 = []
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

users = []
allUser = []
with open("Myaccount.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        allUser.append(row)
        user = {}
        user['username'] = row[0]
        users.append(user)
chats = []
last_date = None
chunk_size = 200
groups = []
try:
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
except asyncio.exceptions.CancelledError:
    print("Gather was cancelled!")
    client.disconnect()
except ConnectionError:
    print("Not connected")
    client.disconnect()
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

i = 0
if len(numberInput1) == 0:
    print('Choose a group to add members:')
    for group in groups:
        print(str(i) + '- ' + group.title)
        i += 1
    g_index = input("Enter a Number: ")
    numberInput1.append(groups[int(g_index)].title)
for group in groups:
    if group.title == numberInput1[0]:
        target_group = group

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
if len(numberInput2) == 0:
    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
    numberInput2.append(mode)
else:
    mode = numberInput2[0]
n = 0
for user in users:
    offset = 0
    limit = 10
    channel = target_group.username
    try:
        participants = client(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(user['username']), offset, limit,
            hash=0
        ))
    except asyncio.exceptions.CancelledError:
        print("Gather was cancelled!")

        client.disconnect()
        break
    except ConnectionError:
        print("Not connected")
        client.disconnect()
        break
    if participants.users:
        indexUser = 0
        url = "Myaccount.csv"
        df = pd.read_csv(url)
        df = df.drop([indexUser])
        df.to_csv("Myaccount.csv", index=False)
        print("The user is already in the group...")
        time.sleep(random.randrange(1, 2))
        continue
    else:
        try:
            indexUser = 0
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            else:
                sys.exit("Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)

            print("Waiting for 60-90 Seconds...")
            time.sleep(random.randrange(60, 70))
        except PeerFloodError:
            n +=1
            print("Getting PeerFloodError from telegram. Script is stopping now. Please try again after some time.")
            print("Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
            if n < 5:
                indexUser = 0
                url = "Myaccount.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Myaccount.csv", index=False)
                continue
            else:
        
                client.disconnect()
                break
        except FloodWaitError:
            n +=1
            print("Getting FloodWaitError from telegram. Script is stopping now. Please try again after some time.")
            print("Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
            if n < 5:
                indexUser = 0
                url = "Myaccount.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Myaccount.csv", index=False)
                continue
            else:
        
                client.disconnect()
                break
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
            indexUser = 0
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)

            print("Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
            continue
        except UsernameNotOccupiedError:
            indexUser = 0
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)
            print("UsernameNotOccupiedError Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
            continue
        except UserChannelsTooMuchError:
            indexUser = 0
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)
            print("UserChannelsTooMuchError Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
            continue
        except UsernameInvalidError:
            indexUser = 0
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)
            print("UsernameInvalidError Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
            continue
        except UserNotMutualContactError:
            indexUser = 0
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)
            print("UserNotMutualContactError Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
            continue
        except UserBannedInChannelError:
            indexUser = 0
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)
            print("UserBannedInChannelError Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
    
            client.disconnect()
            break    
        except UserDeactivatedBanError:
            indexUser = 0
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)
            print("UserDeactivatedBanError Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
    
            client.disconnect()
            break
        except AuthKeyDuplicatedError:
            print("AuthKeyDuplicatedError Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
    
            client.disconnect()
            break
        except PhoneNumberBannedError:
            print("User Banned Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
    
            client.disconnect()
            break
        except ChannelPrivateError:
            print("The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it")
    
            client.disconnect()
            break
        except:
            indexUser = 0
            url = "Myaccount.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Myaccount.csv", index=False)
            print("Unexpected Error")
            print("Waiting for 1 Seconds...")
            time.sleep(random.randrange(1, 2))
    
            client.disconnect()
            break
