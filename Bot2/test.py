# import csv
# from csv import DictWriter

import numpy as np

# # list of column names 
# field_names = ['ID','NAME','RANK','ARTICLE','COUNTRY']

# # Dictionary
# # dict={'ID':6,'NAME':'William','RANK':5532,'ARTICLE':1,'COUNTRY':'UAE'}
# # Open your CSV file in append mode
# # Create a file object for this file
# allDataMembers = []
# with open('event.csv', "r", newline="") as f_object:
#     reader = csv.reader(f_object)
#     for row in reader:
#         print(row)
#         dataProxy = {}
#         dataProxy['ID']  =  row
#         allDataMembers.append(dataProxy)
# doubleUser = []
# with open('event.csv', 'a', encoding='UTF-8') as f_object:        
#     # for member in allDataMembers:
#     np_array = np.array(allDataMembers)
#     print(np_array)
    # item = 6
    # item_index = np.where(np_array==item)
    # print(len(item_index[0]))
        # print(member)
        # if member['ID'][0] == '6':
        #     doubleUser.append(member['ID'][0])
        #     continue
        # else:
        #     continue
#     if len(doubleUser) == 0:
#         dict={'ID':6,'NAME':'William','RANK':5532,'ARTICLE':1,'COUNTRY':'UAE'}
#         # Pass the file object and a list
#         # of column names to DictWriter()
#         # You will get a object of DictWriter
#         dictwriter_object = DictWriter(f_object, fieldnames=field_names,lineterminator="\n")
#         # #Pass the dictionary as an argument to the Writerow()
#         # print(dict)
#         dictwriter_object.writerow(dict)
#         # #Close the file object
#         f_object.close()

array = [1, 2, 1, 3, 4, 5, 1]
item = 6
np_array = np.array(array)
print(np_array)
item_index = np.where(np_array==item)
# Out: (array([0, 2, 6], dtype=int64),)
