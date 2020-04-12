import re
from verse_tools import GetVerses as gv


def extract(file_string):
    refPattern = re.compile(r'(\d* \w+ \d+:\s*\d+[\d\s,;]*)')
    my_refs = refPattern.findall(file_string)
    return [x for x in map(str.strip, my_refs)]


def extract_paragraph_refs(file_string):
    refPattern = re.compile(r'(\{.*?\})')
    my_refs = refPattern.findall(file_string)
    return [x for x in map(str.strip, my_refs)]


def getExtractedVerses(refs, lang="English"):
    g = gv.GetVerses(lang=lang)
    return g.get