#!/usr/bin/env python
# coding: utf-8

# In[186]:


import csv
from collections import namedtuple
import re
import sys


# In[95]:


def flatten(l):
     return [item for sublist in l for item in sublist]


# In[176]:


ClozeCard = namedtuple('ClozeCard', 'id, tags, content')

def read_file(f):
    #with open(f, 'r') as fh:
    #    return fh.readlines()
    with open(f, newline='') as csvfile:
        return [ClozeCard(*r) for r in csv.reader(csvfile, delimiter='\t', quotechar='"')]


# In[179]:


def trim_inside(ls):
    return [l.strip() for l in ls]
    
def generate_cards(card):
    # TODO add `-` recognition
    if '1.' in card.content  and '{' not in card.content:
        lines = [l.rstrip("<br>") for l in card.content.splitlines()]
        lines_with_items = [trim_inside(l.split('.', 1)) for l in lines if len(l) > 0 and l[0].isdigit() or l.startswith('-')]
        headers = [l for l in lines if len(l) == 0 or (not l[0].isdigit() and not l.startswith('-'))]
        start_card_content = '<br>'.join(headers + [(n + ". {{c1::" + c + "}}" if idx == 0 else f"{n}. ...") for idx, (n, c) in enumerate(lines_with_items)])
        new_cards = [ClozeCard(**{**card._asdict(), 
                               "id": f"{card.id}_b",
                               "content": start_card_content})]
        
        for line_idx in range(1, len(lines_with_items)):
            new_lines = [[n, "..."] for (n, c) in lines_with_items]
            new_lines[line_idx - 1][1] = lines_with_items[line_idx - 1][1]
            new_lines[line_idx][1] = "{{c1::" + lines_with_items[line_idx][1] + "}}"
            new_cards += [ClozeCard(**{**card._asdict(), 
                               "id": f"{card.id}_{line_idx}",
                               "content": '<br>'.join(headers + [f"{n}. {c}" for n, c in new_lines])})]
            
        return new_cards
    else:
        return [card]


# In[187]:


def write_cards(cards, file_name):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['id', 'tags', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_ALL)

        for c in cards:
            writer.writerow(c._asdict())


# In[188]:


if __name__ == '__main__':
    #anki_card_path = '/home/sam/Dropbox/03_EPFL/01_courses/25_cellular-biology-for-engineers/anki_cards/cards.csv'
    if len(sys.argv) != 2:
        print("you have to give me a csv file")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    write_cards(flatten([generate_cards(l) for l in read_file(file_path)]), file_path[:-4] + "_mod.csv")


# In[ ]:




