# -*- coding:utf-8 -*-

#   Constraints:
#   -Escribe el codigo necesario para capturar una cadena de texto
#
#   1.- Escribe una funcion que de verdadero o falso si la primera letra de la cadena
#       es mayuscula.
#   2.- Escribe una funcion que cuente las palabras que forman la cadena de texto.
#   3.- Escribe una funcion que reciba como argumento la cadena de texto y regrese una
#       lista con las palabras que la forman.
#   4.- Escribe una funcion que regrese la cadena de texto invertida.
#   5.- Escribe una funcion que regrese la cadena original con la ultima letra de cada
#       palabra en mayuscula.

charChain = raw_input("Ingresa una cadena de caracteres: \n")
print ("\n" + "Cadena introducida: " + "'" + charChain + "'")

# Solucion punto 1.-
def isUpper(charChain):
    yes_or_no = charChain[0].isupper()
    print("La cadena comienza con una letra mayuscula: " + str(yes_or_no))

isUpper(charChain)

# Solucion punto 2.-
def howManyWords(charChain):
    count = 0
    newList = charChain.split(' ')
    for i in newList:
        count += 1
    if count == 1:
        print("Hay " + str(count) + " palabra en la cadena")
    else:
        print("Hay " + str(count) + " palabras en la cadena")

howManyWords(charChain)

# Solucion punto 3.-
def listReturned(charChain):
    newList = charChain.split(' ')
    return newList

print(listReturned(charChain))

# Solucion punto 4.-
def reversedCharChain(charChain):
    return charChain[::-1]

print(reversedCharChain(charChain))

# Solucion punto 5.-
def upperLeft(charChain):
    reversedString = charChain[::-1]
    reversedString = reversedString.title()
    return reversedString[::-1]

print(upperLeft(charChain))
