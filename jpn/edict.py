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

def lookup(word, dictionary):
  '''Look up given word in Edict.
  '''
  #find entry with r_ele.reb that has contents equal to word
  e = dictionary.xpath(u'.//reb[text()="{word}"]'.format(word=word))
  return e


def main():
  parser = argparse.ArgumentParser(description='Look up japanese words via EDict.')
  parser.add_argument('words', nargs='*', help='Words to attempt stemming on')
  args = parser.parse_args()

  print('Loading edict...')

  dictionary = etree.parse('JMdict_e.gz')

  print('Edict loaded...')

  for word in args.words:
    hiragana = romaji2hiragana(word)
    results = lookup(hiragana, dictionary)
    if not results:
      print('No results found...')
    else:
      for result in results:
        print(etree.tostring(result.getparent().getparent(), pretty_print=True, encoding="UTF-8"))
        

if __name__ == "__main__":
  main()
