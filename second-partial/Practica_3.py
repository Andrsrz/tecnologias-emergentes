# -*- coding: utf-8 -*-

# Constraints:
#   - Escribe el codigo necesario para capturar una cadena de texto y definir una
#     funcion para que determine si es una direccion de correo electronico valida.

import re

charChain = raw_input("Ingresa tu email: ")

def isAValidEmail(charChain):
    allGood = "Todo bien"
    somethingIsWrong = "Esta mal"
    emailRegex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+	# username
        @					# @ symbol
        [a-zA-Z0-9.-]+		# domain
        (\.[a-zA-Z]{2,4})	# dot
        )''', re.VERBOSE)
    if not re.match(emailRegex, charChain):
        return somethingIsWrong
    else:
        return allGood

print(isAValidEmail(charChain))

