#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# vim: set ts=2 expandtab:
'''
Module: transliterate.py
Desc: Transliterate using (modified)kunrei-shiki romanizations
Author: john.oneil  
Email: oneil.john@gmail.com
DATE: Wed May 7th 2014

Writing this module because of current defficiencies in the romkan and jTransliterate packages.
  
'''
import os
import argparse
import re

from jpn.exceptions import NonUnicodeInputException

#based on http://en.wikipedia.org/wiki/Kunrei-shiki_romanization
TRANSLITERATION_TABLE = {
u'a' :[u'あ',u'ア'], u'i':[u'い', u'イ'],u'u':[u'う',u'ウ'], u'e':[u'え',u'エ'], u'o':[u'お',u'オ'],
u'ka':[u'か',u'カ'], u'ki':[u'き',u'キ'], u'ku':[u'く',u'ク'], u'ke':[u'け',u'ケ'], u'ko':[u'こ',u'コ'], u'kya':[u'きゃ',u'キャ'], u'kyu':[u'きゅ',u'キュ'], u'kyo':[u'きょ',u'キョ'], 
u'ca':[u'か',u'カ'], u'ci':[u'き',u'キ'], u'cu':[u'く',u'ク'], u'ce':[u'け',u'ケ'], u'co':[u'こ',u'コ'], u'cya':[u'きゃ',u'キャ'], u'cyu':[u'きゅ',u'キュ'], u'cyo':[u'きょ',u'キョ'], 
u'sa':[u'さ',u'サ'], u'si':[u'し',u'シ'], u'su':[u'す',u'ス'], u'se':[u'せ',u'セ'], u'so':[u'そ',u'ソ'], u'sya':[u'しゃ',u'シャ'], u'syu':[u'しゅ',u'シュ'], u'syo':[u'しょ',u'ショ'], 
u'ta':[u'た',u'タ'], u'ti':[u'ち',u'チ'], u'tu':[u'つ',u'ツ'], u'te':[u'て',u'テ'], u'to':[u'と',u'ト'], u'tya':[u'ちゃ',u'チャ'], u'tyu':[u'ちゅ',u'チュ'], u'tyo':[u'ちょ',u'チョ'], 
u'na':[u'な',u'ナ'], u'ni':[u'に',u'ニ'], u'nu':[u'ぬ',u'ヌ'], u'ne':[u'ね',u'ネ'], u'no':[u'の',u'ノ'], u'nya':[u'にゃ',u'ニャ'], u'nyu':[u'にゅ',u'ニュ'], u'nyo':[u'にょ',u'ニョ'], 
u'ha':[u'は',u'ハ'], u'hi':[u'ひ',u'ヒ'], u'hu':[u'ふ',u'フ'], u'he':[u'へ',u'ヘ'], u'ho':[u'ほ',u'ホ'], u'hya':[u'ひゃ',u'ヒャ'], u'hyu':[u'ひゅ',u'ヒュ'], u'hyo':[u'ひょ',u'ヒョ'], 
u'fa':[u'は',u'ハ'], u'fi':[u'ひ',u'ヒ'], u'fu':[u'ふ',u'フ'], u'fe':[u'へ',u'ヘ'], u'fo':[u'ほ',u'ホ'], u'fya':[u'ひゃ',u'ヒャ'], u'fyu':[u'ひゅ',u'ヒュ'], u'fyo':[u'ひょ',u'ヒョ'], 
u'ma':[u'ま',u'マ'], u'mi':[u'み',u'ミ'], u'mu':[u'む',u'ム'], u'me':[u'め',u'メ'], u'mo':[u'も',u'モ'], u'mya':[u'みゃ',u'ミャ'], u'myu':[u'みゅ',u'ミュ'], u'myo':[u'みょ',u'ミョ'], 
u'ya':[u'や',u'ヤ'], u'yu':[u'ゆ',u'ユ'], u'yo':[u'よ',u'ヨ'],  
u'ra':[u'ら',u'ラ'], u'ri':[u'り', u'リ'], u'ru':[u'る',u'ル'], u're':[u'れ',u'レ'], u'ro':[u'ろ',u'ロ'], u'rya':[u'りゃ',u'リャ'], u'ryu':[u'りゅ',u'リュ'], u'ryo':[u'りょ',u'リョ'], 
u'la':[u'ら',u'ラ'], u'li':[u'り', u'りリ'], u'lu':[u'る',u'ル'], u'le':[u'れ',u'レ'], u'lo':[u'ろ',u'ロ'], u'lya':[u'りゃ',u'リャ'], u'lyu':[u'りゅ',u'リュ'], u'lyo':[u'りょ',u'リョ'], 
u'wa':[u'わ',u'ワ'], #u'o':[u'を',u'ヲ'], #u'i':[u'ヰ', u'ゐ '], u'e':[u'ゑ',u'ヱ']
u'n' :[u'ん',u'ン'],  
u'ga':[u'が',u'ガ'], u'gi':[u'ぎ',u'ギ'], u'gu':[u'ぐ',u'グ'], u'ge':[u'げ',u'ゲ'], u'go':[u'ご',u'ゴ'], u'gya':[u'ぎゃ', u'ギャ'], u'gyu':[u'ぎゅ',u'ギュ'] ,u'gyo':[u'ぎょ',u'ギョ'], 
u'za':[u'ざ',u'ザ'], u'zi':[u'じ',u'ジ'], u'zu':[u'ず',u'ズ'], u'ze':[u'ぜ',u'ゼ'], u'zo':[u'ぞ',u'ゾ'], u'zya':[u'じゃ', u'ジャ'], u'zyu':[u'じゅ',u'ジュ'] ,u'zyo':[u'じょ',u'ジョ'], 
u'ja':[u'じゃ',u'ジャ'], u'ji':[u'じ',u'ジ'], u'ju':[u'じゅ',u'ジュ'], u'je':[u'ぜ',u'ゼ'], u'jo':[u'じょ',u'ジョ'], u'jya':[u'じゃ', u'ジャ'], u'jyu':[u'じゅ',u'ジュ'] ,u'jyo':[u'じょ',u'ジョ'], 
u'da':[u'だ',u'ダ'], u'zi':[u'ぢ',u'ヂ'], u'zu':[u'づ',u'ヅ'], u'de':[u'で',u'デ'], u'do':[u'ど',u'ド'], u'zya':[u'ぢゃ', u'ヂャ'], u'zyu':[u'ぢゅ',u'ヂュ'] ,u'zyo':[u'ぢょ',u'ヂョ'], 
u'ba':[u'ば',u'バ'], u'bi':[u'び',u'ビ'], u'bu':[u'ぶ',u'ブ'], u'be':[u'べ',u'ベ'], u'bo':[u'ぼ',u'ボ'], u'bya':[u'びゃ', u'ビャ'], u'byu':[u'びゅ',u'ビュ'] ,u'byo':[u'びょ',u'ビョ'], 
u'pa':[u'ぱ',u'パ'], u'pi':[u'ぴ',u'ピ'], u'pu':[u'ぷ',u'プ'], u'pe':[u'ぺ',u'ペ'], u'po':[u'ぽ',u'ポ'], u'pya':[u'ぴゃ', u'ピャ'], u'pyu':[u'ぴゅ',u'ピュ'] ,u'pyo':[u'ぴょ',u'ピョ'], 

#doubled consonants
u'kka':[u'っか',u'ッカ'], u'kki':[u'っき', u'ッキ'], u'kku':[u'っく',u'ック'], u'kke':[u'っけ',u'ッケ'], u'kko':[u'っこ',u'ッコ'], u'kkya':[u'っきゃ',u'ッキャ'], u'kkyu':[u'っきゅ',u'ッキュ'], u'kkyo':[u'っきょ',u'ッキョ'], 
u'cca':[u'っか',u'ッカ'], u'cci':[u'っき', u'ッキ'], u'ccu':[u'っく',u'ック'], u'cce':[u'っけ',u'ッケ'], u'cco':[u'っこ',u'ッコ'], u'ccya':[u'っきゃ',u'ッキャ'], u'ccyu':[u'っきゅ',u'ッキュ'], u'ccyo':[u'っきょ',u'ッキョ'], 
u'ssa':[u'っさ',u'ッサ'], u'ssi':[u'っし', u'ッシ'], u'ssu':[u'っす',u'ッス'], u'sse':[u'っせ',u'ッセ'], u'sso':[u'っそ',u'ッソ'], u'ssya':[u'っしゃ',u'ッシャ'], u'ssyu':[u'っしゅ',u'ッシュ'], u'ssyo':[u'っしょ',u'ッショ'], 
u'tta':[u'った',u'ッタ'], u'tti':[u'っち', u'ッチ'], u'ttu':[u'っつ',u'ッツ'], u'tte':[u'って',u'ッテ'], u'tto':[u'っと',u'ット'], u'ttya':[u'っちゃ',u'ッチャ'], u'ttyu':[u'っちゅ',u'ッチュ'], u'ttyo':[u'っちょ',u'ッチョ'], 
u'nna':[u'っな',u'ッナ'], u'nni':[u'っに', u'ッニ'], u'nnu':[u'っぬ',u'ッヌ'], u'nne':[u'っね',u'ッネ'], u'nno':[u'っの',u'ッノ'], u'nnya':[u'っにゃ',u'ッニャ'], u'nnyu':[u'っにゅ',u'ッニュ'], u'nyo':[u'っにょ',u'ッニョ'], 
u'hha':[u'っは',u'ッハ'], u'hhi':[u'っひ', u'ッヒ'], u'hhu':[u'っふ',u'ッフ'], u'hhe':[u'っへ',u'ッヘ'], u'hho':[u'っほ',u'ッホ'], u'hhya':[u'っひゃ',u'ッヒャ'], u'hhyu':[u'っひゅ',u'ッヒュ'], u'hhyo':[u'っひょ',u'ッヒョ'], 
u'mma':[u'っま',u'ッマ'], u'mmi':[u'っみ', u'ッミ'], u'mmu':[u'っむ',u'ッム'], u'mme':[u'っめ',u'ッメ'], u'mmo':[u'っも',u'ッモ'], u'mmya':[u'っみゃ',u'ッミャ'], u'mmyu':[u'っみゅ',u'ッミュ'], u'mmyo':[u'っみょ',u'ッミョ'], 
u'rra':[u'っら',u'ッラ'], u'rri':[u'っり', u'ッリ'], u'rru':[u'っる',u'ッル'], u'rre':[u'っれ',u'ッレ'], u'rro':[u'っろ',u'ッロ'], u'rrya':[u'っりゃ',u'ッリャ'], u'rryu':[u'っりゅ',u'ッリュ'], u'rryo':[u'っりょ',u'ッリョ'], 
u'lla':[u'っら',u'ッラ'], u'lli':[u'っり', u'ッリ'], u'llu':[u'っる',u'ッル'], u'lle':[u'っれ',u'ッレ'], u'llo':[u'っろ',u'ッロ'], u'llya':[u'っりゃ',u'ッリャ'], u'llyu':[u'っりゅ',u'ッリュ'], u'llyo':[u'っりょ',u'ッリョ'], 
u'nn' :[u'っん',u'ン'],  
u'gga':[u'っが',u'ッガ'], u'ggi':[u'っぎ',u'ッギ'], u'ggu':[u'っぐ',u'ッグ'], u'gge':[u'っげ',u'ッゲ'], u'ggo':[u'っご',u'ッゴ'], u'ggya':[u'っぎゃ', u'ッギャ'], u'ggyu':[u'っぎゅ',u'ッギュ'] ,u'ggyo':[u'っぎょ',u'ッギョ'], 
u'zza':[u'っざ',u'ッザ'], u'zzi':[u'っじ',u'ッジ'], u'zzu':[u'っず',u'ッズ'], u'zze':[u'っぜ',u'ッゼ'], u'zzo':[u'っぞ',u'ッゾ'], u'zzya':[u'っじゃ', u'ッジャ'], u'zzyu':[u'っじゅ',u'ッジュ'] ,u'zzyo':[u'っじょ',u'ッジョ'], 
u'dda':[u'っだ',u'ッダ'], u'zzi':[u'っぢ',u'ッヂ'], u'zzu':[u'っづ',u'ッヅ'], u'dde':[u'っで',u'ッデ'], u'ddo':[u'っど',u'ッド'], u'zzya':[u'っぢゃ', u'ッヂャ'], u'zzyu':[u'っぢゅ',u'ッヂュ'] ,u'zzyo':[u'っぢょ',u'ッヂョ'], 
u'bba':[u'っば',u'ッバ'], u'bbi':[u'っび',u'ッビ'], u'bbu':[u'っぶ',u'ッブ'], u'bbe':[u'っべ',u'ッベ'], u'bbo':[u'っぼ',u'ッボ'], u'bbya':[u'っびゃ', u'ッビャ'], u'bbyu':[u'っびゅ',u'ッビュ'] ,u'bbyo':[u'っびょ',u'ッビョ'], 
u'ppa':[u'っぱ',u'ッパ'], u'ppi':[u'っぴ',u'ッピ'], u'ppu':[u'っぷ',u'ップ'], u'ppe':[u'っぺ',u'ッペ'], u'ppo':[u'っぽ',u'ッポ'], u'ppya':[u'っぴゃ', u'ッピャ'], u'ppyu':[u'っぴゅ',u'ッピュ'] ,u'ppyo':[u'っぴょ',u'ッピョ'], 

#doubled vowels
u'aa' :[u'ああ',u'アー'], u'ii':[u'いい', u'イー'],u'uu':[u'うう',u'ウー'], u'ee':[u'ええ',u'エー'], u'oo':[u'おお',u'オー'],
u'kaa':[u'かあ',u'カー'], u'kii':[u'きい',u'キー'], u'kuu':[u'くう',u'クー'], u'kee':[u'けえ',u'ケー'], u'koo':[u'こお',u'コー'], u'kyaa':[u'きゃあ',u'キャー'], u'うkyuu':[u'きゅう',u'キュー'], u'kyoo':[u'きょお',u'キョー'], 
u'caa':[u'かあ',u'カー'], u'cii':[u'きい',u'キー'], u'cuu':[u'くう',u'クー'], u'cee':[u'けえ',u'ケー'], u'coo':[u'こお',u'コー'], u'cyaa':[u'きゃあ',u'キャー'], u'うcyuu':[u'きゅう',u'キュー'], u'cyoo':[u'きょお',u'キョー'], 
u'saa':[u'さあ',u'サー'], u'sii':[u'しい',u'シー'], u'suu':[u'すう',u'スー'], u'see':[u'せえ',u'セー'], u'soo':[u'そお',u'ソー'], u'syaa':[u'しゃあ',u'シャー'], u'うsyuu':[u'しゅう',u'シュー'], u'syoo':[u'しょお',u'ショー'], 
u'taa':[u'たあ',u'ター'], u'tii':[u'ちい',u'チー'], u'tuu':[u'つう',u'ツー'], u'tee':[u'てえ',u'テー'], u'too':[u'とお',u'トー'], u'tyaa':[u'ちゃあ',u'チャー'], u'うtyuu':[u'ちゅう',u'チュー'], u'tyoo':[u'ちょお',u'チョー'], 
u'naa':[u'なあ',u'ナー'], u'nii':[u'にい',u'ニー'], u'nuu':[u'ぬう',u'ヌー'], u'nee':[u'ねえ',u'ネー'], u'noo':[u'のお',u'ノー'], u'nyaa':[u'にゃあ',u'ニャー'], u'うnyuu':[u'にゅう',u'ニュー'], u'nyoo':[u'にょお',u'ニョー'], 
u'haa':[u'はあ',u'ハー'], u'hii':[u'ひい',u'ヒー'], u'huu':[u'ふう',u'フー'], u'hee':[u'へえ',u'ヘー'], u'hoo':[u'ほお',u'ホー'], u'hyaa':[u'ひゃあ',u'ヒャー'], u'うhyuu':[u'ひゅう',u'ヒュー'], u'hyoo':[u'ひょお',u'ヒョー'], 
u'faa':[u'はあ',u'ハー'], u'fii':[u'ひい',u'ヒー'], u'fuu':[u'ふう',u'フー'], u'fee':[u'へえ',u'ヘー'], u'foo':[u'ほお',u'ホー'], u'fyaa':[u'ひゃあ',u'ヒャー'], u'うfyuu':[u'ひゅう',u'ヒュー'], u'fyoo':[u'ひょお',u'ヒョー'], 
u'maa':[u'まあ',u'マー'], u'mii':[u'みい',u'ミー'], u'muu':[u'むう',u'ムー'], u'mee':[u'めえ',u'メー'], u'moo':[u'もお',u'モー'], u'myaa':[u'みゃあ',u'ミャー'], u'myuu':[u'みゅう',u'ミュー'], u'myoo':[u'みょお',u'ミョー'], 
u'yaa':[u'やあ',u'ヤー'], u'yuu':[u'ゆう',u'ユー'], u'yoo':[u'よお',u'ヨー'],  
u'raa':[u'らあ',u'ラー'], u'rii':[u'りい', u'リー'], u'ruu':[u'るう',u'ルー'], u'ree':[u'れえ',u'レー'], u'roo':[u'ろお',u'ロー'], u'ryaa':[u'りゃあ',u'リャー'], u'ryuu':[u'りゅう',u'リュー'], u'ryoo':[u'りょお',u'リョー'], 
u'laa':[u'らあ',u'ラー'], u'lii':[u'りい', u'リー'], u'luu':[u'るう',u'ルー'], u'lee':[u'れえ',u'レー'], u'loo':[u'ろお',u'ロー'], u'lyaa':[u'りゃあ',u'リャー'], u'lyuu':[u'りゅう',u'リュー'], u'lyoo':[u'りょお',u'リョー'], 
u'waa':[u'わあ',u'ワー'],
u'gaa':[u'があ',u'ガー'], u'gii':[u'ぎい',u'ギー'], u'guu':[u'ぐう',u'グー'], u'gee':[u'げえ',u'ゲー'], u'goo':[u'ごお',u'ゴー'], u'gyaa':[u'ぎゃあ', u'ギャー'], u'gyuu':[u'ぎゅう',u'ギュー'] ,u'gyoo':[u'ぎょお',u'ギョー'], 
u'zaa':[u'ざあ',u'ザー'], u'zii':[u'じい',u'ジー'], u'zuu':[u'ずう',u'ズー'], u'zee':[u'ぜえ',u'ゼー'], u'zoo':[u'ぞお',u'ゾー'], u'zyaa':[u'じゃあ', u'ジャー'], u'zyuu':[u'じゅう',u'ジュー'] ,u'zyoo':[u'じょお',u'ジョー'], 
u'jaa':[u'じゃあ',u'ジャー'], u'jii':[u'じい',u'ジー'], u'juu':[u'じゅう',u'ジュー'], u'jee':[u'ぜえ',u'ゼー'], u'joo':[u'じょお',u'ジョー'], u'jyaa':[u'じゃあ', u'ジャー'], u'jyu':[u'じゅう',u'ジュー'] ,u'jyo':[u'じょお',u'ジョー'], 
u'daa':[u'だあ',u'ダー'], u'zii':[u'ぢい',u'ヂー'], u'zuu':[u'づう',u'ヅー'], u'dee':[u'でえ',u'デー'], u'doo':[u'どお',u'ドー'], u'zyaa':[u'ぢゃあ', u'ヂャー'], u'zyuu':[u'ぢゅう',u'ヂュー'] ,u'zyoo':[u'ぢょお',u'ヂョー'], 
u'baa':[u'ばあ',u'バー'], u'bii':[u'びい',u'ビー'], u'buu':[u'ぶう',u'ブー'], u'bee':[u'べえ',u'ベー'], u'boo':[u'ぼお',u'ボー'], u'byaa':[u'びゃあ', u'ビャー'], u'byuu':[u'びゅう',u'ビュー'] ,u'byoo':[u'びょお',u'ビョー'], 
u'paa':[u'ぱあ',u'パー'], u'pii':[u'ぴい',u'ピー'], u'puu':[u'ぷう',u'プー'], u'pee':[u'ぺえ',u'ペー'], u'poo':[u'ぽお',u'ポー'], u'pyaa':[u'ぴゃあ', u'ピャー'], u'pyuu':[u'ぴゅう',u'ピュー'] ,u'pyoo':[u'ぴょお',u'ピョー'], 

#permitted exceptions
u'sha':[u'しゃ',u'シャ'], u'shi':[u'し',u'シ'], u'shu':[u'しゅ',u'シュ'], u'sho':[u'しょ',u'ショ'], 
u'tsu':[u'つ', u'ツ'],     
u'cha':[u'ちゃ',u'チャ'], u'chi':[u'ち',u'チ'], u'chu':[u'ちゅ',u'チュ'], u'cho': [u'ちょ',u'チョ'], 
u'fu':[u'ふ',u'フ'],    
#u'ja':[u'じゃ',u'ジャ'], u'ji':[u'じ',u'ジ'], u'ju':[u'じゅ',u'ジュ'], u'jo':[u'じょ',u'ジョ'],
u'di':[u'ぢ',u'ヂ'], u'du':[u'づ',u'ヅ'],    
u'dya':[u'ぢゃ',u'ヂャ'], u'dyu':[u'ぢゅ',u'ヂュ'], u'dyo':[u'ぢょ',u'ヂョ'], 
u'kwa':[u'くゎ',u'クァ'],            
u'gwa':[u'ぐゎ',u'グァ'],            
u'wo':[u'を',u'を'],

#Single consonants. Not strictly correct, but add robustness to general transliteration.
u'b':[u'ぶ',u'ブ'],
u'c':[u'く',u'ク'],
u'd':[u'ど',u'ド'],
u'f':[u'ふ',u'フ'],
u'g':[u'ぐ',u'グ'],
u'h':[u'ふ',u'フ'],
u'hn':[u'ん',u'ン'],
u'j':[u'る',u'ル'],
u'k':[u'く',u'ク'],
u'l':[u'る',u'ル'],
u'm':[u'む',u'ム'],
u'p':[u'ぷ',u'プ'],
u'q':[u'くぃ',u'クイ'],
u'qu':[u'くぃ',u'クイ'],
u'r':[u'る',u'ル'],
u's':[u'す',u'ス'],
u't':[u'と',u'ト'],
u'v':[u'ぶ',u'ブ'],
u'w':[u'わ',u'ワ'],
u'x':[u'ず',u'ズ'],
u'y':[u'ゆ',u'ユ'],  
u'z':[u'ず',u'ズ'],

#simple punctuation handling?
u'a\'' :[u'ああ',u'アー'], u'i\'':[u'いい', u'イー'],u'u\'':[u'うう',u'ウー'], u'e\'':[u'ええ',u'エー'], u'o\'':[u'おお',u'オー'],
u'\'' :[u'',u''],
u'_' :[u'･',u'･'],

#TODO: match dipthongs? Better estimates for American english pronunciation?
#attempt to render 'th' better, without screwing up 'h'
u'tha':[u'ざ',u'ザ'], u'thi':[u'じ',u'ジ'], u'thu':[u'ず',u'ズ'], u'the':[u'ざ',u'ザ'], u'tho':[u'ぞ',u'ゾ'], u'thya':[u'つゃ',u'ツャ'], u'thyu':[u'つゅ',u'ツュ'], u'thyo':[u'つょ',u'ツョ'], 
u'th':[u'つ',u'ツ'],

}

