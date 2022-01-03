import argparse
from dictionaryminer.wordnet import collect_all_data
from dictionaryminer.webster import get_webster_definitions
from halo import Halo
import json
from pathlib import Path

ROOT_DIR = Path(__file__).parent
COMPLETE_DICTIONARY = Path.joinpath(ROOT_DIR, 'assets/complete_dictionary.json')

WEBSTER_DIRECTORY = Path.joinpath(ROOT_DIR, 'assets/webster-dict/')
WEBSTER_DICTIONARY = Path.joinpath(WEBSTER_DIRECTORY, 'webster_dictionary.json')
WORDNET_DIRECTORY = Path.joinpath(ROOT_DIR, 'assets/wordnet-dict/')
WORDNET_DICTIONARY = Path(WORDNET_DIRECTORY, 'wordnet_dictionary.json')

def make_webster_dict():
    print('Creating Webster Dictionary...')
    with open('assets/cmu-pronunciations', 'r', encoding='utf-8') as pronun_file:
        pronunciations_list = pronun_file.readlines()
        dictionary = get_webster_definitions(pronunciations_list=pronunciations_list)

    print('Finishing up...')
    with open(WEBSTER_DICTIONARY, 'w', encoding='utf-8') as dictionary_file:
        json.dump(dictionary, dictionary_file, indent=False, ensure_ascii=False, sort_keys=True)

    print('Successfully created at %s.' % WEBSTER_DICTIONARY)
    print('The Webster Dictionary contains %s entries.' % len(dictionary))


def make_wordnet_dict():
    print('Creating Wordnet Dictionary...')
    with open('assets/cmu-pronunciations', 'r', encoding='utf-8') as pronun_file:
        pronunciations_list = pronun_file.readlines()
        dictionary = collect_all_data(pronunciations_list=pronunciations_list)
    
    print('Finishing up...')
    with open(WORDNET_DICTIONARY, 'w', encoding='utf-8') as dictionary_file:
        json.dump(dictionary, dictionary_file, indent=False, ensure_ascii=False, sort_keys=True)
    
    print('Successfully created at %s.' % WORDNET_DICTIONARY)
    print('The Wordnet Dictionary contains %s entries.' % len(dictionary))


def make_complete_dict():
    print('Creating Complete Dictionary...', flush=True)
    if not WORDNET_DICTIONARY.is_file():
        print('Couldn\'t find Wordnet Dictionary')
        make_wordnet_dict()

    if not WEBSTER_DICTIONARY.is_file():
        print('Couldn\'t find Webster Dictionary')
        make_webster_dict()

    spinner = Halo(text='Collecting all data...', spinner='dots')
    spinner.start()
    with \
        open(WORDNET_DICTIONARY, 'r') as wordnetjson, \
        open(WEBSTER_DICTIONARY, 'r') as websterjson, \
        open(COMPLETE_DICTIONARY, 'w') as dictionary_file:
        
        wordnet = json.load(wordnetjson)
        webster = json.load(websterjson)

        extra_words_from_webster = webster.keys() - wordnet.keys()
        for word in extra_words_from_webster:
            wordnet[word] = webster[word]

        json.dump(wordnet, dictionary_file, indent=False, ensure_ascii=False, sort_keys=True)
    
    spinner.succeed("Done!")
    print('Successfully created at %s.' % COMPLETE_DICTIONARY)
    print('The Complete Dictionary contains %s words.' % len(wordnet.keys()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create an English dictionary for any purpose')
    parser.add_argument('--wordnet', help='Make a dictionary from Wordnet', action='store_true')
    parser.add_argument('--webster', help='Make a dictionary from Wordnet', action='store_true')
    args = parser.parse_args()
    
    if args.wordnet:
        make_wordnet_dict()
    elif args.webster:
        make_webster_dict()
    else:
        make_complete_dict()
    
