import requests
import os
import sys

'''A python script to download the necessary Bibles to get verses from. These bibles are present in a github account 
and should be downloaded from it to get the getVerses.py to work '''


def process_input(i):
    i = i.split(',')
    for x in i:
        if '-' in x:
            range_begin, range_end = [int(i) for i in x.split('-')]
            yield from (int(y) for y in range(range_begin, range_end + 1))
        else:
            yield int(x)


# Variable Declaration

my_url = "https://raw.githubusercontent.com/CrudeRags/Bible-database-for-python/master/"
allLanguages = ['English', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Hindi']

my_database_path = os.path.join(os.path.dirname(__file__), 'resources/Bibles/')
if not os.path.exists(my_database_path):
    os.makedirs(my_database_path)

databases_in_path = [i for i in os.listdir(my_database_path) if i[-2:] == "db"]
existing_languages = [i.split('Bible.db')[0] for i in databases_in_path]

downloadableLanguages = [i for i in allLanguages if i not in existing_languages]
display = [i + "\t[" + str(downloadableLanguages.index(i)) + "]" for i in downloadableLanguages]

availableBibles = "Local Bibles:\n" + '  '.join(existing_languages)
downloadableBibles = "Remote Bibles:\n" + '\n'.join(display)


# Start of Program
def download():

    print(availableBibles)
    print()
    print(downloadableBibles)
    raw_input = input("\nYour Choice (can choose more than one): ")

    toDownload = [downloadableLanguages[i] for i in process_input(raw_input)]

    for x in toDownload:
        BibleName = x + "Bible.db"
        with open(my_database_path + BibleName, 'wb') as out:
            r = requests.get(my_url + BibleName, stream=True)
            print("Downloading {}".format(BibleName))
            total_length = r.headers.get('content-length')

            if total_length is None:  # header does not have content-length
                out.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for chunk in r.iter_content(chunk_size=4096):
                    dl += len(chunk)
                    out.write(chunk)
                    done = int(25*dl/total_length)
                    remaining = 25-done
                    sys.stdout.write("\r[{}{}]".format('='*done,' '*remaining))
                    sys.stdout.flush()

        print("Finished downloading {}".format(BibleName))

if __name__ == '__main__':
    download()