#jpn- Basic Japanese Support Library

jpn is a collection of tools i've started to put together after being frustrated with the problems with similar libraries floating around.
Those problems were:
* Inability to fully transliterate all roman characters to hiragana
* Improper handling of unicode/utf-8
* Inability to deinflect verbs for dictionary lookups

##Installation
Installation is currently only through git.
As usual it is suggested installing into a virtualev.
Installation can be carried out nicely as follows:
```
pip install -e git+https://github.com/johnoneil/jpn#egg=jpn
```

##Status
Library is currently small with the following modules:

###transliterate
Estimate (basically kunrei-shiki) hiragana or katakana representation of an input romaji string.
This can be done by importing the module and using its romaji2katakana or romaji2hiragana methods:
```
>>> from jpn.transliterate import romaji2katakana
>>> romaji2katakana(u'test')
u'\u30c6\u30b9\u30c4'
>>> print(romaji2katakana(u'test').encode('utf-8'))
テスツ
```
Note the following in the above. Input and output to the module methods *must be unicode*, so decode all strings before passing them as inputs.
Similarly, output is also unicode. Encode output to your encoding of choice to use (print) the output.
Also note that the transliteration to katakana above isn't perfect. For example i'd prefer 'test' to be transliterated to 'テスト' or something similar, but it does not do that currently. My initial goal is to transliterate simple romaji strings into hiragana for lookups rather than correctly render english words in Katakana.

Transliteration from Hiragana/Katakana to romaji is not currenty supported.


### deinflect
Estimate possible deinflected versions of input japanese word to aid in dictionary lookups.
