# :scroll: dictionaryminer
Free English dictionary available for any use (personal or commercial). The current dictionary has definitions for over 210,000+ words.

Contributions are encouraged and welcomed! 

## Usage
```shell
$ python make_dictionary.py
$ python make_dictionary.py --webster
$ python make_dictionary.py --wordnet
```

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
The dictionary json files will be created inside the [assets folder](assets/).

## Sources
1. Definition, Part of Speech, Sentence: [Wordnet (Princeton Wordnet License)](https://wordnet.princeton.edu/)
    - The project uses the [wn](https://github.com/goodmami/wn) Python library by Michael Wayne Goodman et al.
2. Definition, Part of Speech, Sentence: [Websters's Unabridged Dictionary (Public Domain)](https://www.gutenberg.org/ebooks/29765)
3. Pronunciations: [The CMU Pronouncing Dictionary (Carnegie Mellon University)](http://www.speech.cs.cmu.edu/cgi-bin/cmudict)
    - [IPA conversion](https://github.com/menelik3/cmudict-ipa) 
