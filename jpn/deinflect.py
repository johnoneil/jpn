#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# vim: set ts=2 expandtab:
'''
Module: deinflect.py
Desc: try to discern the stem of japanese inflected words to aid in lookups.
Author: john.oneil  
Email: oneil.john@gmail.com
DATE: Wed May 7th 2014

  
'''
import os
import argparse
import re

from transliterate import romaji2hiragana


class VerbalTransform:
  def __init__(self, root, polite_ending, negative_ending, te_ending, perfect_ending):
    self.root = root
    self.polite = polite_ending
    self.negative = negative_ending
    self.te = te_ending
    self.perfect = perfect_ending

  def Polite(self, hiragana):
    if re.search(self.polite, hiragana):
      return re.sub(self.polite, self.root, hiragana)
    else:
      return None

  def Negative(self, hiragana):
    if re.search(self.negative, hiragana):
      return re.sub(self.negative, self.root, hiragana)
    else:
      return None

  def Te(self, hiragana):
    if re.search(self.te, hiragana):
      return re.sub(self.te, self.root, hiragana)
    else:
      return None

  def Perfect(self, hiragana):
    if re.search(self.perfect, hiragana):
      return re.sub(self.perfect, self.root, hiragana)
    else:
      return None 

VerbalTransforms = [
  VerbalTransform(u'う', ur'います$', ur'わない$', ur'って$', ur'った$'),
  VerbalTransform(u'つ', ur'ちます$', ur'たない$', ur'って$', ur'った$'),
  VerbalTransform(u'る', ur'ります$', ur'らない$', ur'って$', ur'った$'),
  VerbalTransform(u'く', ur'きます$', ur'かない$', ur'いて$', ur'いた$'),
  VerbalTransform(u'ぐ', ur'ぎます$', ur'がない$', ur'いで$', ur'いだ$'),
  VerbalTransform(u'ぬ', ur'にます$', ur'なない$', ur'んで$', ur'んだ$'),
  VerbalTransform(u'ぶ', ur'びます$', ur'ばない$', ur'んで$', ur'んだ$'),
  VerbalTransform(u'む', ur'みます$', ur'まない$', ur'んで$', ur'んだ$'),
  VerbalTransform(u'す', ur'します$', ur'さない$', ur'して$', ur'した$'),

  VerbalTransform(u'る', ur'ます$', ur'ない$', ur'て$', ur'た$'),
  #VerbalTransform(u'る', ur'ます$', ur'ない$', ur'て$', ur'た$'),

  VerbalTransform(u'する', ur'しない$', ur'しない$', ur'して$', ur'した$'),
  VerbalTransform(u'くる', ur'きます$', ur'こない$', ur'きて$', ur'きた$'),
]


def guess_stem(word):
  """given single input word, try to discern japanese word stem
  """
  #1. input word should have no spaces
  word = word.strip().lower()

  #2b Convert filtered word to hiragana via romkan
  hiragana = romaji2hiragana(word.decode('utf-8'))
  results = [hiragana]

  #3: We've got a simple single word in hiragana. First test against adjectival endings

  #4: No hits for adjetive stem, test against verbal endings
  for tx in VerbalTransforms:
    polite = tx.Polite(hiragana)
    if polite: results.append(polite)
    negative = tx.Negative(hiragana)
    if negative: results.append(negative)
    te = tx.Te(hiragana)
    if te: results.append(te)
    perfect = tx.Perfect(hiragana)
    if perfect: results.append(perfect)

  #5: Return input word and candidate stems as tuple, to do dictionary lookups on all.
  #The best hit will be the longest(?) exact match of a suggested stem
  return tuple(results)


def main():
  parser = argparse.ArgumentParser(description='Guess as uninflected stem of input japanese words (verbs or adjectives).')
  parser.add_argument('words', nargs='*', help='Words to attempt stemming on')
  args = parser.parse_args()

  for word in args.words:
    results = guess_stem(word)
    for result in results:
      print result
        

if __name__ == "__main__":
  main()
