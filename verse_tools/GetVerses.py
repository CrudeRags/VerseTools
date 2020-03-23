import sqlite3
import os
import sys
import re
import argparse
import json
from verse_tools.getResources import get as gL
from verse_tools.getResources import main as gR
from verse_tools import config

def get_pref():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    if not os.path.isfile(config_path):
        config.main()

    with open(config_path, 'r') as rf:
        pref = json.load(rf)

    return pref

def get_resources(lang=None):
    if lang is None:
        gR()
    else:
        gL(lang)

class GetVerses:
    # Initialize class with language only
    def __init__(self, lang=None):

        self.pref = get_pref()                   
        
        if lang is None:
            print("No language specified. Choosing {}".format(self.pref["default_language"]))
            self.lang = self.pref["default_language"]
        else:
            self.lang = lang.capitalize()
        
        self.__variables__() 

        self.__connect__()

    def __variables__(self):
        self.book_res = {"Genesis": 0, "Gen": 0, "Ge": 0, "Gn": 0, "Exodus": 1, "Ex": 1, "Exod": 1, "Exo": 1,
                         "Leviticus": 2, "Lev": 2, "Le": 2, "Lv": 2, "Numbers": 3, "Num": 3, "Nu": 3, "Nm": 3, "Nb": 3,
                         "Numb": 3, "Deuteronomy": 4, "Deut": 4, "De": 4, "Dt": 4, "Deu": 4, "Joshua": 5, "Josh": 5,
                         "Jos": 5, "Jsh": 5, "Judges": 6, "Judg": 6, "Jdg": 6, "Jg": 6, "Jdgs": 6, "Ruth": 7, "Rth": 7,
                         "Ru": 7, "1Samuel": 8, "1Sam": 8, "1Sm": 8, "1Sa": 8, "1S": 8, "2Samuel": 9, "2Sam": 9,
                         "2Sm": 9, "2Sa": 9, "2S": 9, "1Kings": 10, "1Kgs": 10, "1Kin": 10, "1Ki": 10, "1K": 10,
                         "2Kings": 11, "2Kgs": 11, "2Kin": 11, "2Ki": 11, "1Chronicles": 12, "1Chr": 12, "1Chron": 12,
                         "1Ch": 12, "2Chronicles": 13, "2Chr": 13, "2Ch": 13, "2Chron": 13, "Ezra": 14, "Ezr": 14,
                         "Nehemiah": 15, "Neh": 15, "Ne": 15, "Esther": 16, "Esth": 16, "Est": 16, "Es": 16, "Job": 17,
                         "Jb": 17, "Psalms": 18, "Ps": 18, "Psalm": 18, "Pslm": 18, "Psa": 18, "Psm": 18,
                         "Proverbs": 19, "Prov": 19, "Pro": 19, "Prv": 19, "Pr": 19, "Ecclesiastes": 20, "Eccl": 20,
                         "Eccles": 20, "Eccle": 20, "Ecc": 20, "Ec": 20, "Song": 21, "Isaiah": 22, "Isa": 22, "Is": 22,
                         "Jeremiah": 23, "Jer": 23, "Je": 23, "Jr": 23, "Lamentations": 24, "Lam": 24, "La": 24,
                         "Ezekiel": 25, "Ezek": 25, "Eze": 25, "Ezk": 25, "Daniel": 26, "Dan": 26, "Da": 26, "Dn": 26,
                         "Hosea": 27, "Hos": 27, "Ho": 27, "Joel": 28, "Jl": 28, "Amos": 29, "Am": 29, "Obadiah": 30,
                         "Obad": 30, "Jonah": 31, "Jon": 31, "Jnh": 31, "Micah": 32, "Mic": 32, "Mc": 32, "Nahum": 33,
                         "Nah": 33, "Na": 33, "Habakkuk": 34, "Hab": 34, "Zephaniah": 35, "Zeph": 35, "Zep": 35,
                         "Zp": 35, "Haggai": 36, "Hag": 36, "Hg ": 36, "Zechariah": 37, "Zech": 37, "Zec": 37, "Zc": 37,
                         "Malachi": 38, "Mal": 38, "Ml": 38, "Matthew": 39, "Mt": 39, "Matt": 39, "Mark": 40, "Mk": 40,
                         "Mrk": 40, "Luke": 41, "Lk": 41, "Luk": 41, "John": 42, "Jn": 42, "Jhn": 42, "Acts": 43,
                         "Romans": 44, "Rom": 44, "Ro": 44, "Rm": 44, "1Corinthians": 45, "1Cor": 45, "1Co": 45,
                         "2Corinthians": 46, "2Cor": 46, "2Co": 46, "Galatians": 47, "Gal": 47, "Ga": 47,
                         "Ephesians": 48, "Eph": 48, "Ephes": 48, "Philippians": 49, "Phil": 49, "Php": 49, "Pp": 49,
                         "Colossians": 50, "Col": 50, "1Thessalonians": 51, "1Thess": 51, "1Thes": 51, "1Th": 51,
                         "2Thessalonians": 52, "2Thess": 52, "2Thes": 52, "2Th": 52, "1Timothy": 53, "1Tim": 53,
                         "1Ti": 53, "2Timothy": 54, "2Tim": 54, "2Ti": 54, "Titus": 55, "Tit": 55, "Ti": 55,
                         "Philemon": 56, "Philem": 56, "Phm": 56, "Pm": 56, "Hebrews": 57, "Heb": 57, "James": 58,
                         "Jas": 58, "Jm": 58, "1Peter": 59, "1Pet": 59, "1Pe": 59, "1Pt": 59, "1P": 59, "2Peter": 60,
                         "2Pet": 60, "2Pe": 60, "2Pt": 60, "2P": 60, "1John": 61, "1Jn": 61, "1Jhn": 61, "1J": 61,
                         "2John": 62, "2Jn": 62, "2Jhn": 62, "2J": 62, "3John": 63, "3Jn": 63, "3Jhn": 63, "3J": 63,
                         "Jude": 64, "Jud": 64, "Jd": 64, "Revelation": 65, "Rev": 65}
        
        self.my_database_path = os.path.abspath(self.pref['resource_path'])
        my_languages = [i.split("Bible")[0] for i in
                        list(filter(lambda x: x[-2:] == "db", os.listdir(self.my_database_path)))]
        if len(my_languages) < 1:
            get_resources()

        unknown_lang = "Unknown language. Supported languages:\n" + '\n'.join(self.pref['git_languages'])
        if self.lang not in self.pref['git_languages']:
            print("you have chosen {}".format(self.lang))
            sys.exit(unknown_lang)
        elif self.lang not in my_languages:
            print("{} is not available locally".format(self.lang))
            downloadMore = input("Do you want to download {} Bible? (y/N)".format(self.lang))
            if downloadMore == 'y':
                get_resources(lang=self.lang)

    def __connect__(self):
        """Connect to Language specific database"""
        db = os.path.join(self.my_database_path, '{}Bible.db'.format(self.lang))

        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

    def __process_references__(self, references):
        """Return a list of tuples consisting of the chosen language reference and its encoded form"""
        # Encoded form is needed for retrieving data from the database
        _raw_ = []
        _processed_ = []
        if isinstance(references, list):
            for item in references:
                _raw_.extend(item.split(';'))

        elif isinstance(references, str):
            _raw_.extend(references.split(';'))
        else:
            sys.exit("Undetermined Reference type - Only a  list of references or a single reference is supported")
        for ref in _raw_:
            ref = ref.strip()
            ref = re.sub(r'^(\d)\s', r'\1', ref)
            encoded_ref = self.__encode_ref__(ref)
            self.c.execute('SELECT name FROM bookIndex WHERE num=?', (encoded_ref[0][0],))
            book_name = str(self.c.fetchone()[0])
            _, chap_verse = ref.split(' ',1)
            new_reference = book_name + ' ' + chap_verse
            _processed_.append((new_reference, encoded_ref))

        return _processed_

    def __encode_ref__(self, ref):
        """Take one reference and return the book,chapter,verse as integers used to retrieve verses from the database"""
        reference_list = []
        book, _ = ref.split(" ", 1)
        book_number = self.book_res[book]

        chapter_number, raw_verse_nums = [i for i in map(str.strip, _.split(":", 1))]

        verse_nums = []
        parts = raw_verse_nums.split(',')
        for part in parts:
            if '-' in part:
                range_begin, range_end = part.split('-')
                verse_nums.extend([i for i in range(int(range_begin), int(range_end) + 1)])
            else:
                verse_nums.append(part)

        for verseNum in verse_nums:
            reference_list.append((int(book_number), int(chapter_number), int(verseNum)))

        return tuple(reference_list)

    def get(self, references):
        verse_list = []

        my_references = self.__process_references__(references)

        for newReference, encodedReferences in my_references:
            verse_dict = {}
            verses = []
            for reference in encodedReferences:
                self.c.execute('SELECT verse FROM bible WHERE Book=? AND Chapter=? AND Versecount=?', reference)
                verses.append((str(self.c.fetchone()[0])))

            verse_dict['ref'] = newReference
            verse_dict['verse'] = ' '.join(verses)

            verse_list.append(verse_dict)

        return verse_list

