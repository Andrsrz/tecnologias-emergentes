# -*- coding: utf-8 -*-

# Constraints:
#   -Escribe el codigo necesario para capturar varios numeros y
#    almacenarlos en una lista como valores numericos.
# 
#   1.- De la lista capturada imprime una sublista de 2 elementos que correspondan a
#       la mitad de la lista original, independientemente de la cantidad de elementos
#       capturados.
#   2.- De la lista original, imprime en una sola linea de codigo el primer elemento y
#       el ultimo.
#   3.- En la lista original, agrega loa elementos de la lista al final de la misma,
#       imprime el resultado.
#   4.- De la lista obtenina ordena los elementos de menor a mayor e imprime el resultado.
#   5.- Vuelve a ordenar sus elementos de mayor a menor e imprime el resultado.
#   6.- Escribe una funcion que devuelva el cubo de los elementos de la lista, imprime el
#       resultado.

listOfNums = []

sizeOfList = int(raw_input("Ingresa el tamaño de la lista: "))
print("Ingresa los numeros separados por enter: ")

for i in range(int(sizeOfList)):
    listOfNums.append(int(raw_input()))

print("Lista ingresada: " + str(listOfNums))

# Solucion punto 1.-
if sizeOfList % 2 == 0:
    #print("La lista es par")
    print("La mitad de la lista es: " + str(listOfNums[(sizeOfList/2)-1:(sizeOfList/2)+1]))
else:
    #print("La lista es impar")
    print("La mitad de la lista es: " + str(listOfNums[int(round(sizeOfList/2))]))

# Solucion punto 2.-
print("Primer elemento de la lista: " + str(listOfNums[0]) + ". Y ultimo elemento: " + str(listOfNums[sizeOfList-1]))

# Solucion punto 3.-
listOfNums.extend(listOfNums)
print("Lista nueva: " + str(listOfNums))

# Solucion punto 4.-
listOfNums.sort()
print("Lista menor a mayor: " + str(listOfNums))

# Solucion punto 5.-
listOfNums.reverse()
print("Lista mayor a menor: " + str(listOfNums))

# Solucion punto 6.-
def cubeList(aList):
    cbList = []
    for i in aList:
        cube = i * i * i
        cbList.append(cube)
    return cbList

print("Numeros de la lista al cubo: \n" + str(cubeList(listOfNums)))