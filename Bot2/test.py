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
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, ChannelParticipantsSearch
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError, UsernameNotOccupiedError, UserChannelsTooMuchError, PhoneNumberBannedError, UsernameInvalidError, UserNotMutualContactError, UserBannedInChannelError, UserDeactivatedBanError, ChannelPrivateError
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest
import sys
import csv
import traceback
import time
import random
import pandas as pd

dataAPIs = []
allDataAPI = []
with open("Apikey.csv", encoding='UTF-8') as f:  #Enter your file name
    rowss = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rowss, None)
    for row in rowss:
        dataAPIs.append(row)
        dataAPI = {}
        dataAPI['api_id']  =  row[0]
        dataAPI['api_hash'] = row[1]
        dataAPI['phone'] = row[2]
        allDataAPI.append(dataAPI)
numberInput1 = []
numberInput2 = []

for dataAPI in allDataAPI:
    api_id = dataAPI['api_id']                           #enter here api_id 6305419
    api_hash = dataAPI['api_hash'] #Enter here api_hash id e48908e1e2c1cd9f1db222ce809f268e
    phone = dataAPI['phone']  #enter here phone number with country code +84 377200557
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
    with open("Scrapped.csv", encoding='UTF-8') as f:  #Enter your file name
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            allUser.append(row)
            user = {}
            user['username'] = row[0]
            user['user_id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            user['group'] = row[4]
            user['group_id'] = row[5]
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
        # n += 1
        # if n % 100 == 0:
        #     # time.sleep(60)
        #     break
        offset = 0
        limit = 10
        channel = target_group.username
        participants = client(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(user['username']), offset, limit,
            hash=0
        ))
        if participants.users:
            indexUser = 0
            url = "Scrapped.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Scrapped.csv", index=False)
            print("The user is already in the group...")
            time.sleep(random.randrange(1, 2))
            continue
        else:
            try:
                print("Adding {}".format(user['user_id']))
                indexUser = 0
                if mode == 1:
                    if user['username'] == "":
                        continue
                    user_to_add = client.get_input_entity(user['username'])
                elif mode == 2:
                    user_to_add = InputPeerUser(user['user_id'], user['access_hash'])
                else:
                    sys.exit("Invalid Mode Selected. Please Try Again.")
                client(InviteToChannelRequest(target_group_entity, [user_to_add]))

                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)

                print("Waiting for 60-90 Seconds...")
                time.sleep(random.randrange(60, 90))
            except PeerFloodError:
                n +=1
                print("Getting PeerFloodError from telegram. Script is stopping now. Please try again after some time.")
                print("Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                if n < 5:
                    indexUser = 0
                    url = "Scrapped.csv"
                    df = pd.read_csv(url)
                    df = df.drop([indexUser])
                    df.to_csv("Scrapped.csv", index=False)
                    continue
                else:
                    break
            except FloodWaitError:
                print("Getting FloodWaitError from telegram. Script is stopping now. Please try again after some time.")
                print("Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                break
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping.")
                indexUser = 0
                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)

                print("Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UsernameNotOccupiedError:
                indexUser = 0
                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)
                print("UsernameNotOccupiedError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UserChannelsTooMuchError:
                indexUser = 0
                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)
                print("UserChannelsTooMuchError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UsernameInvalidError:
                indexUser = 0
                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)
                print("UsernameInvalidError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UserNotMutualContactError:
                indexUser = 0
                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)
                print("UserNotMutualContactError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UserBannedInChannelError:
                indexUser = 0
                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)
                print("UserBannedInChannelError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UserDeactivatedBanError:
                indexUser = 0
                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)
                print("UserDeactivatedBanError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                break
            except PhoneNumberBannedError:
                # indexApi = dataAPIs.index([str(dataAPI['api_id']),str(dataAPI['api_hash']),str(dataAPI['phone'])])
                # urls = "Apikey.csv"
                # df = pd.read_csv(urls)
                # df = df.drop([indexApi])
                # df.to_csv("Apikey.csv", index=False)
                print("User Banned Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                break
            except ChannelPrivateError:
                print("The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it")
                break
            except:
                #indexUser = allUser.index([str(user['username']),str(user['user_id']),str(user['access_hash']),str(user['name']),str(user['group']),str(user['group_id'])])
                indexUser = 0
                url = "Scrapped.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Scrapped.csv", index=False)
                print("Unexpected Error")
                print("Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
