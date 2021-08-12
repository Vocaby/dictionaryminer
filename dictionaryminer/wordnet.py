import wn
import json
from . import ROOT_DIR
from pathlib import Path
from .pronunciations import get_pronunciation

WN_DATA_DIRECTORY = Path.joinpath(ROOT_DIR, 'assets/dictionary-raw')
WN_WORDS_FILE = Path.joinpath(ROOT_DIR, 'assets/wn_words_no_duplicate.txt')

wn.config.data_directory = WN_DATA_DIRECTORY

PART_OF_SPEECH = {
    'n': 'noun',
    'v': 'verb',
    'a': 'adjective',
    's': 'adjective',
    'r': 'adverb'
}

dictionary = []

def setup():
    if not Path(WN_DATA_DIRECTORY, 'wn.db').is_file():
        print("Downloading the Wordnet database...")
        wn.download('ewn:2020')
    else:
        print("Hello")

def get_wordnet_data(word, pronunciations_list=None):
    words = wn.words(word)
    if words:
        pronunciation = ''
        if pronunciations_list is not None:
            pronunciation = get_pronunciation(word, pronunciations_list)
    
        word_data = {
            "word": word,
            "pronunciation": pronunciation,
            "definitions": {}
        }

        print('Getting %s from Wordnet' % word, end="... ")
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

        print("Done \u2713")
        return word_data
    return None


def collect_all_data(words_file, pronunciations_list=None):
    with open(words_file, 'r') as f:
        print('Collecting wordnet data...')
        for line in f:
            word = line.rstrip()
            word_data = get_wordnet_data(word, pronunciations_list=pronunciations_list)
            dictionary.append(word_data)
            
        return dictionary


setup()
if __name__ == '__main__':
    # collect_all_data(WN_WORDS_FILE)
    # print('Writing dictionary.json and words.txt')
    # with open('wordnet_dictionary.json', 'w', encoding='utf-8') as dictionary_file:
    #     json.dump(dictionary, dictionary_file, indent = True, ensure_ascii=True, sort_keys=True)
    print("Hello")