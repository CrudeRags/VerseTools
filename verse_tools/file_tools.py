import re
from verse_tools import GetVerses as gv


def extract(file_string):
    refPattern = re.compile(r'(\d* *\w+\s+\d+:\s*\d+[-\d\s:,;]*|\d+:\s*\d+[-\d\s,:;]*)')
    my_refs = refPattern.findall(file_string)
    return [x.strip(";,") for x in map(str.strip, my_refs)]


def extract_paragraph_refs(file_string):
    refPattern = re.compile(r'(\{.*?\})')
    my_refs = refPattern.findall(file_string)
    return [x for x in map(str.strip, my_refs)]


def __getVerses__(refs, lang):
    g = gv.GetVerses(lang=lang)   
    return g.get(refs)

def get(refs, lang=None, output=None):
    out_list = []

    if lang is not None:
        langs = lang.split(',')
        for l in langs:
            out_list.append(__getVerses__(refs,l.strip()))
    else:
        lang = gv.get_pref()['default_language']
        out_list.append(__getVerses__(refs,lang))

    x = len(out_list)
    y = len(out_list[0])
    z = [(b, a) for a in range(x) for b in range(y)]
    z.sort()

    if output is not None:
        with open(output, 'w+', encoding='utf8') as out:
            for b, a in z:
                out.write(out_list[a][b]['ref'] + " " +
                          out_list[a][b]['verse'] + '\n')

    else:
        for b, a in z:
            print(out_list[a][b]['ref'] + '\n' + out_list[a][b]['verse'])
            print()
