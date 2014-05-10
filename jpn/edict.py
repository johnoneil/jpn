#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# vim: set ts=2 expandtab:
'''
Module: edict.py
Desc: Wrapper for the traditional jpn Edict dictionary.
Author: john.oneil  
Email: oneil.john@gmail.com
DATE: Friday May 9th 2014

Example EDict entry (for structure)
<entry>
  <ent_seq>1000280</ent_seq>
  <k_ele>
    <keb>論う</keb>
  </k_ele>
  <r_ele>
    <reb>あげつらう</reb>
  </r_ele>
  <sense>
    <pos>&v5u;</pos>
    <pos>&vt;</pos>
    <misc>&uk;</misc>
    <gloss>to discuss</gloss>
  </sense>
  <sense>
    <gloss>to find fault with</gloss>
    <gloss>to criticize</gloss>
    <gloss>to criticise</gloss>
  </sense>
</entry>
  
'''
import os
import argparse
import re

from transliterate import romaji2hiragana
from deinflect import guess_stem
from lxml import etree
from jpn.exceptions import NonUnicodeInputException

def lookup(word, dictionary):
  '''Look up given word in Edict.
  '''
  #ensure input is a unicode string
  if not isinstance(word, unicode):
    raise NonUnicodeInputException('Input argument {word} is not unicode.'.format(word=word))

  results = []
  hiragana_hits = dictionary.xpath(u'//reb[starts-with(text(),"{word}")]'.format(word=word))
  if hiragana_hits:
    hiragana_hits = [x.getparent().getparent() for x in hiragana_hits]
    results.extend(hiragana_hits)

  kanji_hits = dictionary.xpath(u'//keb[starts-with(text(),"{word}")]'.format(word=word))
  if kanji_hits:
    kanji_hits = [x.getparent().getparent() for x in kanji_hits]
    results.extend(kanji_hits)

  return results

def format_entry(entry):
  '''Format an etree object (containing edict data) for printing
  '''
  print(etree.tostring(entry, pretty_print=True, encoding="UTF-8"))


def main():
  parser = argparse.ArgumentParser(description='Look up japanese words via EDict.')
  parser.add_argument('words', nargs='*', help='Words to attempt stemming on')
  args = parser.parse_args()

  edict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'JMdict_e.gz')
  dictionary = etree.parse(edict_path)

  for word in args.words:
    #best practice: to decode early, encode late
    word = word.decode('utf-8')
    hiragana = romaji2hiragana(word)
    results = lookup(hiragana, dictionary)
    if not results:
      print('No results found...')
      possible_hits = guess_stem(hiragana)
      if possible_hits:
        print('Perhaps you meant one of the following:')
        print(', '.join(possible_hits))
    else:
      for result in results:
        format_entry(result)
        

if __name__ == "__main__":
  main()
