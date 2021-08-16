from dictionaryminer.wordnet import collect_all_data
from dictionaryminer.webster import get_webster_definitions
import json

dictionary = {}
words = []

def make_webster_dict():
    with open('assets/cmu-pronunciations', 'r', encoding='utf-8') as pronun_file:
        pronunciations_list = pronun_file.readlines()
        dictionary = get_webster_definitions(pronunciations_list=pronunciations_list)
        words = dictionary.keys()

    with open('assets/webster-dict/webster_dictionary.json', 'w', encoding='utf-8') as dictionary_file, open('etc/webster_parsed_words.txt', 'w', encoding='utf-8') as words_file:
            json.dump(dictionary, dictionary_file, indent=False, ensure_ascii=False, sort_keys=True)
            words_file.write('\n'.join(words))

def make_wordnet_dict():
    with open('assets/cmu-pronunciations', 'r', encoding='utf-8') as pronun_file:
            pronunciations_list = pronun_file.readlines()
            dictionary = collect_all_data('etc/wn_words_no_duplicates.txt', pronunciations_list=pronunciations_list)

    with open('assets/wordnet-dict/wordnet_dictionary.json', 'w', encoding='utf-8') as dictionary_file:
            json.dump(dictionary, dictionary_file, indent=False, ensure_ascii=False, sort_keys=True)

def make_dict():
    print('Making dictionary... ', end='', flush=True)
    with \
        open('assets/wordnet-dict/wordnet_dictionary.json', 'r') as wordnetjson, \
        open('assets/webster-dict/webster_dictionary.json', 'r') as websterjson, \
        open('assets/dictionary.json', 'w') as dictionary_file:
        
        wordnet = json.load(wordnetjson)
        webster = json.load(websterjson)

        extra_words_from_webster = webster.keys() - wordnet.keys()
        for word in extra_words_from_webster:
            wordnet[word] = webster[word]

        json.dump(wordnet, dictionary_file, indent=False, ensure_ascii=False, sort_keys=True)
    print('Done \u2713')
    print('Dictionary contains %s words.' % len(wordnet.keys()))

if __name__ == '__main__':
    make_dict()