import sqlite3
import csv
from tqdm import tqdm

def main():
    tribes, species, uses = load_tables()
    con = sqlite3.connect('naeb.sqlite3')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    insert_tribes(cur, tribes)
    insert_species(cur, species)
    insert_uses(cur, uses)
    con.commit()
    con.close()

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
    if not result:
        cur.execute(f"INSERT INTO {tname} (name) VALUES (?)", (val, ))
        result = cur.execute(f"SELECT * FROM {tname} where name=?", (val, )).fetchone()
    return result['id']

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


def insert_uses(cur, uses):
    print("loading uses")
    u = uses[0]
    doc_id = get_fk_from_name(cur, 'docs', u['documented_by'])
    use_cat = get_fk_from_name(cur, 'use_categories', u['use_category'])
    use_subcat = get_fk_from_name(cur, 'use_subcategories', u['use_subcategory'])
    tribe_id = get_fk_from_name(cur, 'tribes', u['tribe_name'])
    species_id = get_fk_from_name(cur, 'species', u['species_scientific_name'])

    notes = u['notes']

    insert_remaining_species_info(cur, u, species_id)
    cur.execute("""INSERT INTO uses (id, species, tribe, doc, use_category, use_subcategory, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", 
            (u['id'], species_id, tribe_id, doc_id, use_cat, use_subcat, notes)
            )
    return

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
