print ("")
print ("++++++---++++++++++++---++++++++++++---++++++++++++--")
print ("+               _________         ____        ")
print ("- |_\_\  |_|   |_________|       / /\_\       ")
print ("+ |_|\_\ |_|       |_|          /_/__\_\      ")
print ("- |_| \_\|_|       |_|         /_/____\_\     ")
print ("+ |_|  \_|_|       |_|        /_/      \_\    ")
print ("++++++---++++++++++++---++++++++++++---++++++++++++--")
print ("")

import asyncio
import csv
import random
import sys
import time
import traceback
from os import waitpid

import pandas as pd
import socks
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

with open("Proxy.csv", encoding='UTF-8') as f:  #Enter your file name
    rowss = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rowss, None)
    for row in rowss:
        dataProxys.append(row)
        dataProxy = {}
        dataProxy['proxy_id']  =  row[0]
        dataProxy['port'] = row[1]
        allDataProxy.append(dataProxy)

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
indexP=0
for dataAPI in allDataAPI:
    api_id = dataAPI['api_id']                           #enter here api_id 6305419
    api_hash = dataAPI['api_hash'] #Enter here api_hash id e48908e1e2c1cd9f1db222ce809f268e
    phone = dataAPI['phone']  #enter here phone number with country code +84 377200557
    # for dataProxy in allDataProxy:

    proxy = ('http', allDataProxy[indexP]['proxy_id'], int(allDataProxy[indexP]['port']), True)
    print(proxy)
    print(phone)
    # proxy = (socks.SOCKS5, '27.66.252.76', 1080, True)
    client = TelegramClient(phone, api_id, api_hash, proxy=proxy, connection_retries=0, auto_reconnect=True)
    # try:
    #     url = "Proxy.csv"
    #     df = pd.read_csv(url)
    #     df = df.drop([0])
    #     df.to_csv("Proxy.csv", index=False)
    #     client.start()
    # except OSError:
    #     # url = "Proxy.csv"
    #     # df = pd.read_csv(url)
    #     # df = df.drop([0])
    #     # df.to_csv("Proxy.csv", index=False)
    #     continue

    # async def main():
        # Now you can use all client methods listed below, like for example...
    try:
        # url = "Proxy.csv"
        # df = pd.read_csv(url)
        # df = df.drop([0])
        # df.to_csv("Proxy.csv", index=False)
        client.connect()
    except OSError:
        indexP+=1
        continue

    # client.loop.run_until_complete(main())
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
            user = {}
            user['username'] = row[0]
            user['user_id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
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
        indexP+=1
        client.disconnect()
        break
    except ConnectionError:
        print("Not connected")
        indexP+=1
        client.disconnect()
        break
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
        try:
            participants = client(GetParticipantsRequest(
                channel, ChannelParticipantsSearch(user['username']), offset, limit,
                hash=0
            ))
        except asyncio.exceptions.CancelledError:
            print("Gather was cancelled!")
            indexP+=1
            client.disconnect()
            break
        except ConnectionError:
            print("Not connected")
            indexP+=1
            client.disconnect()
            break
        if participants.users:
            indexUser = 0
            url = "Allmembers.csv"
            df = pd.read_csv(url)
            df = df.drop([indexUser])
            df.to_csv("Allmembers.csv", index=False)
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

                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)

                print("Waiting for 60-90 Seconds...")
                time.sleep(random.randrange(60, 70))
            except PeerFloodError:
                n +=1
                print("Getting PeerFloodError from telegram. Script is stopping now. Please try again after some time.")
                print("Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                if n < 5:
                    indexUser = 0
                    url = "Allmembers.csv"
                    df = pd.read_csv(url)
                    df = df.drop([indexUser])
                    df.to_csv("Allmembers.csv", index=False)
                    continue
                else:
                    # url = "Proxy.csv"
                    # df = pd.read_csv(url)
                    # df = df.drop([0])
                    # df.to_csv("Proxy.csv", index=False)
                    indexP+=1
                    client.disconnect()
                    break
            except FloodWaitError:
                n +=1
                print("Getting FloodWaitError from telegram. Script is stopping now. Please try again after some time.")
                print("Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                if n < 5:
                    indexUser = 0
                    url = "Allmembers.csv"
                    df = pd.read_csv(url)
                    df = df.drop([indexUser])
                    df.to_csv("Allmembers.csv", index=False)
                    continue
                else:
                    # url = "Proxy.csv"
                    # df = pd.read_csv(url)
                    # df = df.drop([0])
                    # df.to_csv("Proxy.csv", index=False)
                    indexP+=1
                    client.disconnect()
                    break
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping.")
                indexUser = 0
                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)

                print("Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UsernameNotOccupiedError:
                indexUser = 0
                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)
                print("UsernameNotOccupiedError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UserChannelsTooMuchError:
                indexUser = 0
                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)
                print("UserChannelsTooMuchError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UsernameInvalidError:
                indexUser = 0
                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)
                print("UsernameInvalidError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UserNotMutualContactError:
                indexUser = 0
                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)
                print("UserNotMutualContactError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                continue
            except UserBannedInChannelError:
                indexUser = 0
                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)
                print("UserBannedInChannelError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                indexP+=1
                client.disconnect()
                break    
            except UserDeactivatedBanError:
                # urls = "Proxy.csv"
                # df = pd.read_csv(urls)
                # df = df.drop([0])
                # df.to_csv("Proxy.csv", index=False)
                indexUser = 0
                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)
                print("UserDeactivatedBanError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                indexP+=1
                client.disconnect()
                break
            except AuthKeyDuplicatedError:
                print("AuthKeyDuplicatedError Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                indexP+=1
                client.disconnect()
                break
            except PhoneNumberBannedError:
                # url = "Proxy.csv"
                # df = pd.read_csv(url)
                # df = df.drop([0])
                # df.to_csv("Proxy.csv", index=False)
                # indexApi = dataAPIs.index([str(dataAPI['api_id']),str(dataAPI['api_hash']),str(dataAPI['phone'])])
                # urls = "Apikey.csv"
                # df = pd.read_csv(urls)
                # df = df.drop([indexApi])
                # df.to_csv("Apikey.csv", index=False)
                print("User Banned Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                indexP+=1
                client.disconnect()
                break
            except ChannelPrivateError:
                # url = "Proxy.csv"
                # df = pd.read_csv(url)
                # df = df.drop([0])
                # df.to_csv("Proxy.csv", index=False)
                print("The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it")
                indexP+=1
                client.disconnect()
                break
            except:
                #indexUser = allUser.index([str(user['username']),str(user['user_id']),str(user['access_hash']),str(user['name']),str(user['group']),str(user['group_id'])])url = "Proxy.csv"
                # urls = "Proxy.csv"
                # df = pd.read_csv(urls)
                # df = df.drop([0])
                # df.to_csv("Proxy.csv", index=False)
                indexUser = 0
                url = "Allmembers.csv"
                df = pd.read_csv(url)
                df = df.drop([indexUser])
                df.to_csv("Allmembers.csv", index=False)
                print("Unexpected Error")
                print("Waiting for 1 Seconds...")
                time.sleep(random.randrange(1, 2))
                indexP+=1
                client.disconnect()
                break
