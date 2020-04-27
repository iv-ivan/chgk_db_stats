# coding: utf-8
from os import listdir
from os.path import isfile, join
import codecs

dir = "files/db"
onlyfiles = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f)) and ".txt" in f]

questions = []
answers = []
for file in onlyfiles:
	with codecs.open(file, encoding="utf-8") as f:
		print file
		is_question = False
		is_answer = False
		for line in f:
			v = line.strip().split(" ")
			if line.strip() == u"Вопрос:" or (v[0] == u"Вопрос" and v[1][-1] == u":" and len(v) == 2):
				is_question = True
				question = ""
				continue
			if len(line.strip()) == 0:
				if is_answer and len(answer) > 0 and answer != " ":
					answers.append(answer[:-1].encode("utf-8"))
					if len(answers) != len(questions):
						print file
						print len(answers), len(questions)
						print answers[-1], questions[-1]
						print answers[-2], questions[-2]
						print answers[-3], questions[-3]
						exit()

				if is_question and len(question) > 0 and question != " ":
					questions.append(question[:-1].encode("utf-8"))
				is_question = False
				is_answer = False
				continue
			if line.strip() == u"Ответ:":
				is_answer = True
				answer = ""
				continue
			if is_answer:
				answer += line.strip() + " "
				continue
			if is_question:
				question += line.strip() + " "
				continue
		if is_answer:
			answers.append(answer[:-1].encode("utf-8"))
		if is_question:
			questions.append(question[:-1].encode("utf-8"))
		if len(answers) != len(questions):
			print file
			print len(answers), len(questions)
			print answers[-1], questions[-1]
			exit()


print len(answers), len(questions)

import json
json.dump(answers, open("answers.json", "w"), ensure_ascii=False)
json.dump(questions, open("questions.json", "w"), ensure_ascii=False)
