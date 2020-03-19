import os, urllib, re
from bs4 import BeautifulSoup

root = '/home/jordan/Dropbox/ProjectGreen/Artemis/'

j = 0
for fname in os.listdir(root):
        
    soup = BeautifulSoup(open(root+fname),'html.parser')

    full_details = soup.find_all('div')[17]
    full_details = full_details.find_all('p')
    full_details = map(lambda para: para.text.encode('utf-8'), full_details)

    full_details = '. '.join(full_details)

    for sentence in full_details.split('. '):
        if re.findall('single\s(?!tranche)',sentence):
            print('')
            j += 1
            print(j)
            print(sentence)


