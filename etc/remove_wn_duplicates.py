def remove_duplicate_words(file_location):
    counter = 0
    with open(file_location, 'r', encoding='utf-8') as word_file, open('assets/wn_words_no_duplicate.txt', 'w', encoding='utf-8') as new_file:
        read = ''
        for line in word_file.readlines():
            if line != read:
                new_file.write(line)
                
            read = line


if __name__ == '__main__':
    file_location = 'assets/wn_words.txt'
    remove_duplicate_words(file_location)