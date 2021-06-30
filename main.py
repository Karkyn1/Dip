# coding: utf-8
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#from PIL import ImageTk
import time, threading
from ECDHKE import *
# pip install pillow
class mainWin():

    def __init__(self):
        self.pause1 = 0.5
        self.pause2 = 1
        self.utf8s = {0:'⁰', 1:'¹', 2:'²', 3:'³', 4:'⁴', 5:'⁵',
                      6:'⁶', 7:'⁷', 8:'⁸', 9:'⁹', 10:'¹⁹'}
        self.root = Tk()
        self.root.geometry("535x580")
        self.imgA = PhotoImage(file='alice.png')
        self.imgB = PhotoImage(file='bob.png')
        #фрейм основной
        self.fm = Frame(self.root)
        self.fm.pack(side=TOP, expand=True, fill=BOTH)

        #self.btn = Button(self.fm, text="привет")
        #self.btn.place(x=0,y=0)

        self.l1 = Label(self.fm, text="Введите неприводимый полином:", font="Calibri 12")
        self.l1.place(x=10, y=5)
        self.cmbPolinom = ttk.Combobox(self.fm, values=[1,2,3,4,5,6,7,8,9,10], width=5)
        self.cmbPolinom.place(x=475,y=35)
        self.cmbPolinom.bind("<<ComboboxSelected>>", self.createPolinom)
        self.elemPolinom = []
        self.lblPolinom = []

        self.l2 = Label(self.fm, text="Введите элемент конечного поля X:", font="Calibri 12")
        self.l2.place(x=10, y=60)
        self.cmbPX = ttk.Combobox(self.fm, values=[1,2,3,4,5,6,7,8,9,10], width=5)
        self.cmbPX.place(x=475,y=90)
        self.cmbPX.bind("<<ComboboxSelected>>", self.createPX)
        self.elemPX = []
        self.lblPX = []

        self.l3 = Label(self.fm, text="Введите  элемент конечного поля  Y:", font="Calibri 12")
        self.l3.place(x=10, y=115)
        self.cmbPY = ttk.Combobox(self.fm, values=[1,2,3,4,5,6,7,8,9,10], width=5)
        self.cmbPY.place(x=475,y=145)
        self.cmbPY.bind("<<ComboboxSelected>>", self.createPY)
        self.elemPY = []
        self.lblPY = []
        

        self.l4 = Label(self.fm, text="Закрытый ключ Алисы:", font="Calibri 12")
        self.l4.place(x=10, y=180)
        self.keyA = Entry(self.fm, width=57)
        self.keyA.place(x=182, y=185)
        

        self.l5 = Label(self.fm, text="Закрытый ключ Боба:", font="Calibri 12")
        self.l5.place(x=10, y=210)
        self.keyB = Entry(self.fm, width=57)
        self.keyB.place(x=182, y=215)

        self.btnGo = Button(self.fm, text='Выполнить', font='Arial 12')
        self.btnGo.pack(side=BOTTOM, fill=X)
        self.btnGo.bind('<ButtonRelease>', self.createRezult)

        self.liAlice = Label(self.fm)
        self.liBob = Label(self.fm)

        self.tAlice1 = Label(self.fm, text = "")
        self.tAlice1.place(x=10,y=250)
        self.tAlice2 = Label(self.fm, text = "")
        self.tAlice2.place(x=10,y=270)
        self.tAlice3 = Label(self.fm, text = "")
        self.tAlice3.place(x=10,y=460)
        self.tAlice4 = Label(self.fm, text = "")
        self.tAlice4.place(x=10,y=480)
        self.tAlice5 = Label(self.fm, text = "")
        self.tAlice5.place(x=10,y=500)
        self.tAlice6 = Label(self.fm, text = "")
        self.tAlice6.place(x=10,y=520)

        self.tBob1 = Label(self.fm, text = "")
        self.tBob1.place(x=300,y=250)
        self.tBob2 = Label(self.fm, text = "")
        self.tBob2.place(x=300,y=270)
        self.tBob3 = Label(self.fm, text = "")
        self.tBob3.place(x=300,y=460)
        self.tBob4 = Label(self.fm, text = "")
        self.tBob4.place(x=300,y=480)
        self.tBob5 = Label(self.fm, text = "")
        self.tBob5.place(x=300,y=500)
        self.tBob6 = Label(self.fm, text = "")
        self.tBob6.place(x=300,y=520)

        self.lSmsa = Label(self.fm, text="")
        self.lSmsa.place(x=145, y=350)

        self.lSmsb = Label(self.fm, text="", justify="right", anchor=S)
        self.lSmsb.place(x=145, y=370)
        
        self.root.mainloop()


    def createPolinom(self, event):
        n = int(self.cmbPolinom.get().strip())
        print(n)
        for e in self.elemPolinom:
            e.destroy()
        for l in self.lblPolinom:
            l.destroy()
        self.elemPolinom = []
        self.lblPolinom = []
        lst = list(range(n))
        for i in lst[::-1]:
            print(i)
            mnz = n-1-i
            e = Entry(self.fm, width=2)
            e.insert(END, 0)
            e.place(x=42*mnz+10, y=35)
            self.elemPolinom.append(e)
            if i != 0:
                l = Label(self.fm,text='x'+self.utf8s.get(i,'')+'+')
                l.place(x=42*mnz+30, y=35)
                self.lblPolinom.append(l)


    def createPX(self, event):
        n = int(self.cmbPX.get().strip())
        for e in self.elemPX:
            e.destroy()
        for l in self.lblPX:
            l.destroy()
        self.elemPX = []
        self.lblPX = []
        lst = list(range(n))
        for i in lst[::-1]:
            mnz = n-1-i
            e = Entry(self.fm, width=2)
            e.insert(END, 0)
            e.place(x=42*mnz+10, y=90)
            self.elemPX.append(e)
            if i != 0:
                l = Label(self.fm,text='x'+self.utf8s.get(i,'')+'+')
                l.place(x=42*mnz+30, y=90)
                self.lblPX.append(l)


    def createPY(self, event):
        n = int(self.cmbPY.get().strip())
        for e in self.elemPY:
            e.destroy()
        for l in self.lblPY:
            l.destroy()
        self.elemPY = []
        self.lblPY = []
        lst = list(range(n))
        for i in lst[::-1]:
            mnz = n-1-i
            e = Entry(self.fm, width=2)
            e.insert(END, 0)
            e.place(x=42*mnz+10, y=145)
            self.elemPY.append(e)
            if i != 0:
                l = Label(self.fm,text='x'+self.utf8s.get(i,'')+'+')
                l.place(x=42*mnz+30, y=145)
                self.lblPY.append(l)


    def clearWid(self):
        self.tAlice1["text"] = ""
        self.tAlice2["text"] = ""
        self.tAlice3["text"] = ""
        self.tAlice4["text"] = ""
        self.tAlice5["text"] = ""
        self.tAlice6["text"] = ""

        self.tBob1["text"] = ""
        self.tBob2["text"] = ""
        self.tBob3["text"] = ""
        self.tBob4["text"] = ""
        self.tBob5["text"] = ""
        self.tBob6["text"] = ""


    def createRezult(self, event):
        print("1")
        #imgA = ImageTk.PhotoImage(Image.open("alice.png"))
        #imgA = PhotoImage(file='alice.jpg')
        self.clearWid()
        my_thread = threading.Thread(target=self.threadRez)
        my_thread.start()
        

    def threadRez(self):
        # вычисляем сначала полином
        polinom = []
        np = len(self.elemPolinom)
        for i, e in enumerate(self.elemPolinom):
            if int(e.get().strip()) != 0:
                polinom.append(np-i-1)
        ppx = []
        nx = len(self.elemPX)
        for i, e in enumerate(self.elemPX):
            if int(e.get().strip()) != 0:
                ppx.append(nx-i-1)
        ppy = []
        ny = len(self.elemPY)
        for i, e in enumerate(self.elemPY):
            if int(e.get().strip()) != 0:
                ppy.append(ny-i-1)
        print(polinom)
        print(ppx)
        print(ppy)
        # вычисляет точку
        F = exp2bin(polinom)
        Xp = exp2bin(ppx)
        Yp = exp2bin(ppy)
        P = Point(Xp,Yp,F)
        P.padElements()
        N = 600
        # берем ключ Алисы и боба
        a = int(self.keyA.get().strip())
        b = int(self.keyB.get().strip())
        print("Примитивная точка P =",P.out())
        print("Примитивная точка P =",P.decOut())
        # шаг 1
        A = scalarMultPoint(P,a)
        B = scalarMultPoint(P,b)
        sp = '⮞'
        sl = '⮜'
        p = '―'
        smsa = '―A―⮞'
        smsb = '⮜―B―'
        # 1 - Алиса чет вычисляет
        self.liAlice = Label(self.fm, image=self.imgA)
        self.liAlice.place(x=10,y=300)
        time.sleep(self.pause1)
        self.tAlice1['text'] = "Алиса вычисляет А: " + str(A.out())
        time.sleep(self.pause1)
        self.tAlice2['text'] = "Алиса вычисляет А: " + str(A.decOut())
        time.sleep(self.pause1)

        # 2 - Боб чет вычисляет
        self.liBob = Label(self.fm, image=self.imgB)
        self.liBob.place(x=300,y=300)
        time.sleep(self.pause1)
        self.tBob1['text'] = "Боб вычисляет B: " + str(B.out())
        time.sleep(self.pause1)
        self.tBob2['text'] = "Боб вычисляет B: " + str(B.decOut())
        time.sleep(self.pause1)
        self.lSmsa["text"] = smsa
        for ii in range(9):
            time.sleep(0.5)
            self.lSmsa["text"] = p + self.lSmsa["text"]
            txt = '    '*(9-ii)
            txt = txt + smsb
            txt += p*ii
            self.lSmsb["text"] = txt
            #self.lSmsb["text"] = p + self.lSmsb["text"]
        A2 = scalarMultPoint(B,a)
        B2 = scalarMultPoint(A,b)
        self.tAlice3["text"] = "Алиса получает B: " + str(B.out())
        time.sleep(self.pause1)
        self.tAlice4["text"] = "Алиса вычисляет: " + str(A2.out())
        time.sleep(self.pause1)
        self.tAlice5["text"] = "Алиса получает B: " + str(B.decOut())
        time.sleep(self.pause1)
        self.tAlice6["text"] = "Алиса вычисляет: " + str(A2.decOut())
        time.sleep(self.pause1)
            
        self.tBob3["text"] = "Боб получает А: " + str(A.out())
        time.sleep(self.pause1)
        self.tBob4["text"] = "Боб вычисляет: " + str(B2.out())
        time.sleep(self.pause1)
        self.tBob5["text"] = "Боб получает А: " + str(A.decOut())
        time.sleep(self.pause1)
        self.tBob6["text"] = "Боб вычисляет:" + str(B2.decOut())
        C = scalarMultPoint(P,a*b)
        
        messagebox.showinfo("Общий ключ", "Алиса и Боб имеют общий ключ: " + str(C.out()) + " или " + str(C.decOut()))

mainWin()