def romaji2hiragana(phrase):
  '''Transliterate using kunrei-shiki
  '''
  #ensure input is a unicode string
  if not isinstance(phrase, unicode):
    raise NonUnicodeInputException('Input argument {phrase} is not unicode.'.format(phrase=phrase))

  hiragana = u''
  while phrase:
    (h,p) = nibble(phrase)
    #print 'returned phrase is ' + h[0]
    hiragana += h[0]
    phrase = p
  return hiragana

def romaji2katakana(phrase):
  '''Transliterate using kunrei-shiki
  '''
    #ensure input is a unicode string
  if not isinstance(phrase, unicode):
    raise NonUnicodeInputException('Input argument {phrase} is not unicode.'.format(phrase=phrase))

  katakana = u''
  while phrase:
    (h,p) = nibble(phrase)
    katakana += unicode(h[1])
    phrase = p
  return katakana


def nibble(phrase):
  '''Nibble off longest phrase
  '''
  #longest possible key->kana is 4 characters, so search next four then three etc for key hit
  for i in reversed(range(4)):
    nib = phrase[:i]
    if nib in TRANSLITERATION_TABLE:
      return (TRANSLITERATION_TABLE[nib], phrase[i:])
  return ([phrase[:1], phrase[:1]], phrase[1:])
  


def main():
  parser = argparse.ArgumentParser(description='Transliterate romaji to hiragana.')
  parser.add_argument('-k', '--katakana', help='Transliterate to katakana',action='store_true')
  parser.add_argument('words', nargs='*', help='Words to transliterate')
  args = parser.parse_args()

  for word in args.words:
    #best practice: decode early, encode late. Just handle unicode in libs.
    word = word.decode('utf-8')
    if args.katakana:
      print(romaji2katakana(word).encode('utf-8'))
    else:
      print(romaji2hiragana(word).encode('utf-8'))
        

if __name__ == "__main__":
  main()
