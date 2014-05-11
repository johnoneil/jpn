#jpn- Basic Japanese Support Library

jpn is a collection of tools i've started to put together after being frustrated with the problems with similar libraries floating around.
Those problems were:
* Inability to fully transliterate all roman characters to hiragana
* Improper handling of unicode/utf-8
* Inability to deinflect verbs for dictionary lookups

That said, the library currently does the following
* Transliterates romaji (roman letter) strings into either Hiragana or Katakana. The basic mapping of characters is Kunrei-Shiki, but with some modificaitons to ensure robustness.
* Deinflect a given hiragana (unicode) string to guess at root words. This functionality is still very primitive, but it can provide estimates of both verb and adjective roots for simple cases like the polite, past, negative etc.
* Look up strings in the standard Edict japanese dictionary. This currently uses lxml for speed, but is still not ideal in its performance for anything other than command line use.

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

####jpn-transliterate
The package makes available a command line utility wrapper to carry out transliteration, 'jpn-transliterate'. Use is as below:
```
(jpn)joneil@joneilDesktop ~/code/jpn $ jpn-transliterate -h
usage: jpn-transliterate [-h] [-k] [words [words ...]]

Transliterate romaji to hiragana.

positional arguments:
  words           Words to transliterate

optional arguments:
  -h, --help      show this help message and exit
  -k, --katakana  Transliterate to katakana

(jpn)joneil@joneilDesktop ~/code/jpn $ jpn-transliterate -k testo
テスト

(jpn)joneil@joneilDesktop ~/code/jpn $ jpn-transliterate dokiniikimasuka?
どきにいきますか?
```


### deinflect
Estimate possible deinflected versions of input japanese word to aid in dictionary lookups.
This is a basic module that through the method "guess_stem' returns a list of unicode deinflection estimates for a given unicode input string. For example if we have the romaji string u'dekimasu' or the hiragana string u'できます' we'd like to be able to guess its root u'できる'. We can do this as show below.
```
>>> from jpn.deinflect import guess_stem
>>> guess_stem(u'できます')
(u'\u3067\u304d\u307e\u3059', u'\u3067\u304f', u'\u3067\u304d\u308b', u'\u3067\u304f\u308b')
>>> for stem in guess_stem(u'できます'):print(stem.encode('utf-8'));
... 
できます
でく
できる
でくる
```
Note (again) in the example above input and output *are always unicode.* Decode from and encode to your encoding of choice before using the exported method.
Also note that the module here provided several guesses as to possible roots. Some could be nonsense. Only a subsequent dictionary lookup will reveal which estimates are actual words and which arent.

#### jpn-deinflect
A command line wrapper is also included for this method. Simple invocation is as follows:
```
(jpn)joneil@joneilDesktop ~/code/jpn $ jpn-deinflect -h
usage: jpn-deinflect [-h] [words [words ...]]

Guess as uninflected stem of input japanese words (verbs or adjectives).

positional arguments:
  words       Words to attempt stemming on

optional arguments:
  -h, --help  show this help message and exit

(jpn)joneil@joneilDesktop ~/code/jpn $ jpn-deinflect kirimasu
きります
きる
きりる

(jpn)joneil@joneilDesktop ~/code/jpn $ jpn-deinflect akakunai
あかくない
あかい
あかくる

```
