# Free-English-Dictionary
:book: Free English dictionary available for any use

## Data Structure
```json
{
    "word" : {
        "pronunciation": "Some pronunciation",
        "definitions": {
            "noun": [
                        {
                            "definition": "Some definition",
                            "sentence": "Some sentence"
                        },
                        {
                            "definition": "Another definition",
                            "sentence": "Another sentence",
                        }
                    ],
            "verb": [
                        {
                            "definition": "Some definition",
                            "sentence": "Some sentence"
                        },
                        {
                            "definition": "Another definition",
                            "sentence": "Another sentence",
                        }
                    ]
        }
    }
}
```

## Output Files
The formatted dictionary json files inside the [assets folder](assets/). Words that are included in the dictionaries are inside the [etc folder](etc/). The parsed Webster dictionary file is [webster_dictionary.json](assets/webster-dict/webster_dictionary.json). The Wordnet dictionary file is [wordnet_dictionary.json](assets/wordnet-dict/wordnet_dictionary.json). The all-in-one dictionary is being worked on.

## Some Useful Commands
To see the number of words that's in the Webster dictionary but not in Wordnet, use the command below:

`awk 'FNR==NR {a[$0]++; next} !($0 in a)' assets/wn_words_no_duplicates.txt assets/webster_parsed_words.txt | wc -l`

## Sources
1. Definition, Part of Speech, Sentence: [Wordnet (Princeton Wordnet License)](https://wordnet.princeton.edu/)
    - The project uses the [wn](https://github.com/goodmami/wn) Python library by Michael Wayne Goodman et al.
2. Definition, Part of Speech, Sentence: [Websters's Unabridged Dictionary (Public Domain)](https://www.gutenberg.org/ebooks/29765)
3. Pronunciations: [The CMU Pronouncing Dictionary (Carnegie Mellon University)](http://www.speech.cs.cmu.edu/cgi-bin/cmudict)
    - [IPA conversion](https://github.com/menelik3/cmudict-ipa) 