from collections import OrderedDict
import json
import re
import sys

import utils

def replace_combining_chars(s):
    s = s.replace('א\u05B7', 'אַ')
    s = s.replace('א\u05B8', 'אָ')
    s = s.replace('ב\u05BC', 'בּ')
    s = s.replace('ב\u05BF', 'בֿ')
    s = s.replace('ו\u05BC', 'וּ')
    s = s.replace('ו\u05B9', 'וֹ')
    s = s.replace('ו\u05BA', 'וֹ')
    s = s.replace('וו', 'װ');
    s = s.replace('וי', 'ױ');
    s = s.replace('י\u05B4', 'יִ')
    s = s.replace('יי', 'ײ');
    s = s.replace('יי\u05B7', 'ײַ')
    s = s.replace('ײ\u05B7', 'ײַ')
    s = s.replace('כ\u05BC', 'כּ')
    s = s.replace('פ\u05BC', 'פּ')
    s = s.replace('פ\u05BF', 'פֿ')
    s = s.replace('ש\u05C2', 'שׂ')
    s = s.replace('ת\u05BC', 'תּ')
    return s

def replace_pos(entry):
    new_entry = {}
    new_entry['eng'] = entry['eng']
    new_entry['_pro'] = entry['_pro']
    new_entry['_pos'] = []
    for pos in entry['_pos']:
        new_pos = pos
        if pos == '(adj.)':
            new_pos = 'adj'
        elif pos == '(adv.)':
            new_pos = 'adv'
        elif pos == '(f.)':
            new_pos = 'f'
        elif pos == '(m.)':
            new_pos = 'm'
        elif pos == '(n.)':
            new_pos = 'n'
        elif pos == '(name)':
            new_pos = 'name'
        new_entry['_pos'].append(new_pos)
    return new_entry

def normalize(input, output):
    # load the json into an object
    d = json.load(input)

    # normalize yiddish strings
    new_d = {}
    for yiddish in d:
        new_yiddish = replace_combining_chars(yiddish)
        new_entry = replace_pos(d[yiddish])
        if new_yiddish not in new_d:
            new_d[new_yiddish] = new_entry
        else:
            new_d[new_yiddish] = utils.combine_entries(new_entry, new_d[new_yiddish])

    # remove the empty key
    new_d.pop('', None)

    # sort the dictionary
    new_d = OrderedDict(sorted(new_d.items(), key=lambda i: utils.sort_yiddish(i[0])))

    # output the json
    json.dump(new_d, output, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as input, open(sys.argv[2], 'w', encoding='utf-8') as output:
        normalize(input, output)