def set_lang(lang):
    confirm = input("Are you sure you want to change default fallback language? (y/n): ")
    
    with open(os.path.dirname(__file__)+"config.json",'r') as rf:
        pref = json.load(rf)
    
    if confirm == 'y':
        pref["default_language"] = lang.lower().capitalize()
    
    with open(os.path.dirname(__file__) + "config.json", 'w') as rf:
        json.dump(pref, rf, indent=2,sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lang", nargs='*',
                        help="Language you want to retrieve verses in - Enter full name")
    parser.add_argument("-o", "--output", help="Output file name. Ex: output.txt")
    parser.add_argument("-u", "--usage", help="Help regarding detailed usage")
    parser.add_argument("-c", "--change_language", help="change default language")
    parser.add_argument("ref", help="reference to be looked up or name of file containing references")

    args = parser.parse_args()

    if len(sys.argv) == 1 or not args.ref:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.lang is None:
        pref = get_pref()
        print("\nNo language specified. Choosing {}\n".format(pref["default_language"]))
        args.lang = [pref["default_language"]]
    
    if args.change_language:
        set_lang(args.change_language)

    elif args.usage:

        usage = '''

        Detailed Help for GetVerses.py!        


        usage: GetVerses.py [-h] [-l LANG] [-o OUTPUT] [-u USAGE] [-c CHANGE_LANGUAGE] ref

        This script takes in a single reference or a file containing
        multiple references - each reference in a single line. 
        It also takes in the name of the language in which you 
        want the output and either displays the verses with the 
        reference or writes it to a file for storing

        -o Use this flag to specify the path of the output file 

        -l Specify in which language you want the output. If no language
        is specified, it defaults to your preferred language. More than
        one language can be specified

        -c Change your default language


        Examples: 


        getVerses.py "Ezra 1:1"         

        >This prints Ezra 1:1 in default language on screen


        getVerses.py -o "E:/my_verses.txt" -l English "Rev 1:7"         

        >This creates a new file called "my_verses.txt" and prints 
        the verse in English into the file


        getVerses.py -o "my_verses.txt" -l Telugu "my_references.txt" 

        >This reads all the references from my_references.txt and 
        ouputs the verses in Telugu into the file "my_verses.txt"


        '''

        print(usage)

    my_ref = args.ref

    if os.path.isfile(my_ref):
        with open('my_ref') as f:
            my_ref = f.read().splitlines()

    output = []

    for _lang_ in args.lang:

        raw_out = GetVerses(_lang_).get(my_ref)
        output.append(raw_out)

    x = len(output)
    y = len(output[0])
    z = [(b, a) for a in range(x) for b in range(y)]
    z.sort()

    if args.output:
        with open(args.output, 'w+', encoding='utf8') as out:
            for b, a in z:
                out.write(output[a][b]['ref'] + ' ' + output[a][b]['verse'] + '\n\n')

    else:
        for b, a in z:
            print(output[a][b]['ref'] + '\n' + output[a][b]['verse'])
            print()
