import re 
import unicodedata

"""
Reads in terra_pinyin.dict.yaml and essay.txt and prints entries to a new file. 
Each line in the new file has the following three values separated by tabs: 
1. properly tone-marked pinyin (word)
2. pinyin spaced by syllable without tone markings (input code)
3. integer weight 

e.g. 
píng’ān    ping an    100

Resources: 
- https://github.com/rime/home/wiki/CustomizationGuide
- https://github.com/rime/home/wiki/RimeWithSchemata
- https://github.com/LEOYoon-Tsaw/Rime_collections/blob/master/Rime_description.md
"""

# baguwen reference data: set of words with pronunciations specified 
# (no need to build pronunciations)
specified_romanizations = {} 

# baguwen reference data: dict of character pronunciations to build words
character_dict = {} 

# scan terra_pinyin and build baguwen reference data 
# file from https://github.com/rime/rime-terra-pinyin
with open('terra_pinyin.dict.yaml') as f:
    for line in f: 
        if '\t' in line: 
            line = line.replace('\n', '')
            vals = line.split('\t')
            characters, romanization = vals[:2]
            percentage = int(float(vals[2].replace('%', ''))) if len(vals) > 2 else 100

            # strip midpoints 
            # (these should ideally be rendered as spaces, but are ignored for now)
            characters = characters.replace("·", "")

            # amend tones of '一'
            yi_indices = [m.start() for m in re.finditer('一', characters)]
            tone_indices = [m.start() for m in re.finditer('[0-9]', romanization)]
            for index in yi_indices: 
                tone_index = tone_indices[index]
                romanization = romanization[:tone_index] + '1' + romanization[tone_index+1:]

            # amend tones of '不'
            bu_indices = [m.start() for m in re.finditer('不', characters)]
            for index in bu_indices: 
                tone_index = tone_indices[index]
                romanization = romanization[:tone_index] + '4' + romanization[tone_index+1:]

            # build specified_romanizations
            if characters not in specified_romanizations: 
                specified_romanizations[characters] = [romanization]
            else: 
                specified_romanizations[characters].append(romanization)

            # build character_dict
            # special case for 個 ge5, whose percentage is 0 for some reason 
            if len(characters) == 1 and (percentage > 5 or characters == '個'):
                if characters not in character_dict: 
                    character_dict[characters] = [romanization]
                else: 
                    character_dict[characters].append(romanization)

# set of romanized words to write to final file 
romanization_set = set()

# dict of weights for each romanization
weights_dict = {}

# add words from baguwen 
# file from https://github.com/rime/rime-essay
with open('essay.txt') as baguwen: 
    for line in baguwen: 
        characters, weight = line.split('\t')[:2]
        weight = int(weight)

        # add words with specified romanizations
        if characters in specified_romanizations: 
            for r in specified_romanizations[characters]:
                romanization_set.add(r)
                if r not in weights_dict: 
                    weights_dict[r] = weight 
                else: 
                    weights_dict[r] += weight 

        # build pronunciations if word not in specified_romanizations 
        # (i.e. don't have pronunciations specified)
        else: 
            romanizations_so_far = ['']
            failed = False 
            for char in characters: 
                if char not in character_dict: 
                    failed = True
                    break 
                new_romanizations = []
                for word_romanization in romanizations_so_far: 
                    if len(word_romanization) > 0: 
                        word_romanization += ' '
                    for romanization in character_dict[char]: 
                        new_romanizations.append(word_romanization + romanization)
                romanizations_so_far = new_romanizations
            if not failed: 
                for r in romanizations_so_far: 
                    romanization_set.add(r)
                    if r not in weights_dict: 
                        weights_dict[r] = weight 
                    else: 
                        weights_dict[r] += weight 

# alphabetize 
romanization_list = sorted(romanization_set) 

# tones dictionary of combining diacritical marks, used for marking tones 
# https://en.wikipedia.org/wiki/Combining_character
tones = {
    '1': '\u0304',
    '2': '\u0301', 
    '3': '\u030c', 
    '4': '\u0300'
}

# prepare entries and write to output file 
with open('lumen_pinyin.dict.yaml', 'w') as output: 
    output.write(
"""# Rime dictionary
# encoding: utf-8
#
# Lumen Pinyin - 光耀拼音
#
#   William Pan <wpan@berkeley.edu>
#

---
name: lumen_pinyin
version: "2020.07.04"
sort: by_weight
use_preset_vocabulary: false
...
    
""") 

    for entry in romanization_list: 
        input_code = '' 
        word = '' # word in pinyin 
        alt_word = '' # alt_word with hyphen (only built if word is four syllables)

        syllables = entry.split(' ')
        for index, syllable in enumerate(syllables): 
            toneless, tone = syllable[:-1], syllable[-1:]

            # mark tones
            if tone == '5': 
                marked = toneless.replace('v', 'ü')
            else: 
                if 'e' in toneless: 
                    vowel = 'e'
                elif 'a' in toneless: 
                    vowel = 'a'
                elif 'ou' in toneless: 
                    vowel = 'o'
                else: 
                    # final vowel takes the mark 
                    vowel = re.findall(r'[aeiouv]', toneless)[-1]
                display_vowel = 'ü' if vowel == 'v' else vowel 
                composed = unicodedata.normalize('NFC', display_vowel + tones[tone])
                marked = toneless.replace(vowel, composed).replace('v', 'ü')

            # add syllable to input code 
            if len(input_code) > 0: 
                input_code += ' '
            input_code += toneless

            # add syllable to word
            if len(word) > 0 and toneless[0] in 'aeo': 
                word += '’'
            word += marked

            # if four-syllable word, add syllable to alt_word
            if len(syllables) == 4: 
                if index == 2:
                    alt_word += '-'
                elif len(alt_word) > 0 and toneless[0] in 'aeo': 
                    alt_word += '’'
                alt_word += marked 
            
        # add entry to dictionary file
        output.write(
            word.capitalize() + '\t' + 
            input_code.capitalize() + '\t' + 
            str(weights_dict[entry]) + '\n'
        )
        output.write(
            word + '\t' + 
            input_code + '\t' + 
            str(weights_dict[entry]) + '\n'
        )

        # if alt_word exists, add to dictionary file
        if alt_word: 
            output.write(
                alt_word.capitalize() + '\t' + 
                input_code.capitalize() + '\t' + 
                str(weights_dict[entry]) + '\n'
            )
            output.write(
                alt_word + '\t' + 
                input_code + '\t' + 
                str(weights_dict[entry]) + '\n'
            )
