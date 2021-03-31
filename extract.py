from bs4 import BeautifulSoup

def extract_tribes():
    """
    Just a list of species and uses
    """
    fp = "data/tribes/00001.html"
    with open(fp, 'r') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    body = soup.body
    
    tribe_name = body.h3.text.split(': ')[1]

    return {'tribe_name': tribe_name}

def extract_species():
    fp = "data/species/00001.html"
    with open(fp, 'r') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    body = soup.body
    species_name = body.h3.text
    
    main_text = body.find_all(attrs={'class': 'container'})[1]

    common_name_pat = re.compile('Common names: (.*)$')
    common_names = pat.search(main_text.find_all(string=pat)[0]).groups()[0]

    usda_url_pat = re.compile("http://plants.usda.gov/java/profile?symbol=(.*)")
    usda_code = usda_url_pat.search(main_text.find('a')['href']).groups()[0]

    return {'name': species_name, 'common_names';common_names, 'usda_code':usda_code}


