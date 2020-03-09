import requests
import os
import json
import sys

'''A python script to download the necessary Bibles to get verses from. 
These bibles are present in a github account and should be downloaded 
from it to get the getVerses.py to work '''

def load_preferences():
    _pref_path_ = os.path.join(os.path.dirname(__file__), 'resources/preferences.json')

    with open(_pref_path_, 'r', encoding='utf8') as f:
        _pref = json.load(f)

    return _pref,_pref_path_


def refresh():
    git = requests.get('https://api.github.com/repos/CrudeRags/Bible-database/commits')
    trl = git.json()[0]['commit']['tree']['url']  # url of tree in the latest commit
    trl_get = requests.get(trl)

    my_languages = []

    for x in trl_get.json()['tree']:
        if x['path'][-2:] == 'db':
            my_languages.append(x['path'].split('Bible')[0])

    _pref, preference = load_preferences()

    _pref['git_languages'] = my_languages

    with open(preference, 'w', encoding='utf8') as f:
        json.dump(_pref, f, indent=2)

    return


# Variable Declaration
db_url = "https://raw.githubusercontent.com/CrudeRags/Bible-database-for-python/master/"

try:
    pref, preference_path = load_preferences()
    allLanguages = pref['git_languages']
except KeyError:
    refresh()
    pref, preference_path = load_preferences()
    allLanguages = pref['git_languages']

my_database_path = os.path.join(os.path.dirname(__file__), 'resources/Bibles/')
if not os.path.exists(my_database_path):
    os.makedirs(my_database_path)

databases_in_path = [i for i in os.listdir(my_database_path) if i[-2:] == "db"]
existing_languages = [i.split('Bible.db')[0] for i in databases_in_path]

downloadableLanguages = [i for i in allLanguages if i not in existing_languages]
display = [i + "\t[" + str(downloadableLanguages.index(i)) + "]" for i in downloadableLanguages]

availableBibles = "Local Bibles:\n" + '  '.join(existing_languages)
downloadableBibles = "Remote Bibles:\n" + '\n'.join(display)


def process_input(i):
    i = i.split(',')
    for x in i:
        if '-' in x:
            begin, _end = [int(i) for i in x.split('-')]
            yield from (int(y) for y in range(begin, _end + 1))
        else:
            yield int(x)


# Start of Program
def get():
    print(availableBibles)
    print()
    print(downloadableBibles)
    raw_input = input("\nYour Choice (can choose more than one): ")

    to_download = [downloadableLanguages[i] for i in process_input(raw_input)]

    for x in to_download:
        bible_name = x + "Bible.db"
        with open(my_database_path + bible_name, 'wb') as out:
            r = requests.get(db_url + bible_name, stream=True)
            print("Downloading {}".format(bible_name))
            total_length = r.headers.get('content-length')

            if total_length is None:  # header does not have content-length
                out.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for chunk in r.iter_content(chunk_size=4096):
                    dl += len(chunk)
                    out.write(chunk)
                    done = int(25 * dl / total_length)
                    remaining = 25 - done
                    sys.stdout.write("\r[{}{}]".format('=' * done, ' ' * remaining))
                    sys.stdout.flush()

        print("Finished downloading {}".format(bible_name))


if __name__ == '__main__':
    get()
