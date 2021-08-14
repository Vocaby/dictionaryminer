from dictionaryminer.wordnet import collect_all_data
from dictionaryminer.webster import get_webster_definitions
import json

dictionary = {}
words = []

# with open('assets/cmu-pronunciations', 'r', encoding='utf-8') as pronun_file:
#     pronunciations_list = pronun_file.readlines()
#     dictionary, words = get_webster_definitions(pronunciations_list=pronunciations_list)

# with open('assets/webster-dict/webster_dictionary.json', 'w', encoding='utf-8') as dictionary_file, with open('etc/webster_parsed_words.txt', 'w', encoding='utf-8') as words_file:
#         json.dump(dictionary, dictionary_file, indent=False, ensure_ascii=False, sort_keys=True)
#         words_file.write('\n'.join(words))

# with open('assets/cmu-pronunciations', 'r', encoding='utf-8') as pronun_file:
#         pronunciations_list = pronun_file.readlines()
#         dictionary = collect_all_data('etc/wn_words_no_duplicates.txt', pronunciations_list=pronunciations_list)

# with open('assets/wordnet-dict/wordnet_dictionary.json', 'w', encoding='utf-8') as dictionary_file:
#         json.dump(dictionary, dictionary_file, indent=False, ensure_ascii=False, sort_keys=True)