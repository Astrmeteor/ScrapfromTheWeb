import sys
import requests
import html5lib
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
reload(sys)
sys.setdefaultencoding('utf-8')


def text_save(filename, data):
    file = open(filename, 'w')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')
        s = s.replace("u'", '').replace(',', '') + '\n'
        s = s.replace("'", '')
        s = s.replace("\u2018", '"').replace("\u2019", '"').replace("\u201c", '"').replace("\u201d", '"').replace("\u2026", '...').replace("\u2013", '-').replace("\xa0", ':')
        file.write(s)
    file.close()
    print ("Saved")


def Scraping():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    res = requests.get('https://wuxiaworld.com/novel/battle-through-the-heavens', headers=headers)
    res.encoding = res.apparent_encoding
    html = res.text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find('div', class_="novel-body").find('h2')
    author = soup.find('div', style="flex: 1").find('dd')
    intro = soup.find('div', class_="novel-bottom p-15").find('div', class_='fr-view').find('p')
    print('Novel:', title.text, '\n Author:', author.text, '\n Intro:', intro.text)

    chapter_url = requests.get('https://wuxiaworld.com/novel/battle-through-the-heavens#chapters', headers=headers)
    chapter_url.encoding = chapter_url.apparent_encoding
    xml = chapter_url.text
    soup1 = BeautifulSoup(xml, "html.parser")
    lists = soup1.find_all('li', class_='chapter-item')
    list_all = []
    list_m = []

    pbar = tqdm(total=len(lists), desc='Scraping')
    for list_n in lists:
        a = list_n.find('a')
        #name = a.text
        chapter = 'https://www.wuxiaworld.com'+a['href']
        req = requests.get(chapter, headers=headers)
        req.encoding = req.apparent_encoding
        req = req.text
        s = BeautifulSoup(req, "html.parser")
        find_content = s.find('div', id='chapter-content')
        content = find_content.find_all('p')
        for artical in content:
            list_all.append([artical.text])
        pbar.update(1)
    pbar.close()

    list_m[0:3] = [title.text, author.text, intro.text]
    list_m += list_all
    text_save('BattleThroughTheHeavens.txt', list_m)
if __name__ == '__main__':
    Scraping()
