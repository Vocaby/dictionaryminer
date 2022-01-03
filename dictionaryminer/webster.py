from . import ROOT_DIR
from halo import Halo
from pathlib import Path
from .pronunciations import get_pronunciation

PART_OF_SPEECH = {
    'prep': 'preposition',
    'n': 'noun',
    'v': 'verb',
    'a': 'adjective',
    'adv': 'adverb',
    'conj': 'conjunction',
    'interj': 'interjection',
    'pron': 'pronoun'
}

dictionary = {}

def is_end(line):
    return line.rstrip() == '!E!'


def is_word_line(line):
    return line.isupper() and line.find('.') == -1


def is_definition_defn(line):
    return line[:5] == 'Defn:'


def get_definition(line, webster, definitions):
    # Definition always ends with the first period.
    # Short definition always ends with a semi-colon.
    lcounter = 0
    definition_found = False
    definition = ''

    while line and line != '\n' and definition_found == False:
        pcount = line.count('.')
        scount = line.count(';')
        line = line.rstrip()
        if line[0] == '[': break

        if pcount == 0 and scount == 0:
            definition += ' ' + line if lcounter > 0 else line
        elif pcount > 0:
            definition_found = True
            if '[Obs.]' in line:
                definition += ' ' + line[:line.find('[Obs.]')+6] if lcounter > 0 else line[:line.find('[Obs.]')+6]
            else:
                # Get long definition
                definition += ' ' + line[:line.find('.')+1] if lcounter > 0 else line[:line.find('.')+1]
        elif scount > 0:
            if line.find('; as') == -1:
                # Just return short def if available
                definition_found = True
                definition += ' ' + line[:line.find(';')] + '.' if lcounter > 0 else line[:line.find(';')] + '.'
            else:
                definition += ' ' + line if lcounter > 0 else line

        if not definition_found: line = webster.readline()
        lcounter += 1

    if definition: definitions.append({'definition': definition, 'sentence': ''})


def is_definition_num(line):
    return line[:1].isnumeric() and line[1:3] == '. '


def get_definition_num(line, webster, definitions):
    # Definition always ends with the first period.
    if line[0] == '(' and line.rstrip()[-1] == ')' or line.find(': [') != -1:
        line = webster.readline()
        if is_definition_letter(line):
            get_definition(line[3:], webster, definitions)
        else:
            get_definition(line, webster, definitions)
    else:
        get_definition(line, webster, definitions)


def is_definition_letter(line):
    if len(line) > 3:
        return line[0] == '(' and line[1].isalpha() and line[2] == ')'
    return False


def get_webster_definitions(pronunciations_list=None):
    spinner = Halo(text='Collecting webster data...', spinner='dots')
    spinner.start()
    
    with open(Path.joinpath(ROOT_DIR, 'assets/webster-dict/webster-full-raw'), 'r', encoding='utf-8') as webster:
        line = webster.readline()
        word = ''
        # Read lines until the end of file
        while(not is_end(line)):
            # Check if line is a word
            # Loop through the word body if not    
            while is_word_line(line):
                word = line.rstrip().lower()
                # print('Getting %s from Webster' % word, end='... ')
                line = webster.readline()

                # Parsing Part of Speech
                pos = ''
                pos_start = line.find(', ')
                pos_end = line.find('.')
                
                pos_exists = False
                word_variations = word.split(';')
                for i in range(0, len(word_variations)):
                    if pos_start != -1 and pos_end != -1 and pos_start < pos_end:
                        if line[pos_start+2:pos_end] in PART_OF_SPEECH:
                            pos = PART_OF_SPEECH[line[pos_start+2:pos_end]]
                            pos_exists = True
                            break
                    
                    pos_start = line.find(', ', pos_start+1)
                
                if not pos_exists:
                    # print("Empty Part Of Speech X")
                    break

                definitions = []
                ## Move and collect definitions until new word
                while not is_word_line(line):
                    if line != '\n':
                        if is_definition_num(line):
                            get_definition_num(line[line.find('. ')+2:], webster, definitions)
                        
                        if is_definition_letter(line):
                            get_definition(line[3:], webster, definitions)

                        if is_definition_defn(line):
                            line = line[6:]
                            if is_definition_letter(line):
                                line = line[3:].strip()
                            
                            get_definition(line, webster, definitions)
                    
                    line = webster.readline()
                    

                if len(definitions) > 0:
                    prev_variant = ''
                    for variant in word_variations:
                        variant = variant.strip()
                        pronunciation = ''
                        if pronunciations_list is not None:
                            pronunciation = get_pronunciation(variant, pronunciations_list)
                        # Some words have same variations in the Webster dict (e.g. Ampere)
                        if prev_variant != variant:
                            if variant in dictionary:
                                # Add on to the word object for different PoS
                                dictionary[variant]['definitions'].setdefault(pos, []).extend(definitions)
                            else:
                                # New word in the dictionary
                                dictionary[variant] = {
                                    'pronunciation': pronunciation,
                                    'definitions': {
                                        pos: definitions
                                    }
                                }

                            prev_variant = variant

                    # print("Done \u2713")
                else:
                    pass
                    # print("Empty Definition X")

            if not is_end(line):
                line = webster.readline()

    spinner.succeed("Done!")
    return dictionary
