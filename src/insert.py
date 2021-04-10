import sqlite3
import csv
from tqdm import tqdm
import json
import sys
sys.path.append('./biblib')
from biblib.bib import Parser

def main():
    tribes, species, uses = load_tables()
    con = sqlite3.connect('naeb.sqlite3')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    insert_sources(cur)
    insert_tribes(cur, tribes)
    insert_species(cur, species)
    con.commit()
    insert_uses(con,cur, uses)
    con.commit()
    con.close()

def insert_sources(cur):
    print("loading sources")
    bib = load_bib()
    mapping = load_mapping()
    ref_to_name = {r:n for n,r in mapping}

    for k,e in tqdm(bib.items()):
        typ = e.typ
        fulltext = ref_to_name[k]
        cur.execute("INSERT INTO sources (refcode, type, fulltext) VALUES (?, ?, ?)", (k, typ, fulltext))
        _id = cur.lastrowid
        for f,v in e.items():
            cur.execute(f"UPDATE sources SET {f} = ? WHERE id = ?", (v, _id))

    return


def insert_tribes(cur, tribes):
    print("loading tribes")
    for t in tqdm(tribes):
        cur.execute("INSERT INTO tribes (id, name) VALUES (?, ?)", (t['id'], t['tribe_name']))
    return

def insert_species(cur, species):
    print("loading species")
    for s in tqdm(species):
        cur.execute(
                " INSERT INTO species (id, name, common_names, usda_code) VALUES (?, ?, ?, ?)",
                (s['id'], s['name'], s['common_names'], s['usda_code'])
                )
    return


def get_fk_from_name(cur, tname, val):
    result = cur.execute(f"SELECT * FROM {tname} where name=?", (val,)).fetchone()
    if result:
        result_id = result['id']
    else:
        cur.execute(f"INSERT INTO {tname} (name) VALUES (?)", (val, ))
        result_id = cur.lastrowid
    return result_id

def insert_remaining_species_info(cur, u, species_id):
    spec = cur.execute("SELECT * FROM species where id=?", (species_id,)).fetchone()
    updates = []
    for cname in ['usda_code', 'common_names','family', 'family_apg']:
        u_val = u['_species_' + cname]
        spec_val = spec[cname]
        if not spec_val:
            updates.append((cname, u_val))
        elif spec_val != u_val:
            raise ValueError(f"use {u} has species.{cname}={u_val} but already exists with val {spec_val}")
        else:
            continue
    for c,v in updates:
        cur.execute(f"UPDATE species SET {c}=? WHERE id=?", (v,species_id))


def get_subcat(cur, subcat_name, cat_id):
    if subcat_name == 'Unspecified':
        return None
    result = cur.execute("SELECT * FROM use_subcategories where name=?", (subcat_name,)).fetchone()
    if result and result['parent']==cat_id:
        subcat_id = result['id']
    else:
        cur.execute(f"INSERT INTO use_subcategories (name, parent) VALUES (?, ?)", (subcat_name, cat_id))
        subcat_id = cur.lastrowid
    return subcat_id

def insert_uses(con, cur, uses):
    mapping = dict(load_mapping())
    print("loading uses")
    for u in tqdm(uses):
        # source_id = get_fk_from_name(cur, 'sources', u['source'])
        source_id = get_source_id(cur, u['source'], mapping)
        use_cat = get_fk_from_name(cur, 'use_categories', u['use_category'])
        use_subcat = get_subcat(cur, u['use_subcategory'], use_cat)
        tribe_id = get_fk_from_name(cur, 'tribes', u['tribe_name'])
        species_id = get_fk_from_name(cur, 'species', u['species_name'])

        notes = u['notes']

        insert_remaining_species_info(cur, u, species_id)
        cur.execute("""INSERT INTO uses (id, species, tribe, source, use_category, use_subcategory, notes, pageno, rawsource)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (u['id'], species_id, tribe_id, source_id, use_cat, use_subcat, notes, u['pageno'], u['rawsource'])
                )
    return

def get_source_id(cur, source, mapping):
    return cur.execute(
            "SELECT id from sources where refcode = ?",
            (mapping[source],)
            ).fetchone()['id']


def load_mapping():
    with open('static/source-mapping.json','r') as f:
        j = json.load(f)
    return j

def load_bib():
    with open('static/canonical-sources.txt', 'r') as f:
        entries = Parser().parse(f).get_entries()
    return entries

def load_tables():
    names = ['tribes','species','uses']
    data = []
    for n in names:
        fp = f"data/extracted/{n}.csv"
        with open(fp, 'r') as f:
            reader = csv.DictReader(f)
            data.append([row for row in reader])
    return tuple(data)

if __name__ == '__main__':
    main()
