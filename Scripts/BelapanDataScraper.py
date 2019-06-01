from nltk import tokenize
import os
import regex as re
import requests
from time import sleep
from bs4 import BeautifulSoup as bs

def tokenize_from_text(text, outputPath):
    counter = 0
    tokenized_text = tokenize.sent_tokenize(text)
    outF = open(outputPath, "a", encoding="utf8")
    #to avoid sentenses about place and date of action we use [1:]
    for line in tokenized_text[1:]:
        if(line == ""):
            continue
        counter +=1
        if("\n" in line):
            outF.write(line)
        else:
            outF.write(line + "\n")
    outF.close()
    return counter

def nextMonthPage(oldUrl):
    m = re.search(r'archive/(\d{4,})/(\d{2,})/', oldUrl)
    year = int(m.group(1))
    newMonth = int(m.group(2))+1
    if(newMonth == 13):
        newMonth = 1
        year += 1
        create_folder(year)
    if year == 2018 and newMonth == 12:
        return "exit"
    strMonth = str(newMonth).zfill(2)
    pathToBelFile = create_file(newMonth, year, "be")
    pathToRusFile = create_file(newMonth, year, "ru")
    replacedYear = oldUrl.replace(m.group(1), str(year))
    newUrl = replacedYear[:35]+strMonth+
    replacedYear[37:69]+strMonth+replacedYear[71:]
    print(f"Year: {year}. Month: {newMonth}")
    return [newUrl, pathToBelFile, pathToRusFile]

def processMonthPage(monthPageUrl):
    r = requests.get(monthPageUrl)
    soup = bs(r.content, 'html.parser')
    links = []
    for link in soup.findAll('a', href=True, target="_blank"):
        correctLink = link['href']
        #to avoid incorrect non-number links 
        if(not any(c.isalpha() for c in correctLink[8:].replace("eu", ""))):
            if(correctLink.find("_") != -1):
                links.append(f"https://by.belapan.by{correctLink}")
    print("Links count: " + str(len(links)))
    return links

def processArticlePage(pageUrl, pathToFile):
    counter = 0
    r = requests.get(pageUrl)
    soup = bs(r.content, 'html.parser')
    for content in soup.findAll('div', class_ = 'wysiwygContent'):
        counter+=tokenize_from_text(content.text, pathToFile)
    return counter

def get_rus_url(urlBel):
    rusUrlStart = urlBel.replace('by.','')
    indexOfLastSymbol = rusUrlStart.rfind('_')
    return rusUrlStart[:indexOfLastSymbol]

def create_folder(year):
    newpath = os.path.join('BelapanParsedData', str(year))
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def create_file(month, year, lang):
    path = os.path.join('BelapanParsedData', str(year), f'{month}.{lang}')
    open(path, 'x')
    return path

def write_counter_to_file(counter):
    f = open("counter.txt", 'w')
    f.write(str(counterRus))
    f.close()

counterRus = 0
counterBel = 0
currentUrl = r"https://by.belapan.by/archive/2008/08/" +
"?filterby=month&startdate=2008-08-01&chunksize=2000"
#create_folder(2007)
while(currentUrl != "exit"):
    currentUrl, pathToBelFile, pathToRusFile = nextMonthPage(currentUrl)
    sleep(1)
    links = processMonthPage(currentUrl)
    for belLink in links:
        rusLink = get_rus_url(belLink)
        counterBel += processArticlePage(belLink, pathToBelFile)
        counterRus += processArticlePage(rusLink, pathToRusFile)
        write_counter_to_file(counterRus)
        print(f'Tokenized sentenses: {counterRus}')
