"""
Three tables:
    * tribes: 'uses/tribes/X/': 291.
    * species: 'uses/species/X/: 4260
    * uses (fk to species and tribes): 'uses/X/': 44961
"""
import os
import requests
from tqdm import trange
import time 

BASE_URL = "http://naeb.brit.org/"
# [(name, url, n)]
SCHEMA = [
        ('tribes', 'uses/tribes/{}/', 291),
        ('species', 'uses/species/{}/', 4260),
        ('uses', 'uses/{}', 44961)
        ]
headers = {}

def main():
    for (name, url, N) in SCHEMA:
        print(f"Getting {name}")
        folder = ensure_folder(name)
        latest = get_latest(folder)
        u = BASE_URL + url
        for i in trange(latest, N+1):
            u1 = u.format(i)
            resp = requests.get(u1, headers=headers)
            if resp.status_code != 200:
                print(resp.status_code, url)
                raise AssertionError
            fp = os.path.join(folder, f'{i:05.0f}.html')
            with open(fp, 'w') as f:
                f.write(resp.text)
            time.sleep(.5)

def ensure_folder(name):
    base = "data/"
    d = os.path.join(base, name)
    if os.path.exists(d):
        return d
    else:
        os.mkdir(d)
        return d

def get_latest(folder):
    files = os.listdir(folder)
    if len(files) == 0:
        return 1 # ids seem to start at 1
    filenums = [int(x.split('.')[0]) for x in files]
    return max(filenums)


if __name__ == '__main__':
    main()
