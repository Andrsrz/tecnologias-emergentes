# -*- coding: utf-8 -*-

#   Elaborar una aplicacion Python que se mantenga en ejecucion (Menu)
#   administre la informacion del archivo de personas (Altas, Bajas y Cambios)
#   y debe brindar la funcionalidad de imprimir especificamente un solo
#   oficio, varios o todos
#   Generar primero PDF y después Word

# --- Imports ---

from Tkinter import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import pickle, time, os, os.path, re, sys, docx, ttk, tkMessageBox, smtplib

# --- Variables ---

listPersonData, tempList = [], []
dictPeople = {}
personKey, name, apellidoPat, myEmail, MY_SECRET_PASSWORD = '', '', '', 'andrsruiz@hotmail.com', 'Hotmail.301111'
filename = '.demo.docx'
doc = docx.Document(filename)

# --- Functions ---

def getDate():
    actualYear = str(time.strftime("%Y"))
    actualMonth = str(time.strftime("%m"))
    actualDay = str(time.strftime("%d"))
    actualDate = actualDay + "/" + actualMonth + "/" + actualYear
    return str(actualDate)

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

def addPersonToList():
    global nameGUI, firstNameGUI, txtBoxLastName, txtBoxPosition, txtBoxCompany, txtBoxStreet
    global txtBoxNumExt, txtBoxNumInt, txtBoxSuburb, txtBoxTown, txtBoxState, txtBoxPostCode
    global txtBoxTel, txtBoxEmail, txtBoxBirthDate, listPersonData, personKey, dictPeople
    
    listPersonData = []
    dictPeople = {}
    dictSample = {}
    personKey, name, apellidoPat = "", "", ""
    name = str(nameGUI.get())
    apellidoPat = str(firstNameGUI.get())

    if " " in name:
        listName = name.split(" ")
        name = listName[0] + listName[1]
        personKey = name + apellidoPat
    else:
        personKey = name + apellidoPat

    listPersonData.append(nameGUI.get())
    listPersonData.append(firstNameGUI.get())
    listPersonData.append(txtBoxLastName.get())
    listPersonData.append(txtBoxPosition.get())
    listPersonData.append(txtBoxCompany.get())
    listPersonData.append(txtBoxStreet.get())
    listPersonData.append(txtBoxNumExt.get())
    listPersonData.append(txtBoxNumInt.get())
    listPersonData.append(txtBoxSuburb.get())
    listPersonData.append(txtBoxTown.get())
    listPersonData.append(txtBoxState.get())
    listPersonData.append(txtBoxPostCode.get())
    listPersonData.append(txtBoxTel.get())
    
    email = txtBoxEmail.get()
    emailRegex = re.compile(r'''(
        [a-zA-Z0-9._%+-]+	# username
        @					# @ symbol
        [a-zA-Z0-9.-]+		# domain
        (\.[a-zA-Z]{2,4})	# dot
        )''', re.VERBOSE)
    if not re.match(emailRegex, email):
        listPersonData = []
        personKey = []
        tkMessageBox.showerror("Email Error", "El email ingresado no es valido.\nEjemplo: name@domain.algo")
    else:
        listPersonData.append(email)

    numFechNac = txtBoxBirthDate.get()
    dateRegex = re.compile(r'\d{1,2}\/\d{1,2}\/\d{4}|\d{1,2}\/\d{1,2}\/\d{2}')
    if not re.match(dateRegex, numFechNac):
        listPersonData = []
        personKey = []
        tkMessageBox.showerror("Birthdate Error", "La fecha ingresada no es valida.\nEjemplo: xx/xx/xxxx")
    else:
        listPersonData.append(numFechNac)

    listPersonData.append(calculateAge(listPersonData))

def addPersonToDict(listPersonData):
    global personKey, dictPeople
    dictPeople.clear()

    if os.path.exists(".person.pickle"):
        pickleIn = open(".person.pickle","rb")
        dictSample = pickle.load(pickleIn)
        dictSample.update({personKey:listPersonData})
        dictPeople = dictSample
    else:
        dictPeople.update({personKey:listPersonData})

