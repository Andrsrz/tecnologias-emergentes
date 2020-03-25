# -*- coding: utf-8 -*-

#   Constraints:
#
#   -Combinar correspondencias:
#
#   En un archivo de texto plano registra información de personas (nombre, apellidoP,
#   apellidoM, cargo, empresa, calle, numeroExt, numeroInt, colonia, municipio, estado,
#   codigoPostal, telefono, correoElectronico, fechaNacimiento, edadCalculada), el formato
#   lo determinarás de acuerdo a la implementación.
#
#   En otro archivo de texto plano elabora un "oficio", con la estructura que consideres
#   necesaria para incluir la información de las personas (archivo anterior).
#
#   Elabora un programa en python que cree un oficio por cada registro de personas y que
#   reemplace los datos de las mismas en el texto del oficio.

# --- Imports ---

import pickle, time, os, os.path, re, sys, docx

# --- Variables ---

listPersonData = []
dictPeople = {}
prompt = "> "
decision = "No"
personKey = ''
filename = '.demo.docx'
doc = docx.Document(filename)

# --- Functions ---

def calculateAge(listPersonData):
    actualYear = int(time.strftime("%Y"))
    actualMonth = int(time.strftime("%m"))
    newList = listPersonData[14].split('/')
    personYear = int(newList[2])
    personMonth = int(newList[1])
    age = actualYear - personYear
    if personMonth > actualMonth:
        age = age - 1
    return str(age)

def newPerson():
    global personKey, dictPeople, listPersonData
    listPersonData = []
    dictPeople = {}
    dictSample = {}

    print "Bienvenido a combinar correspondencia:\nIngresa el Nombre de la persona(Solo nombre):"
    name = raw_input(prompt)
    listPersonData.append(name)

    print "Ingresa el Apellido Paterno:"
    apellidoPat = raw_input(prompt)
    listPersonData.append(apellidoPat)

    print "Ingresa el Apellido Materno:"
    apellidoMat = raw_input(prompt)
    listPersonData.append(apellidoMat)

    print "Ingresa el Cargo de la persona:"
    cargo = raw_input(prompt)
    listPersonData.append(cargo)

    print "Ingresa el Nombre de la Empresa:"
    nameEmp = raw_input(prompt)
    listPersonData.append(nameEmp)

    print "Ingresa la Calle:"
    nameCalle = raw_input(prompt)
    listPersonData.append(nameCalle)

    print "Ingresa el Numero Exterior:"
    numExt = raw_input(prompt)
    listPersonData.append(numExt)

    print "Ingresa el Numero Interior:"
    numInt = raw_input(prompt)
    listPersonData.append(numInt)

    print "Ingresa la Colonia:"
    nameCol = raw_input(prompt)
    listPersonData.append(nameCol)

    print "Ingresa el Municipio:"
    nameMun = raw_input(prompt)
    listPersonData.append(nameMun)

    print "Ingresa el Estado:"
    nameEst = raw_input(prompt)
    listPersonData.append(nameEst)

    print "Ingresa el Codigo Postal:"
    numPost = raw_input(prompt)
    listPersonData.append(numPost)

    print "Ingresa el Telefono:"
    numTel = raw_input(prompt)
    listPersonData.append(numTel)

    print "Ingresa el Correo Electronico (name@domain.com):"
    email = raw_input(prompt)
    emailRegex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+	# username
        @					# @ symbol
        [a-zA-Z0-9.-]+		# domain
        (\.[a-zA-Z]{2,4})	# dot
        )''', re.VERBOSE)
    if not re.match(emailRegex, email):
        raw_input("Email invalido. Presiona enter para volver a comenzar")
        os.system('cls' if os.name == 'nt' else 'clear')
        newPerson()
    else:
        listPersonData.append(email)

    print "Ingresa tu Fecha de Nacimiento (xx/xx/xxxx):"
    numFechNac = raw_input(prompt)
    dateRegex = re.compile(r'\d{1,2}\/\d{1,2}\/\d{4}|\d{1,2}\/\d{1,2}\/\d{2}')
    if not re.match(dateRegex, numFechNac):
        raw_input("Fecha invalida. Presiona enter para volver a comenzar")
        os.system('cls' if os.name == 'nt' else 'clear')
        newPerson()
    else:
        listPersonData.append(numFechNac)

    listPersonData.append(calculateAge(listPersonData))

    if os.path.exists(".person.pickle"):
        pickleIn = open(".person.pickle","rb")
        dictSample = pickle.load(pickleIn)
        if " " in name:
            listName = name.split(" ")
            name = listName[0] + listName[1]
        personKey = name + apellidoPat
        dictSample.update({personKey:listPersonData})
        dictPeople = dictSample
    else:
        if " " in name:
            listName = name.split(" ")
            name = listName[0] + listName[1]
        personKey = name + apellidoPat
        dictPeople.update({personKey:listPersonData})

def writeFile():
    global personKey, doc, dictSample
    dictSample = {}

    pickleOut = open(".person.pickle","wb")
    pickle.dump(dictPeople, pickleOut)
    pickleOut.close()

    pickleIn = open(".person.pickle","rb")
    dictSample = pickle.load(pickleIn)

    for x in dictSample:
        if x in dictSample.keys():
            for paragraph in doc.paragraphs:
                if '(1)' and '(2)' and '(3)' in paragraph.text:
                    paragraph.text = "Nombre completo: " + dictSample[x][0] + " " + dictSample[x][1] + " " + dictSample[x][2] + "."
                elif '(15)' and '(16)' in paragraph.text:
                    paragraph.text = "Fecha de Nacimiento: " + dictSample[x][14] + ". Edad: " + dictSample[x][15] + "."
                elif '(5)' and '(4)' in paragraph.text:
                    paragraph.text = "Nombre de la Empresa: " + dictSample[x][4] + ". Cargo: " + dictSample[x][3] + "."
                elif '(6)' and '(7)' and '(8)' and '(12)' in paragraph.text:
                    paragraph.text = "Calle: " + dictSample[x][5] + ". Numero Interior: " + dictSample[x][7] + ". Numero Exterior: " + dictSample[x][6] + ". Codigo Postal: " + dictSample[x][11] + "."
                elif '(9)' and '(10)' and '(11)' in paragraph.text:
                    paragraph.text = "Colonia: " + dictSample[x][8] + ". Municipio: " + dictSample[x][9] + ". Estado: " + dictSample[x][10] + "."
                elif '(14)' and '(13)' in paragraph.text:
                    paragraph.text = "Correo Electronico: " + dictSample[x][13] + ". Telefono: " + dictSample[x][12] + "."
            doc.save(x + ".docx")
            doc = docx.Document(filename)
        else:
            print 'No existe la persona'

# --- Program ---

newPerson()
writeFile(dictPeople)