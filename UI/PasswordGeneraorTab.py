import random
import tkinter
import tkinter as tk
from tkinter import ttk
import os
from UI import Consts
from tkinter import Menu

class PasswordGeneratorTab:

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.minlength = 16
        self.maxlength = 20
        self.minASCII = 65
        self.maxASCII = 90
        self.minDigetASCII = 48
        self.maxDigetASCII = 57
        self.ENTRY_WIDTH = 40


        self.generateFrame = ttk.Labelframe(frame, text='generate password')
        self.generateFrame.grid(column=0, row=1, padx=8, pady=10, sticky="W")


        ttk.Label(self.generateFrame, text="password min size:").grid(column=0, row=0, padx=0, pady=0, sticky="W")

        self.minSize = tk.StringVar()
        self.minSizeEntry = ttk.Entry(self.generateFrame, width=Consts.ENTRY_WIDTH, textvariable=self.minSize)
        self.minSizeEntry.grid(column=1, row=0, sticky="W")
        self.minSize.set(str(self.minlength))

        ttk.Label(self.generateFrame, text="password max size:").grid(column=0, row=1, padx=0, pady=0, sticky="W")

        self.maxSize = tk.StringVar()
        self.maxSizeEntry = ttk.Entry(self.generateFrame, width=Consts.ENTRY_WIDTH, textvariable=self.maxSize)
        self.maxSizeEntry.grid(column=1, row=1, sticky="W")
        self.maxSize.set(str(self.maxlength))

        ttk.Button(self.generateFrame, text="generate", command=self.show_passwword).grid(column=1, row=2)

        ttk.Label(self.generateFrame, text="password min size:").grid(column=0, row=3, padx=0, pady=0, sticky="W")

        self.PasswordVar = tk.StringVar()
        self.passwordEntry = ttk.Entry(self.generateFrame, width=Consts.ENTRY_WIDTH, textvariable=self.PasswordVar, state='readonly')
        self.passwordEntry.grid(column=1, row=3, sticky="W")

        self.photo = tkinter.PhotoImage(file=r'C:\Users\\eitan\PycharmProjects\passwordGenerator\copy.png')

        ttk.Button(self.generateFrame, image=self.photo, command=self.copy).grid(column=2, row=3)


    def generate_password(self, passLength):
        generatedpassword = ''
        password = ""
        for character in range(passLength):
            if random.randint(1, 3) == 1:
                char = chr(random.randint(self.minDigetASCII, self.maxDigetASCII))
                generatedpassword += char
            else:
                char = chr(random.randint(self.minASCII, self.maxASCII))
                generatedpassword += char.lower()
        for char in generatedpassword:
            if char.isdigit() == False:
                if random.randint(1, 3) == 3:
                    password += char.upper()
                else:
                    password += char
            else:
                password += char
        return password


    def addToClipBoard(self, text):
        command = 'echo ' + text.strip() + '| clip'
        os.system(command)


    def show_passwword(self):
        try:
            minlength = int(self.minSize.get())
            maxlength = int(self.maxSize.get())

            passleangth = random.randint(minlength, maxlength)

            password = self.generate_password(passleangth)

            self.PasswordVar.set(password)

        except:
            raise Exception
            print('there was an error when generating passowrd \n'
                  'are you sure that password min size or max size are actually numbers \n'
                  'or min size is smaller than max size')

    def copy(self):
        self.addToClipBoard(self.PasswordVar.get())