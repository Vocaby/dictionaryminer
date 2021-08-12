def binary_search_substring(pronunciations_list, search, separator):
    mid = int((len(pronunciations_list) - 1) / 2)
    return _binary_search_substring(pronunciations_list, search, 0, mid, len(pronunciations_list)-1, separator)


def _binary_search_substring(pronunciations_list, search, low, mid, high, separator):
    queried_word = search + separator
    if high >= low:
        a, b = pronunciations_list[mid].split(separator)
        if queried_word in pronunciations_list[mid] and len(a) == len(search):
            return pronunciations_list[mid].rstrip()

        if queried_word < pronunciations_list[mid]:
            high = mid - 1
        elif queried_word > pronunciations_list[mid]:
            low = mid + 1

        mid = int((low + high) / 2)
        return _binary_search_substring(pronunciations_list, search, low, mid, high, separator)

    return -1


def get_pronunciation(word, pronunciations_list):
    word = word.upper()
    line = binary_search_substring(pronunciations_list, word, '\t')
    if line == -1:
        return -1
    else:
        word, pronunciation = line.split('\t')
        return pronunciation.split(',')[0] # Some words have multiple pronunciations