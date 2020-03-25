# -*- coding: utf-8 -*-
import re

def isPhoneNumber(text):
	if len(text) != 12:
		return False
	for i in range(0, 3):
		if not text[i].isdigit():
			return False
	if text[3] != '-':
		return False
	for i in range(4, 7):
		if not text[i].isdigit():
			return False
	if text[7] != '-':
		return False
	for i in range(8, 12):
		if not text[i].isdigit():
			return False
	return True

phoneNumRegex = re.compile(r'(\(\d{3}\)) (\d{3}-\d{3}-\d{4})')
example = phoneNumRegex.search('Number: (044) 331-065-6222.')
print (example.group())

heroRegex = re.compile(r'Batman|Tina Fey')
matchObj = heroRegex.findall('Batman and Tina Fey')
print (matchObj)

fechaRegex = re.compile(r'\d{2}\/\d{2}\/\d{4}|\d\/\d\/\d{4}|\d\/\d{2}\/\d{4}|\d{2}\/\d\/\d{4}|\d{2}\/\d{2}\/\d{2}|\d\/\d\/\d{2}|\d\/\d{2}\/\d{2}|\d{2}\/\d\/\d{2}')
fechaRegex2 = re.compile(r'\d{1,2}\/\d{1,2}\/\d{4}|\d{1,2}\/\d{1,2}\/\d{2}')
emailRegex = re.compile(r'''(
	[a-zA-Z0-9._%+-]+	# username
	@					# @ symbol
	[a-zA-Z0-9.-]+		# domain
	(\.[a-zA-Z]{2,4})	# dot
	)''', re.VERBOSE)
matchObj2 = fechaRegex2.findall('Fecha: 18/10/95')
matchObj3 = fechaRegex2.findall('Fecha: 1/10/1988')
matchObj4 = fechaRegex2.findall('Fecha: 1/1/1988')
matchObj5 = fechaRegex2.findall('Fecha: 11/1/88')
matchObj6 = emailRegex.search('andres@algo.com')
postalRegex = re.compile(r'\d{5}')
print (matchObj2)
print (matchObj3)
print (matchObj4)
print (matchObj5)
print (matchObj6.group())
"""
print('415-555-4242 is a phone number:')
print(isPhoneNumber('415-555-4242'))
print('Moshi moshi is a phone number:')
print(isPhoneNumber('Moshi moshi'))
"""
"""
message = 'Call me at 415-555-1011 tomorrow. 415-555-9999 is my office.'

for i in range(len(message)):
	chunk = message[i:i+12]
	if isPhoneNumber(chunk):
		print('Phone number found: ' + chunk)

print 'Done'
"""