def makePickle(dictPeople):
    pickleOut = open(".person.pickle","wb")
    pickle.dump(dictPeople, pickleOut)
    pickleOut.close()

def infoMsgBox():
    tkMessageBox.showinfo("Info", "Aplicacion hecha por:\nAndres Ruiz.")

def saveToFile():
    global nameGUI, firstNameGUI, txtBoxLastName, txtBoxPosition, txtBoxCompany, txtBoxStreet
    global txtBoxNumExt, txtBoxNumInt, txtBoxSuburb, txtBoxTown, txtBoxState, txtBoxPostCode
    global txtBoxTel, txtBoxEmail, txtBoxBirthDate, listPersonData
    try:
        addPersonToList()
        addPersonToDict(listPersonData)
        makePickle(dictPeople)
        txtBoxName.delete(0,END)
        txtBoxFirstName.delete(0,END)
        txtBoxLastName.delete(0,END)
        txtBoxPosition.delete(0,END)
        txtBoxCompany.delete(0,END)
        txtBoxStreet.delete(0,END)
        txtBoxNumExt.delete(0,END)
        txtBoxNumInt.delete(0,END)
        txtBoxSuburb.delete(0,END)
        txtBoxTown.delete(0,END)
        txtBoxState.delete(0,END)
        txtBoxPostCode.delete(0,END)
        txtBoxTel.delete(0,END)
        txtBoxEmail.delete(0,END)
        txtBoxBirthDate.delete(0,END)
        cboxPeople["value"] = personKey
    except:
        tkMessageBox.showerror("Data Error", "No se pudo guardar la persona.\nVuelve a intentar.")

def makeWord():
    global filename, doc
    personName = cboxPeople.get()
    try:
        pickleIn = open(".person.pickle","rb")
        dictSample = pickle.load(pickleIn)
        for x in dictSample:
            if x in dictSample.keys() and x == personName:
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
                doc.save(personName + ".docx")
            doc = docx.Document(filename)
        dictSample.clear()
        cboxPeople.set('')
        pickleIn.close()
    except:
        tkMessageBox.showerror("Data Error", "Selecciona una persona para generar el documento.")

def syncCombobox():
    filesList = []
    cboxPeople.set('')
    cboxPeople["values"] = ""
    
    try:
        if os.path.exists(".person.pickle"):
            pickleIn = open(".person.pickle","rb")
            dictSample = pickle.load(pickleIn)
            for x in dictSample.keys():
                filesList.append(x)
            cboxPeople["values"] = filesList
    except:
        tkMessageBox.showerror("Data Error", "No hay Base de Datos")

def deletePerson():
    global dictPeople

    try:
        pickleIn = open(".person.pickle","rb")
        dictSample = pickle.load(pickleIn)
        personToDelete = cboxPeople.get()
        if personToDelete in dictSample.keys():
            dictSample.pop(personToDelete, None)
            dictPeople = dictSample
            makePickle(dictPeople)
            syncCombobox()
    except:
        tkMessageBox.showerror("Data Error", "Selecciona una persona primero")

def addToQueue():
    global TextArea, cboxPeople, tempList

    person = cboxPeople.get()

    if len(tempList) > 0:
        TextArea.config(state=NORMAL)
        if person in tempList:
            tkMessageBox.showwarning("Data Warning", "Esa persona ya está en la cola.")
        else:
            tempList.append(person)
            TextArea.insert('1.0', person + "\n")
        TextArea.config(state=DISABLED)
    else:
        TextArea.config(state=NORMAL)
        tempList.append(person)
        TextArea.insert('1.0', person + "\n")
        TextArea.config(state=DISABLED)

def cleanQueue():
    global tempList, TextArea
    tempList = []
    TextArea.config(state=NORMAL)
    TextArea.delete(1.0, END)
    TextArea.config(state=DISABLED)

