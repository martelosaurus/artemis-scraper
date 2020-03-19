import csv, time, random 
from bs4 import BeautifulSoup
import urllib2 as url

# parameters
N = 20 # maximum number of items in the item list

field_names = ['Ratings','Cedent / sponsor','Placement / structuring agent/s','Trigger type', 'Risk modelling / calculation agents etc','Risks / perils covered','Issuer','Size','Date of issue']
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
    
            issue = {}
            at_a_glance = soup.find_all('li')[-N:]
            at_a_glance = map(lambda t: t.text.encode('utf-8'),at_a_glance)    

            def find_field(field):
                for line in at_a_glance:
                    if line.find(field) is 0:
                        return line[len(field)+2:]

            for field in field_names:
                issue[field] = find_field(field)

            full_details = soup.find_all('div')[17].text.encode('utf-8')
            full_details = full_details.split('. ')

            expected_loss = []
            for sentence in full_details:
                if sentence.find('expected loss') is not -1:
                    expected_loss += [sentence]
            expected_loss = '. '.join(expected_loss) 

            attachment_prob = []
            for sentence in full_details:
                if sentence.find('attachment') is not -1:
                    attachment_prob += [sentence]
            attachment_prob = '. '.join(attachment_prob) 

            issue['Expected_Loss'] = expected_loss
            issue['Attachment_Prob'] = attachment_prob
            #issue['Notes'] = full_details

            DB += [issue]

with open('artemis_data.csv','w') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=field_names + ['Expected_Loss','Attachment_Prob'])
    writer.writeheader()
    for row in DB:
        writer.writerow(row)
