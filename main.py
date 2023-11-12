import requests
import json
import time

token = "c1598721c1598721c159872141c12b806acc159c15987219f9a265511f76681353f3a40"
gid = "rolecon"
fld = "sex, bdate"
vers = 5.154
payload = {'access_token': token,
           'group_id': gid,
           'fields': fld,
           'offset': 0,
           'v': vers
          }

members = []
print(type(members))
end_of_members_flag = False
offset = 1000
while not end_of_members_flag:
    r = requests.get("https://api.vk.com/method/groups.getMembers", params=payload).text
    data_dict = json.loads(r)
    members += data_dict["response"]["items"]
    if data_dict["response"]["next_from"] == "":
        end_of_members_flag = True
    else:
        payload["offset"] = offset
        offset += 1000
        #time.sleep(5)
    print(len(members))

print(data_dict)
print(data_dict["response"]["next_from"])
print(data_dict["response"]["items"][0]["id"])

# payload['start_from'] = data_dict["response"]["next_from"]
# r = requests.get("https://api.vk.com/method/groups.getMembers", params=payload).text
# data_dict = json.loads(r)
# print(data_dict["response"]["next_from"])
