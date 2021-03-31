from bs4 import BeautifulSoup
import re

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

def search_and_get_first_group(rawpat, text):
    pat = re.compile(rawpat)
    return pat.search(text.find(string=pat)).groups()[0]

def extract_uses():
    fp = "data/uses/00001.html"
    with open(fp, 'r') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    body = soup.body

    doc_by = body.find('strong').next_sibling.next_sibling.strip()
    
    sciname = search_and_get_first_group('Scientific name: (.*)', body)
    tribe_name = search_and_get_first_group('Native American Tribe: (.*)', body)
    family_name = search_and_get_first_group('Family: (.*)', body)
    family_apg = search_and_get_first_group('Family (APG): (.*)', body)
    notes = search_and_get_first_group('Notes: (.*)', body)
    use_cat = search_and_get_first_group('Use category: (.*)', body)
    use_subcat = search_and_get_first_group('Use sub-category: (.*)', body)
    common_names = search_and_get_first_group('Common names: (.*)', body)
    usda_code = search_and_get_first_group('USDA symbol: (.*) ', body)

    
    return {
            'uses': {
                'tribe_name': tribe_name,
                'use_category': use_cat,
                'use_subcategory': use_subcat,
                'documented_by': doc_by,
                'notes': notes
                },
            'species': {
                'usda_code': usda_code,
                'scientific_name': sciname,
                'common_names': common_names,
                'family': family_name,
                'family_apg': family_apg 
                }
            }