def makeSomeWords():
    global tempList, doc

    if len(tempList) == 0:
        tkMessageBox.showwarning("Data Warning", "No hay personas en\nla cola de impresión")
    else:
        try:
            pickleIn = open(".person.pickle","rb")
            dictSample = pickle.load(pickleIn)
            for x in tempList:
                if x in dictSample.keys():
                    personName = x
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
                    doc.save(personName + ".docx")
                doc = docx.Document(filename)
            cleanQueue()
            dictSample.clear()
            pickleIn.close()
        except:
            tkMessageBox.showerror("Data Error", "Revisa la base de datos.")

def makeAllWords():
    global filename, doc
    personName = ''
    try:
        pickleIn = open(".person.pickle","rb")
        dictSample = pickle.load(pickleIn)
        for x in dictSample:
            if x in dictSample.keys():
                personName = x
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
                doc.save(personName + ".docx")
            doc = docx.Document(filename)
        dictSample.clear()
        cboxPeople.set('')
        pickleIn.close()
    except:
        tkMessageBox.showerror("Data Error", "Selecciona una persona para generar el documento.")

def sendEmail():
    global myEmail, MY_SECRET_PASSWORD, cboxPeople

    try:
        pickleIn = open(".person.pickle","rb")
        dictSample = pickle.load(pickleIn)
        cBoxKey = cboxPeople.get()
        if cBoxKey in dictSample.keys():
            toEmail = dictSample[cBoxKey][13]

            msg = MIMEMultipart()
            msg['From'] = myEmail
            msg['To'] = toEmail
            msg['Subject'] = 'Documento del dia: ' + getDate()

            body = 'Hola, ' + cBoxKey + ' aqui esta tu documento'
            msg.attach(MIMEText(body, 'plain'))

            fileToSendName = cBoxKey + ".docx"
            attachment = open(fileToSendName, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % fileToSendName)
            
            msg.attach(part)
            text = msg.as_string()
            try:
                smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
                # or smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtpObj.ehlo() # Stablish connection to the server, code 250 for success
                smtpObj.starttls() # Start TSL encryption, code 220 for success
                smtpObj.login(myEmail, MY_SECRET_PASSWORD) # Login, code 235 for success
                smtpObj.sendmail(myEmail, toEmail, text) # Send email
                smtpObj.quit() # Disconnect from server
            except:
                smtpObj.quit() # Disconnect from server
                tkMessageBox.showerror("Connection Error", "No se pudo conectar con el servidor.\nIntenta mas tarde.")
    except:
        tkMessageBox.showerror("Data Error", "Selecciona una persona para enviar correo.")

def sendSomeEmails():
    global myEmail, MY_SECRET_PASSWORD, tempList

    if len(tempList) == 0:
        tkMessageBox.showwarning("Data Warning", "No hay personas en\nla cola de impresión")
    else:
        try:
            pickleIn = open(".person.pickle","rb")
            dictSample = pickle.load(pickleIn)
            for x in tempList:
                if x in dictSample.keys():
                    toEmail = dictSample[x][13]

                    msg = MIMEMultipart()
                    msg['From'] = myEmail
                    msg['To'] = toEmail
                    msg['Subject'] = 'Documento del dia: ' + getDate()

                    body = 'Hola, ' + x + ' aqui esta tu documento'
                    msg.attach(MIMEText(body, 'plain'))

                    fileToSendName = x + ".docx"
                    attachment = open(fileToSendName, "rb")

                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', "attachment; filename= %s" % fileToSendName)
                    
                    msg.attach(part)
                    text = msg.as_string()
                try:
                    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
                    # or smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    smtpObj.ehlo() # Stablish connection to the server, code 250 for success
                    smtpObj.starttls() # Start TSL encryption, code 220 for success
                    smtpObj.login(myEmail, MY_SECRET_PASSWORD) # Login, code 235 for success
                    smtpObj.sendmail(myEmail, toEmail, text) # Send email
                    smtpObj.quit() # Disconnect from server
                except:
                    tkMessageBox.showerror("Connection Error", "No se pudo conectar con el servidor.\nIntenta mas tarde.")
            cleanQueue()
        except:
            tkMessageBox.showerror("Data Error", "Revisa que todas las personas\nde la cola de impresión\nya tengan documento.")

