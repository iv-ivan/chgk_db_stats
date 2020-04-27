# coding: utf-8
import json
import nltk
import string
from collections import defaultdict
import math

answers = json.load(open("answers.json"))
questions = json.load(open("questions.json"))

print len(answers), len(questions)

def tokenize(s):
	if isinstance(s, str):
		s = s.decode("utf-8")
	tokens = nltk.word_tokenize(s)
	tokens = [token.lower() for token in tokens if (token not in string.punctuation)]
	return tokens

def process_text(q, a):
	wq = {}
	wa = {}
	ww = defaultdict(dict)

	for token in tokenize(q):
		wq[token] = 1
	for token in tokenize(a):
		wa[token] = 1

	for word_q in wq:
		for word_a in wa:
			ww[word_q][word_a] = 1
	return wq, wa, ww

wq = defaultdict(lambda:0)
wa = defaultdict(lambda:0)
ww = defaultdict(lambda:defaultdict(lambda:0))

N = len(questions)
for i in xrange(N):
	wq_atom, wa_atom, ww_atom = process_text(questions[i], answers[i])
	for w in wq_atom:
		wq[w] += 1
	for w in wa_atom:
		wa[w] += 1
	for w1 in ww_atom:
		for w2 in ww_atom[w1]:
			ww[w1][w2] += 1

MAX_PRINT = 50
for v, k in sorted( ((v,k) for k,v in wa.iteritems()), reverse=True)[:MAX_PRINT]:
	print v, k

pmi = []
for w1 in ww:
	for w2 in ww[w1]:
		pmi.append((w1, w2, math.log(ww[w1][w2]*1.0/wq[w1]/wa[w2])))

for v in sorted(pmi, key=lambda x: x[2], reverse=True)[:MAX_PRINT]:
	print v[0], v[1], v[2]