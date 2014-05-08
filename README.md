#jpn- Basic Japanese Support Library

jpn is a collection of tools i've started to put together after being frustrated with the problems with similar libraries floating around.
Those problems were:
* Inability to fully transliterate all roman characters to hiragana
* Improper handling of unicode/utf-8
* Inability to deinflect verbs for dictionary lookups

##Status
Library is currently small with the following modules:

###transliterate
Estimate (kunrei-shiki) hiragana or katakana representation of an input romaji string.

### deinflect
Estimate possible deinflected versions of input japanese word to aid in dictionary lookups.
