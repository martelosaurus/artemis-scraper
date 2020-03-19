import inflect

root = '/home/jordan/Dropbox/ProjectGreen/Artemis/'

storm_words = [
    'storm',
    'snow',
    'flood',
    'hurricane',
    'wind',
    'cyclone',
    'winter',
    'surge'
]

field_names_l1 = [
    'Cedent / sponsor',
    'Placement / structuring agent/s',
    'Trigger type', 
    'Risk modelling / calculation agents etc',
    'Risks / perils covered',
    'Issuer',
    'Size',
    'Date of issue',
]

field_names_l2 = [
    'term',
    'year',
    'mnth',
    'storm',
    'earthquake',
    'num_years',
    'expected loss of',
    'attachment probability of',
    'year',
    'classes',
    'tranche'
]

conjunction_regex = '(\, while|\, the second)'

field_names = field_names_l1 + field_names_l2

def num_wrds():
    """returns list of the english word for each number up to ten"""
    nums = range(0,10)
    p = inflect.engine()
    return  dict(zip(map(lambda t: p.number_to_words(t).encode('utf-8'),nums),nums))

def download():
    """download html files from Artemis"""
    soups = BeautifulSoup(open('main.html'),'html.parser')
    links = map(lambda link: link.get('href'), soups.find_all('a'))
    links = links[152:741]
    links = map(lambda link: link.encode('utf-8'), links)
    for link in enumerate(links):
        urllib.urlretrieve(link[1], root + str(link[0]) + '.html')
