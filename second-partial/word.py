# -*- coding: utf-8 -*-

import re, sys, os, docx

listP = ['nombre','apellido1','apellido2','cargo','empresa','calle','numExt','numInt','colonia','municipio','estado','codPost','tel','email','fecNac']
strRegex = re.compile(r'\(\d\)|\(\d{2}\)')
filename = 'test.docx'
doc = docx.Document(filename)
replace = r'esto es una prueba'

def ReplaceStrDocx(docObj, regex, listP):
	for p in docObj.paragraphs:
		if regex.search(p.text):
			inline = p.runs
			#
			for i in range(len(inline)):
				if regex.search(inline[i].text):
					if inline[i].text == '(1)':
						text = regex.sub(listP[0], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(2)':
						text = regex.sub(listP[1], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(3)':
						text = regex.sub(listP[2], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(4)':
						text = regex.sub(listP[3], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(5)':
						text = regex.sub(listP[4], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(6)':
						text = regex.sub(listP[5], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(7)':
						text = regex.sub(listP[6], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(8)':
						text = regex.sub(listP[7], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(9)':
						text = regex.sub(listP[8], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(10)':
						text = regex.sub(listP[9], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(11)':
						text = regex.sub(listP[10], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(12)':
						text = regex.sub(listP[11], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(13)':
						text = regex.sub(listP[12], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(14)':
						text = regex.sub(listP[13], inline[i].text)
						inline[i].text = text
					elif inline[i].text == '(15)':
						text = regex.sub(listP[14], inline[i].text)
						inline[i].text = text

ReplaceStrDocx(doc, strRegex, listP)
doc.save('test2.docx')