def sendAllEmails():
    global myEmail, MY_SECRET_PASSWORD

    try:
        pickleIn = open(".person.pickle","rb")
        dictSample = pickle.load(pickleIn)
        for x in dictSample:
            if x in dictSample.keys():
                toEmail = dictSample[x][13]

                msg = MIMEMultipart()
                msg['From'] = myEmail
                msg['To'] = toEmail
                msg['Subject'] = 'Documento del dia: ' + getDate()

                body = 'Hola, ' + x + ' aqui esta tu documento'
                msg.attach(MIMEText(body, 'plain'))

                fileToSendName = x + ".docx"
                attachment = open(fileToSendName, "rb")

                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % fileToSendName)
                
                msg.attach(part)
                text = msg.as_string()
            try:
                smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
                # or smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtpObj.ehlo() # Stablish connection to the server, code 250 for success
                smtpObj.starttls() # Start TSL encryption, code 220 for success
                smtpObj.login(myEmail, MY_SECRET_PASSWORD) # Login, code 235 for success
                smtpObj.sendmail(myEmail, toEmail, text) # Send email
                smtpObj.quit() # Disconnect from server
            except:
                tkMessageBox.showerror("Connection Error", "No se pudo conectar con el servidor.\nIntenta mas tarde.")
    except:
        tkMessageBox.showerror("Data Error", "No hay base de datos.")

# --- GUI ---

master = Tk()
master.title("Correspondencia")
master.geometry('740x340')
master.resizable(False, False)

ntBook = ttk.Notebook(width=740, height=340)
ntBook.pack()

tabPer = ttk.Frame(ntBook)
ntBook.add(tabPer, text="Persona")
tabFile = ttk.Frame(ntBook)
ntBook.add(tabFile, text="Archivo")
tabInfo = ttk.Frame(ntBook)
ntBook.add(tabInfo, text="Info")

lbName = Label(tabPer, text="Nombre(s)").grid(column=0, row=0)
nameGUI = StringVar()
txtBoxName = Entry(tabPer, textvariable=nameGUI)
txtBoxName.grid(column=1, row=0)
lbFirstName = Label(tabPer, text="Apellido Paterno").grid(column=0, row=1)
firstNameGUI = StringVar()
txtBoxFirstName = Entry(tabPer, textvariable=firstNameGUI)
txtBoxFirstName.grid(column=1, row=1)
lbLastName = Label(tabPer, text="Apellido Materno").grid(column=0, row=2)
lastNameGUI = StringVar()
txtBoxLastName = Entry(tabPer, textvariable=lastNameGUI)
txtBoxLastName.grid(column=1, row=2)
lbPost = Label(tabPer, text="Cargo").grid(column=0, row=3)
positionGUI = StringVar()
txtBoxPosition = Entry(tabPer, textvariable=positionGUI)
txtBoxPosition.grid(column=1, row=3)
lbCompany = Label(tabPer, text="Empresa").grid(column=0, row=4)
companyGUI = StringVar()
txtBoxCompany = Entry(tabPer, textvariable=companyGUI)
txtBoxCompany.grid(column=1, row=4)
lbStreet = Label(tabPer, text="Calle").grid(column=0, row=5)
streetGUI = StringVar()
txtBoxStreet = Entry(tabPer, textvariable=streetGUI)
txtBoxStreet.grid(column=1, row=5)
lbNumExt = Label(tabPer, text="Numero Exterior").grid(column=0, row=6)
numExtGUI = StringVar()
txtBoxNumExt = Entry(tabPer, textvariable=numExtGUI)
txtBoxNumExt.grid(column=1, row=6)
lbNumInt = Label(tabPer, text="Numero Interior").grid(column=0, row=7)
numIntGUI = StringVar()
txtBoxNumInt = Entry(tabPer, textvariable=numIntGUI)
txtBoxNumInt.grid(column=1, row=7)
lbSuburb = Label(tabPer, text="Colonia").grid(column=2, row=0)
suburbGUI = StringVar()
txtBoxSuburb = Entry(tabPer, textvariable=suburbGUI)
txtBoxSuburb.grid(column=3, row=0)
lbTown = Label(tabPer, text="Municipio").grid(column=2, row=1)
townGUI = StringVar()
txtBoxTown = Entry(tabPer, textvariable=townGUI)
txtBoxTown.grid(column=3, row=1)
lbState = Label(tabPer, text="Estado").grid(column=2, row=2)
stateGUI = StringVar()
txtBoxState = Entry(tabPer, textvariable=stateGUI)
txtBoxState.grid(column=3, row=2)
lbPostCode = Label(tabPer, text="Codigo Postal").grid(column=2, row=3)
posCodeGUI = StringVar()
txtBoxPostCode = Entry(tabPer, textvariable=posCodeGUI)
txtBoxPostCode.grid(column=3, row=3)
lbTel = Label(tabPer, text="Telefono").grid(column=2, row=4)
telGUI = StringVar()
txtBoxTel = Entry(tabPer, textvariable=telGUI)
txtBoxTel.grid(column=3, row=4)
lbEmail = Label(tabPer, text="Email").grid(column=2, row=5)
emailGUI = StringVar()
txtBoxEmail = Entry(tabPer, textvariable=emailGUI)
txtBoxEmail.grid(column=3, row=5)
lbEmail2 = Label(tabPer, text="name@domain.algo").grid(column=4, row=5)
lbBirthDate = Label(tabPer, text="Fecha de Nacimiento").grid(column=2, row=6)
birthDateGUI = StringVar()
txtBoxBirthDate = Entry(tabPer, textvariable=birthDateGUI)
txtBoxBirthDate.grid(column=3, row=6)
lbBirthDate2 = Label(tabPer, text="dd/mm/yyyy").grid(column=4, row=6)
btnSaveInfo = Button(tabPer, text="Guardar", command=saveToFile)
btnSaveInfo.grid(column=2, row=8)

