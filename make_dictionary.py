from dictionaryminer.wordnet import get_wordnet_data

with open('assets/cmu-pronunciations', 'r', encoding='utf-8') as pronun_file:
    pronunciations_list = pronun_file.readlines()
    data = get_wordnet_data('exciting', pronunciations_list=pronunciations_list)
    print(data)