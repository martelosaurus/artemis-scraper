import csv, time, random 
from bs4 import BeautifulSoup
import urllib2 as url

# parameters
N = 20 # maximum number of items in the item list

field_names = ['Ratings','Cedent / sponsor','Placement / structuring agent/s','Trigger type', 'Risk modelling / calculation agents etc','Risks / perils covered','Issuer','Size','Date of issue','Notes']
field_names.sort()

DB = []

with open('artemis_deals.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != 'Issuer':  

            issue = row[0]
            issue = issue.lower()
            issue = issue.replace('/','-')
            issue = issue.replace('(',' ')
            issue = issue.replace(')','')
            issue = issue.replace(' ','-')
            issue = issue.replace('---','-')
            issue = issue.replace('--','-')
            issue = issue.replace('.','')

            arturl = 'http://www.artemis.bm/deal-directory/{}/'.format(issue)
            print(arturl)
            response = url.urlopen(arturl)
            soup = BeautifulSoup(response,'html.parser')
    
            at_a_glance = soup.find_all('li')[-N:]
            at_a_glance = map(lambda t: t.text.encode('utf-8'),at_a_glance)    

            def 

            at_a_glance = map(lambda t:
            

            at_a_glance = ':'.join(at_a_glance)
            for rating_agency in ['Fitch','Moodys','Morningtsar','S&P']:
                at_a_glance = at_a_glance.replace(rating_agency,rating_agency[:-1])
            at_a_glance = at_a_glance.split(':')
            at_a_glance = dict(zip(at_a_glance[::2],at_a_glance[1::2]))
            
            full_details = soup.find_all('div')[17].text.encode('utf-8')
            full_details = full_details.split('. ')

            at_a_glance['Notes'] = full_details

            keys = at_a_glance.keys()
            keys.sort()
            if keys == field_names:
                print(keys)
                print(field_names)
                DB = DB + [at_a_glance]
                print(len(DB))

with open('artemis_data.csv','w') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=field_names)
    writer.writeheader()
    for row in DB:
        writer.writerow(row)
