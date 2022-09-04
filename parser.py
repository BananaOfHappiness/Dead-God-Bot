import requests
import time
import re
from bs4 import BeautifulSoup

url = 'https://dead-god.ru'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15"
}

def get_desc(name_input):
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        Item_Name = soup.find('span', {'data-name': True}, string = re.compile(name_input, re.I))
        Parent = Item_Name.parent
        Item_Description = Parent.find('span', {'data-description' : True}).get_text() 
        Item_Synergies = Parent.find('span', {'data-synergies' : True})
        Item_Book_of_Virtues = Parent.find('span', {'book-of-virtues-wisp' : True})
        Item_Judas_Birth_Right = Parent.find('span', {'judas-birthright-effect' : True})
        Item_Bugs = Parent.find('span', {'data-bugs' : True})
        if Item_Synergies != None:
            Item_Synergies = Item_Synergies.text
        else:
            Item_Synergies = ''

        if Item_Book_of_Virtues != None:
            Item_Book_of_Virtues = Item_Book_of_Virtues.text
        else:
            Item_Book_of_Virtues = ''

        if Item_Judas_Birth_Right != None:
            Item_Judas_Birth_Right = Item_Judas_Birth_Right.text
        else:
            Item_Judas_Birth_Right = ''

        if Item_Bugs != None:
            Item_Bugs = Item_Bugs.text
        else:
            Item_Bugs = ''
        return Item_Name.text, Item_Description, Item_Synergies, Item_Book_of_Virtues, Item_Judas_Birth_Right, Item_Bugs
    except:
        return "None, Pls try again", 'Ой! Что-то пошло не так, попробуйте ввести точное название предмета', '', '', '', ''


def download_pics():
    urls = []
    names =[]
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    for link in soup.find_all('span', {'data-icon' : True}):
        urls.append(''.join(link.find_all(text=True)))
    for name in soup.find_all('span', {'data-name' : True}):
        names.append(''.join(name.find_all(text=True)))
    for i in range(0, len(urls)):
        url1 = urls[i]
        img_data = requests.get(url1, verify=False).content
        with open('downloads/' + names[i] + '.png', 'wb') as handler:
            handler.write(img_data)
    print('Done!')

if __name__ == '__main__':
    download_pics()