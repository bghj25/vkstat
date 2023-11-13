import requests
import json
import datetime
import data
import matplotlib.pyplot as plt


fld = "sex, bdate"
vers = 5.154
publics_data = {"Актуально на ": str(datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S"))}

for gid in data.gids:  # Указать в data.py список пабликов
    print(gid)
    payload = {'access_token': data.token,  # Указать в data.py токен
               'group_id': gid,
               'fields': fld,
               'offset': 0,
               'v': vers
               }

    members = []
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
            # time.sleep(5)


    male = 0
    female = 0
    today = datetime.date.today()

    ages = {}
    ful_date = 0
    half_date = 0
    no_date = 0
    for member in members:
        if member["sex"] == 1:
            female += 1
        elif member["sex"] == 2:
            male += 1

        try:
            bd = member["bdate"].split(".")
            if len(bd) == 3:
                birthday = datetime.date(int(bd[2]), int(bd[1]), int(bd[1]))
                ful_date += 1
                try:
                    ages[(today - birthday).days // 365] += 1
                except KeyError:
                    ages[(today - birthday).days // 365] = 1
            else:
                half_date += 1
                # if (today - birthday).days // 365 == 122:
                #     print("vk.com/id{}".format(member["id"]))
                # print((today - birthday).days // 365)
        except KeyError:
            no_date += 1
            pass

    sorted_ages = dict(sorted(ages.items()))



    #print(ages)

    # plt.bar(range(len(sorted_ages)), list(sorted_ages.values()), align='center')
    # plt.xticks(range(len(sorted_ages)), list(sorted_ages.keys()), rotation=90)
    # plt.show()

    # print(sorted_ages)
    publics_data[gid] = {"Всего подписчиков: ": len(members),
                         "Из них мужчины: ": male,
                         "Из них женщины: ": female,
                         "Неопределившихся: ": len(members) - male - female,
                         "Возрастная характеристика: ": {"Не указана дата рождения: ": no_date,
                                                         "Частично указана дата рождения:": half_date,
                                                         "Полностью дата рождения:": ful_date,
                                                         "Статистика по возрастам(на основании {}"
                                                         " человек с полной датой".format(ful_date): sorted_ages}
                         }


with open("sample.json", "w") as outfile:
    json.dump(publics_data, outfile, ensure_ascii=False, indent=4)