lb = Label(tabFile, text="").grid(column=0, row=0)
lb2 = Label(tabFile, text="\t").grid(column=0, row=1)
cboxPeople = ttk.Combobox(tabFile, state="readonly")
cboxPeople.grid(column=3, row=1)
btnWord = Button(tabFile, text="Generar Word", command=makeWord)
btnWord.grid(column=2, row=1)
btnSync = Button(tabFile, text="Actualizar", command=syncCombobox)
btnSync.grid(column=5, row=1)
btnDelete = Button(tabFile, text="Borrar", command=deletePerson)
btnDelete.grid(column=4, row=3)
btnSendEmail = Button(tabFile, text="Enviar\nal Correo", command=sendEmail)
btnSendEmail.grid(column=5, row=3)
btnAddToQueue = Button(tabFile, text="Agregar a Cola", command=addToQueue)
btnAddToQueue.grid(column=4, row=1)
lb3 = Label(tabFile, text="Cola de impresion").grid(column=1, row=5)
TextArea = Text(tabFile, width=15, height=7)
TextArea.grid(column=2, row=5)
TextArea.config(state=DISABLED)
btnClearQueue = Button(tabFile, text="Limpiar cola\nde Impresión", command=cleanQueue)
btnClearQueue.grid(column=3, row=5)
btnPrintTA = Button(tabFile, text="Generar Words", command=makeSomeWords)
btnPrintTA.grid(column=2, row=6)
btnSemdSomeEmails = Button(tabFile, text="Enviar al Correo", command=sendSomeEmails)
btnSemdSomeEmails.grid(column=2, row=7)
btnMakeAll = Button(tabFile, text="Generar Todos\nWords", command=makeAllWords)
btnMakeAll.grid(column=4, row=5)
btnSendAllEmail = Button(tabFile, text="Enviar Todos\nal Correo", command=sendAllEmails)
btnSendAllEmail.grid(column=5, row=5)

btnInfo = Button(tabInfo, text="Info", command=infoMsgBox)
btnInfo.pack()

master.mainloop()