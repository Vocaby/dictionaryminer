import wn
import sys
import json
import os
from halo import Halo
from . import ROOT_DIR
from pathlib import Path
from .pronunciations import get_pronunciation

WN_DATA_DIRECTORY = Path.joinpath(ROOT_DIR, 'assets/wordnet-dict/')
WN_ENTRIES_FILE = Path.joinpath(WN_DATA_DIRECTORY, 'wordnet-entries.txt')

wn.config.data_directory = WN_DATA_DIRECTORY

PART_OF_SPEECH = {
    'n': 'noun',
    'v': 'verb',
    'a': 'adjective',
    's': 'adjective',
    'r': 'adverb'
}

dictionary = {}

def setup():
    print('Setting up wordnet...')
    wn_db_path = Path(WN_DATA_DIRECTORY, 'wn.db')
    if not wn_db_path.is_file():
        print('Downloading the Wordnet database...')
        wn.download('ewn:2020')
    
    print('Getting Wordnet entries...')
    cmd = 'sqlite3 %s "SELECT DISTINCT form FROM forms;" > %s' % (wn_db_path, WN_ENTRIES_FILE) 
    os.system(cmd)


def get_wordnet_data(word, pronunciations_list=None):
    words = wn.words(word)
    if words:
        pronunciation = ''
        if pronunciations_list is not None:
            pronunciation = get_pronunciation(word, pronunciations_list)
    
        word_data = {
            "pronunciation": pronunciation,
            "definitions": {}
        }

        for w in words:
            current_word = w.lemma()
            pos = PART_OF_SPEECH[w.pos]

            for synset in w.synsets():
                definition = synset.definition()
                synonyms = synset.lemmas()
                if current_word in synonyms: synonyms.remove(current_word)
                sentence = ''
                for example in synset.examples():
                    if example is not None:    
                        if current_word in example:
                            sentence = example
                            break
                        elif word in example:
                            sentence = example
                            break

                                
                word_data['definitions'].setdefault(pos, []).append({
                    "definition": definition,
                    "sentence": sentence
                })

        return word_data
    return None


def collect_all_data(pronunciations_list=None):
    setup()
    spinner = Halo(text='Collecting wordnet data...', spinner='dots')
    spinner.start()
    with open(WN_ENTRIES_FILE, 'r') as f:
        for line in f:
            word = line.rstrip()
            word_data = get_wordnet_data(word, pronunciations_list=pronunciations_list)
            dictionary[word] = word_data

        spinner.succeed("Done!")
        return dictionary

    spinner.fail("Something went wrong")
    return {}

if __name__ == '__main__':
    print("Wordnet Main")
