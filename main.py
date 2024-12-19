from bs4 import BeautifulSoup
from bs4 import Tag
import requests
import json

URL = "https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2"

response = requests.get(URL)

if response.status_code != 200:
    print(f"Ошибка при запросе к сайту: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

teachers = soup.find_all('h3')
posts = soup.find_all('li', class_ = 'tss')

data_json = []
for i in range(0, len(teachers)):
    d = {
        "id":i+1,
        "Преподаватель": teachers[i].text,
        "Должность": posts[i].text
    }
    data_json.append(d)

with open('data.json','w',encoding='UTF-8') as file:
    json.dump(data_json, file, ensure_ascii = False, indent=4)

with open('data.json','r',encoding='UTF-8') as file:
    data = json.load(file)

with open('index.html','r',encoding='UTF-8') as file:
    filedata = file.read()

soup = BeautifulSoup(filedata, "html.parser")

paste = soup.find("div", class_="new_table")

table = Tag(name = "table")

thead = Tag(name = "thead")
tr = Tag(name = "tr")

heads = ["№", "Преподаватель", "Должность"]
for head in heads:
    th = Tag(soup, name="th")
    th.string = head
    tr.append(th)

thead.append(tr)
table.append(thead)

tbody = Tag(name="tbody")
for teacher in data:
    tr2 = Tag(name = "tr")

    td1 = Tag(name = "td")
    td1.string = str(teacher["id"])
    tr2.append(td1)

    td2 = Tag(name = "td")
    td2.string = teacher["Преподаватель"]
    tr2.append(td2)

    td3 = Tag(name = "td")
    td3.string = teacher["Должность"]
    tr2.append(td3)

    tbody.append(tr2)

table.append(tbody)

paste.append(table)

with open('index.html', 'w', encoding="UTF-8") as index_file:
    index_file.write((soup.prettify()))