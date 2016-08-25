from bs4 import BeautifulSoup
import re
import json

regex = re.compile(r"([0-9]+)", flags=0)
soup = BeautifulSoup(open("data.html"), "lxml")

def genNameAndUrl(obj):
  dataObj = {}
  dataObj["name"] = obj["title"]
  dataObj["url"] = obj["href"]
  return dataObj

allData = {}
allData["domain"] = "http://wiki.52poke.com"
nameAndUrls = []

allTd = soup.find_all('td')
langs = ["ch","jp","en"]

for oneTd in allTd:
  if oneTd.string and "#" in oneTd.string:
    tdStr = str(oneTd.string)
    match = re.search(regex, tdStr)
    if match:
      pokeData = {}
      pokeId = int(match.group(0))
      pokeData["id"] = pokeId
      for lang in langs:
        oneTd = oneTd.next_sibling.next_sibling
        if oneTd:
          pokeData[lang] = genNameAndUrl(oneTd.a)
      nameAndUrls.append(pokeData)

allData["data"] = nameAndUrls

with open('data.json', 'w') as outfile:
    json.dump(allData, outfile, encoding="utf-8")