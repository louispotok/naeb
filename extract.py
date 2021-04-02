from bs4 import BeautifulSoup
import re
import csv
import os
import tqdm

RAW_PATH = "data/raw/"
EXTRACTED_PATH = "data/extracted/"

COL_NAMES = {
        'tribes': ['id', 'tribe_name'],
        'species': ['id', 'name','common_names','usda_code'],
        'uses': ['id','tribe_name','species_scientific_name'
            ,'use_category'
            ,'use_subcategory'
            ,'documented_by'
            ,'notes'
            ,'_species_usda_code'
            ,'_species_common_names'
            ,'_species_family'
            ,'_species_family_apg'
        ]
        }

def main():
    if not os.path.exists(EXTRACTED_PATH):
        os.mkdir(EXTRACTED_PATH)
    print("extracting tribes")
    # tribes = process('tribes', extract_tribes)
    print("extracting species")
    # species = process('species', extract_species)
    print("extracting uses")
    uses = process('uses', extract_uses)


def process(dirname, extract_fn):
    vals = extract(dirname, extract_fn)
    dump(dirname, vals, COL_NAMES[dirname])

def dump(dirname, vals, col_names):
    fp = os.path.join(EXTRACTED_PATH, f"{dirname}.csv")
    if os.path.exists(fp):
        os.remove(fp)
    with open(fp, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(col_names)
        writer = csv.DictWriter(f, fieldnames=col_names)
        for row in vals:
            writer.writerow(row)

def extract(dirname, fn):
    results = []
    path = os.path.join(RAW_PATH, dirname)
    for filename in tqdm.tqdm(os.listdir(path)):
        fp = os.path.join(path, filename)
        with open(fp, 'r') as f:
            doc = f.read()
        soup = BeautifulSoup(doc, 'html.parser')
        id_ = filename.split('.')[0]
        results.append(fn(soup, id_))
    return results

def extract_tribes(soup, id_):
    """
    Just a list of species and uses
    """
    body = soup.body
    tribe_name = body.h3.text.split(': ')[1]
    return {'tribe_name': tribe_name, 'id': id_}

def extract_species(soup, id_):
    body = soup.body
    species_name = body.h3.text
    
    main_text = body.find_all(attrs={'class': 'container'})[1]

    common_name_pat = re.compile('Common names: (.*)$')
    common_names = common_name_pat.search(main_text.find_all(string=common_name_pat)[0]).groups()[0]
    
    usda_url_pat = re.compile(re.escape("http://plants.usda.gov/java/profile?symbol=") + "(.*)")
    hrefs = [a['href'] for a in main_text.find_all('a')]
    usda_code = None
    for h in hrefs:
        m = usda_url_pat.search(h)
        if m:
            usda_code = m.groups()[0]
            continue

    return {'id': id_, 'name': species_name, 'common_names':common_names, 'usda_code':usda_code}

def search_and_get_first_group(rawpat, text):
    pat = re.compile(rawpat)
    result = text.find(string=pat)
    if result:
        m = pat.search(result)
        if m:
            return m.groups()[0]
    return None

def extract_uses(soup, id_):
    body = soup.body

    doc_by = body.find('strong').next_sibling.next_sibling.strip()
    
    sciname = search_and_get_first_group('Scientific name: (.*)', body)
    tribe_name = search_and_get_first_group('Native American Tribe: (.*)', body)
    family_name = search_and_get_first_group('Family: (.*)', body)
    family_apg = search_and_get_first_group('Family \(APG\): (.*)', body)
    notes = search_and_get_first_group('Notes: (.*)', body)
    use_cat = search_and_get_first_group('Use category: (.*)', body)
    use_subcat = search_and_get_first_group('Use sub-category: (.*)', body)
    common_names = search_and_get_first_group('Common names: (.*)', body)
    usda_code = search_and_get_first_group('USDA symbol: (.*) \(', body)

    # TODO: don't split these here; later when we normalize
    return {
            'id': id_,
            'tribe_name': tribe_name,
            'species_scientific_name': sciname,
            'use_category': use_cat,
            'use_subcategory': use_subcat,
            'documented_by': doc_by,
            'notes': notes,
            '_species_usda_code': usda_code,
            '_species_common_names': common_names,
            '_species_family': family_name,
            '_species_family_apg': family_apg 
            }


if __name__ == '__main__': 
    main()
