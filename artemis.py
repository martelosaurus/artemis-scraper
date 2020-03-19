import csv, os, urllib, re, artsupp
import numpy as np
import matplotlib.dates as mdates
from bs4 import BeautifulSoup

class Tranche(self):

    def __init__(self,name,size,expected_loss,attchmnt_prob):
    
        self.name = name
        self.size = size
        self.expected_loss = expected_loss
        self.attchmnt_prob = attchmnt_prob

class Issue(self):

    def __init__(self,name,size):

        self.name = name
        tranche_sizes = dedictify('size',tranches)

    def add_tranche(self,tranches):
        """adds a set of tranches to the issue"""
        # NOTE: 23-04-2019: assume any issue w/o class is single

    def aggregate(self):
        """aggregates expected losses and attachment probabilities"""

        def dedictify(key,tranches):
            return np.array([tranche[key] for tranche in tranches])  

        expected_loss = dedictify('expected_loss',tranches)
        attchmnt_prob = dedictify('attchmnt_prob',tranches)

        issue['expected loss of'] = np.average(expected_loss,weight=tranche_size)
        issue['attchmnt prob of'] = np.average(attchmnt_prob,weight=tranche_size)


# PARAMETERS
N = 20
n = 10

num_wrds = artsupp.num_wrds()

# LOOP OVER FILES
DB = []
FD = []

for fname in os.listdir(artsupp.root):
    
    # create an issue
    issue = Issue()

    # prepare the soup
    soup = BeautifulSoup(open(artsupp.root+fname),'html.parser')

    #-------------------------------------------------------------------------#
    # STAGE I: AT A GLANCE                                                    #  
    #-------------------------------------------------------------------------#

    # strain the soup
    at_a_glance = soup.find_all('li')[-N:]
    at_a_glance = [item.text.encode('utf-8') for item in at_a_glance]

    # fix rating agencies 
    for agency in ['Fitch','Moodys','Morningstar','S&P']:
        at_a_glance = [item.replace(agency+':',agency) for item in at_a_glance]

    # find at a glance items
    for field in artsupp.field_names_l1:
        line = [item for item in at_a_glance if field in item]        
        line = line[0].split(': ')
        issue[field] = '' if len(line) == 1 else line[1]

    # clean size
    issue['Size'] = issue['Size'].replace(')','').replace('m','')
    size_index = issue['Size'].find('$')
    issue['Size'] = issue['Size'][size_index+1:] 

    # date of issue
    issue_date = issue['Date of issue'].split(' ')
    issue['year'] = issue_date[1] 
    issue['mnth'] = issue_date[0]

    #-------------------------------------------------------------------------#
    # STAGE II: FULL DETAILS                                                  #  
    #-------------------------------------------------------------------------#

    # full details
    full_details = soup.find_all('div')[17]
    full_details = full_details.find_all('p')
    full_details = map(lambda para: para.text.encode('utf-8'), full_details)
    full_details_words = []
    for paragraph in full_details:
        paragraph = paragraph.replace('-',' ') 
        full_details_words += [paragraph]
    full_details_words = '. '.join(full_details_words)

    # pull the peril
    set1 = set(issue['Risks / perils covered'])
    set2 = set(artsupp.storm_words)
    issue['storm'] = False if set1.isdisjoint(set2) else True
    issue['earthquake'] = True if 'earthquake' in issue['Risks / perils covered'] else False

    # pull the term
    year_split = full_details_words.split('year')
    year_words = map(lambda x: x.replace('(',' ').replace(')',' '),year_split)
    year_words = map(lambda x: x[-n:-1],year_words)
    year_words = map(lambda x: x[x.rfind(' ')+1:],year_words)
    year_words = map(lambda x: str(num_wrds[x]) if x in num_wrds.keys() else x,year_words)
    year_words = map(lambda x: x.replace(',',''),year_words)
    year_words = filter(lambda x: not x.isalpha(),year_words)
    year_words = map(lambda x: float(x),year_words)
    year_words = filter(lambda x: x<10,year_words)
    issue['term'] = '' if not year_words else year_words[0]        
    issue['num_years'] = 'ONE' if len(set(year_words)) is 1 else ''

    # NOTE: 23-04-2019: only issue w/ tranche, w/o class is EDF 12-2003   
    class_regex = 'Class ([A-Z]|\d+)'
    class_found = set(re.findall(class_regex,full_details_words))
    issue.add_tranche(class_found)

    for phrase in ['expected loss of','attachment probability of']:

        phrase_regex = '(?<!above\s)' + value + ' (\d\.\d+)%'

        for sentence in full_details_words.split('. '):

            # NOTE: 25-04-2019: typically, there is just one clause
            for clause in re.split(artsupp.conjunction_regex,sentence):

                # STEP 1: find "value phrases" and extract values
                # NOTE: 23-04-2019: false 'expected loss's preceded by 'above'
                values = re.findall(phrase_regex,clause)

                # STEP 2: find the tranche in clause, sentence, or paragraph 
                tranche = re.findall(issue.tranche)
           
                if clause_trnch: # check clause
                        issue.add_stat(phrase,phrase_nmbrs)
                elif sentence_trnch: # check sentence

                elif paragraph_trnch: # check paragraph

                else:


    issue.aggregate()

    DB += [issue]

# PRINT DATA TO DISK
with open('artemis_data.csv','w') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=artsupp.field_names)
    writer.writeheader()
    for row in DB:
        writer.writerow(row)
