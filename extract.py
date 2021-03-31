from bs4 import BeautifulSoup
import re
import json

def main():
    tribes = process('tribes', extract_tribes)
    species = process('species', extract_species)
    uses = process('uses', extract_uses)


def process(dirname, extract_fn):
    vals = extract(dirname, extract_fn)
    dump(dirname, vals)

def dump(dirname, vals):
    fp = "data/processed/{dirname}.json"
    with open(fp, 'w') as f:
        json.dump(vals, f)

def extract(dirname, fn):
    results = []
    for fp in os.listdir(f"data/{dirname}"):
        with open(fp, 'r') as f:
            doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        results.append(fn(soup))
    return results

def extract_tribes(soup):
    """
    Just a list of species and uses
    """
    body = soup.body
    tribe_name = body.h3.text.split(': ')[1]
    return {'tribe_name': tribe_name}

def extract_species(soup):
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

def extract_uses(soup):
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


if __name__ == '__main__': 
    main()
