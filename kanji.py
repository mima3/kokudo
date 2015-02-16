#!/usr/bin/env python
# -*- coding: utf8 -*-
# 以下のページのコード
# takayanの雑記帳 pythonで文章中のアラビア数字を漢数字に変換するスクリプト
# http://neu101.seesaa.net/article/159968583.html
import re

char2int = {
  u'0' :0, u'1' :1, u'2' :2, u'3' :3, u'4' :4,
  u'5' :5, u'6' :6, u'7' :7, u'8' :8, u'9' :9,
  u'０':0, u'１':1, u'２':2, u'３':3, u'４':4,
  u'５':5, u'６':6, u'７':7, u'８':8, u'９':9,
}

numKanji0 = [ u'', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九' ]
numKanji1 = [ u'', u'',   u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九' ]
numKanji  = [ numKanji0, numKanji1, numKanji1, numKanji1 ]

numPlace1 = [ u'', u'十', u'百', u'千' ]
numPlace4 = [ u'', u'万', u'億', u'兆', u'京', u'垓' ]

# 千の桁が１のときの処理:
#
# (a) 全て千
# 　例 　千万,　　千五百万, 　一万千, 　千
#
# (b) 全て一千
# 　例 一千万,　一千五百万, 一万一千, 一千
#
# (c) 四桁のときだけ千。残りは一千
# 　例 一千万,　一千五百万, 一万一千, 　千
#
# (d) 四桁のときは常に千。百十一の桁が無ければ一千、あれば千。
# 　例 一千万,　　千五百万, 一万一千, 　千
#
# (e) 一万以下の千の桁は常に千。一万以上の千の桁は常に一千。
# 　例 一千万,　一千五百万, 　一万千, 　千
#
# (f) 一万以下の千の桁は常に千。一万以上の千の桁は、百十一の桁が無ければ一千、あれば千。
# 　例 一千万,　　千五百万, 　一万千, 　千

def convert_pure_integerstring(match):
  source = match.group()
  numstr = re.sub( u'[,，]', u'', source )
#  numKanji[3] = numKanji0    # (b)
#  numKanji[3] = numKanji1 if len(numstr) == 4 else numKanji0  # (c),(e)
  s = []
  for ch in ((u'0'*((4-len(numstr)%4)&3))+numstr): s.insert(0,char2int[ch])

  list = []
  while len(s):
    temp = u''
    for i in range(4):
      if s[i]: temp = numKanji[i][s[i]] + numPlace1[i] + temp
    list.append(temp)
    s = s[4:]

  if len(list) > len(numPlace4): return source

  result = u''  # (a),(b),(c),(d)
#  result = list[0][1:] if list[0].startswith(u'一千') else list[0]  # (e)
#  result = list[0]  # (f)
  for i in range(len(list)):  # (a),(b),(c),(d)
#  for i in range(1,len(list)):　# (e),(f)
    if list[i]:
        if len(list) > 1 and list[i] == u'千': list[i] = u'一' + list[i]  # (d)
#        if list[i] == u'千': list[i] = u'一' + list[i]  # (f)
        result = list[i] + numPlace4[i] + result

  return result if result else u'零'

def convert_integerstring(string):
  if string == None or string == u'': return u''
  p = re.compile(u'[0-9０-９][0-9０-９,，]*[0-9０-９]|[0-9０-９]')
  return p.sub( convert_pure_integerstring, string )

#t = u'北海道旭川市南八条通25丁目3a'
#print convert_integerstring( u'北海道旭川市南八条通25丁目3')