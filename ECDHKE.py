#################Point Class#################
class Point:
    def __init__(self, X, Y, F):
        ##X и Y - элементы конечного поля
        ##ie x^5 + x^3 + x + 1 = [1,1,0,1,0,1]
        self.X = X.copy()
        self.Y = Y.copy()
        ##F - многочлен, неприводимый над конечным полем
        self.F = F.copy()
        ##Поле GF (2 ^ n)
        self.n = len(self.F) - 1

    def getX(self):
        return self.X.copy()

    def getY(self):
        return self.Y.copy()

    def getF(self):
        ##получаем неприводимый полином
        return self.F.copy()

    def getN(self):
        ##олучить n, где GF (2 ^ n)
        return self.n

    def padElements(self):
        l = self.n
        self.X += [0]*(l-len(self.X))
        self.Y += [0]*(l-len(self.Y))

    def isEqual(self, P):
        X1 = self.X.copy()
        Y1 = self.Y.copy()
        X2 = P.X.copy()
        Y2 = P.Y.copy()
        l = max(len(X1),len(X2),len(Y1),len(Y2))
        X1 += [0]*(l-len(X1))
        Y1 += [0]*(l-len(Y1))
        X2 += [0]*(l-len(X2))
        Y2 += [0]*(l-len(Y2))
        ##проверить, равны ли
        if (X1 == X2 and Y1 == Y2):
            return True
        else:
            return False

    def onCurve(self):
        return onCurve(self.getX(),self.getY(),self.getF())

    def add(self, P):
        return addPoints(self, P)

    def mult(self, k):
        return scalarMultPoint(self, k)

    def out(self):
        ##Возвращает точку в виде двоичной строки для печати
        x = ""
        y = ""
        for i in reversed(self.X.copy()):
            x += str(i)
        for i in reversed(self.Y.copy()):
            y += str(i)
        return("("+x+", "+y+")")
        
    def decOut(self):
        ##Возвращает точку в виде десятичной строки для печати
        x = 0
        y = 0
        for i in range(len(self.X)):
            x += self.X[i] * 2**i
        for i in range(len(self.Y)):
            y += self.Y[i] * 2**i
        return("("+str(x)+", "+str(y)+")")

    def printPoly(self):
        poly = "("
        poly += printPoly(self.getX())
        poly += ", "
        poly += printPoly(self.getY())
        poly += ")"
        return poly

    def copy(self):
        return Point(self.X.copy(),self.Y.copy(),self.F.copy())

#################Функции конечных элементов поля#################
def multFFE(A,B,F):
    ##Умножьте два элемента конечного поля
    ## Выход = A (x) B (x) mod F (x) mod 2
    A = A.copy()
    B = B.copy()
    F = F.copy()
    if (F[-1] != 1):
        print("Убедитесь, что степень F (x) правильная")
    if (len(A)>len(F) or len(B)>len(F)):
        print("Убедитесь, что A (x) и B (x) уже уменьшены")
    l = len(F)
    A += [0]*(l-len(A))
    B += [0]*(l-len(B))
    C = [0]*(l*2)
    ## Умножить (сдвинуть и сложить)
    for i in range(l):
        C = addFFE(C,B[i]*A)
        A = [0] + A
    ##mod F
    C.reverse()
    F.reverse()
    ## проверить, равен ли C 0
    if C.count(1) == 0:
        return [0]*(l-1)
   ## убедитесь, что они начинаются с 1
    C = C[C.index(1):]
    F = F[C.index(1):]
    ## начать деление
    while(len(C) >= len(F)):
        C = addFFE(C,F)
        C = C[C.index(1):]
    C.reverse()
    return C

def inverseFFE(A,F):
    ##Инверсия конечного элемента поля
    ##(2 ^ n) -2 = 2 ^ (n-1) + 2 ^ (n-2) + ... + 2
    m = len(F) - 1
    temp = multFFE(A,A,F)
    output = temp.copy()
    while (m > 2):
        temp = multFFE(temp,temp,F)
        output = multFFE(output,temp,F)
        m -= 1
    return output

def addFFE(A,B):
    ##Добавьте два конечных элемента поля (все, что они делают, это XOR их)
    ##Выход = A (x) + B (x) mod 2 
    A = A.copy()
    B = B.copy()
    l = max(len(A),len(B))
    
    A += [0]*(l-len(A))
    B += [0]*(l-len(B))
    C = []
    for i in range(l):
        ## ^ это оператор XOR
        C.append(A[i]^B[i])
    return C

#################Point Functions#################
def addPoints(P1,P2):
    ##добавить точки по эллиптической кривой y ^ 2 + xy = x ^ 3 + x ^ 2 + 1
    ##где кривая больше GF (2 ^ n)
    F = P1.getF()
    if (P1.isEqual(P2)):
        ## вычислить лямбду
        t1 = multFFE(P1.getY(),inverseFFE(P1.getX(),F),F)
        t2 = P1.getX()
        s = addFFE(t1, t2)
       ## рассчитать X3
        t1 = multFFE(s,s,F)
        t2 = s
        t3 = [1]
        X3 = addFFE(t1,t2)
        X3 = addFFE(X3,t3)
    else:
        ## вычислить лямбду
        num = addFFE(P1.getY(),P2.getY())
        den = addFFE(P1.getX(),P2.getX())
        s = multFFE(num,inverseFFE(den,F),F)
        ## рассчитать X3
        t1 = addFFE(multFFE(s,s,F),s)
        t2 = addFFE(P1.getX(),P2.getX())
        t3 = [1]
        X3 = addFFE(t1,t2)
        X3 = addFFE(X3,t3)
   ## рассчитать Y3
    t1 = multFFE(addFFE(P1.getX(),X3),s,F)
    t2 = X3
    t3 = P1.getY()
    Y3 = addFFE(t1,t2)
    Y3 = addFFE(Y3,t3)
    ## создать точку
    P3 = Point(X3,Y3,F)
    return P3

def scalarMultPoint(P,k):
    temp = P.copy()
    output = 0
    K = int2bin(k)
    for i in K:
        if (i == 1):
            if (output == 0):
                output = temp.copy()
            else:
                output = addPoints(output,temp)
        temp = addPoints(temp,temp)
    return output

def onCurve(X,Y,F):
    ## эллиптическая кривая имеет форму y ^ 2 + xy = x ^ 3 + x ^ 2 + 1 над GF (2 ^ n)
    l = len(F) - 1
    left = addFFE(multFFE(Y,Y,F),multFFE(X,Y,F))
    left += [0]*(l-len(left))
    t2 = multFFE(X,X,F)
    t1 = multFFE(X,t2,F)
    t3 = [1]
    right = addFFE(t1,t2)
    right = addFFE(right,t3)
    right += [0]*(l-len(right))
    if (left == right):
        return True
    else:
        return False

#################Функции эллиптической кривой#################
def orderPoint(A,P,N):
    ##Найти порядок точки A на EC
    ##N - количество точек по EC
    ##P является примитивной точкой на ЕС
    ##эллиптическая кривая имеет форму y ^ 2 + xy = x ^ 3 + x ^ 2 + 1 над GF (2 ^ n)
    temp = P.copy()
    ## Найти k, где kP = a
    for k in range(1,N):
        if temp.isEqual(A):
            break
        temp = addPoints(temp,P)
    for i in range(1,N+1):
        if (k*i%N==0):
            return i
    return 0

def orderSimple(i,E):
    for x in range(1,E+1):
        if(i*x%E==0):
            return x
    return 0

def numberPoints(F):
    ## получить количество точек по ЕС
    ## F - неприводимый многочлен
    ## эллиптическая кривая имеет форму y ^ 2 + xy = x ^ 3 + x ^ 2 + 1 над GF (2 ^ n)
    pointList = []
    l = len(F) - 1
    i = 0
    for xi in range(2**l):
        X = int2bin(xi)
        for yi in range(2**l):
            Y = int2bin(yi)
            ## Проверьте все точки, чтобы проверить, на кривой ли
            if (onCurve(X,Y,F)):
                i += 1
                pointList.append(Point(X,Y,F))
        if (xi%30 == 0):
            i += 1
    print("Количество точек =",str(i))
    return i

def maximalPoints(P,N):
    ##Примитивная точка P
    ##N = количество точек на кривой E
    P.padElements()
    testPoint = P.copy()
    i = 1
    while(True):
        order = orderSimple(i,N)
        if (testPoint.onCurve() == False):
            print("Ошибка: точка",testPoint.out(),"не на кривой!")
            break
        if (order == N):
            ## Печать максимальных точек
            print (i,"P =",testPoint.out(),"ord =",str(order))
        if(testPoint.getX() == P.getX() and i > 1 and i < N-1):
            print("Ошибка: не начинается с примитивного элемента")
            break
        if(i==N-1):
            break
        i += 1
        testPoint = addPoints(testPoint,P)
        testPoint.padElements()
    return 0

#################Функции списка#################
def printPoly(P):
    output = ""
    if (P[0] == 1):
        output = "1"
    for i in range (1,len(P)):
        if (P[i] == 1):
            output = "X^" + str(i) + " + " + output
    if (output[-2] == "+"):
        output = output[0:-3]
    return output

def exp2bin(exp):
    ### принимает список показателей и конвертирует в двоичный список
    ## x^5 + x^3 + x + 1 == [5,3,1,0] => [1,1,0,1,0,1]
    output = [0] * (max(exp) + 1)
    for i in exp:
        output[i] = 1
    return output

def str2bin(s):
    ## Вход: "10111" Выход: [1,1,1,0,1]
    s = list(s)
    s.reverse()
    for i in range(len(s)):
        s[i] = int(s[i])
    return s

def hex2bin(h):
   ## принимает шестнадцатеричную строку и преобразует в двоичный список в обратном порядке
    ## "50" => 0101 0000 => [0,0,0,0,1,0,1,0]
    output = []
    hexTable = ['0000', '0001', '0010', '0011',
                '0100', '0101', '0110', '0111',
                '1000', '1001', '1010', '1011',
                '1100', '1101', '1110', '1111']
    for c in h:
        output += list(hexTable[int(c,16)])
    output.reverse()
    for i in range(len(output)):
        output[i] = int(output[i])
    return output

def int2bin(i):
    ##принимает десятичное целое число и преобразует в двоичный список в обратном порядке
    if (i == 0):
        return [0]
    ##сначала преобразовать в шестнадцатеричную строку
    h = hex(i)[2:]
    output = hex2bin(h)
    ##удалить конечные 0
    output.reverse()
    output = output[output.index(1):]
    output.reverse()
    return output
'''
#################ECDHKE#################
##неприводимый полином
F = exp2bin([9,8,0])
##Примитивная точка
Xp = exp2bin([1,0])
Yp = exp2bin([5,4,3])
P = Point(Xp,Yp,F)
P.padElements()
##N = numberPoints(F)
N = 600
##Закрытый ключ Алисы и Боба
a = 21
b = 34
print("Примитивная точка P =",P.out())
print("Примитивная точка P =",P.decOut())
##Step 1
print("Шаг 1")
A = scalarMultPoint(P,a)
B = scalarMultPoint(P,b)
print("Алиса вычисляет  = A =",A.out())
print("Алиса вычисляет  = A =",A.decOut())
print("И отправляет точку А Бобу")
print("Боб вычисляет  = B =",B.out())
print("Боб вычисляет  = B =",B.decOut())
print("И отправляет точку B Алисе")
##Step 2
print("Step 2")
A2 = scalarMultPoint(B,a)
B2 = scalarMultPoint(A,b)
print("Алиса получает B =",B.out(),"и вычисляет =",A2.out())
print("Алиса получает B =",B.decOut(),"и вычисляет =",A2.decOut())
print("Боб получает A =",A.out(),"и вычисляет A =",B2.out())
print("Боб получает A =",A.decOut(),"и вычисляет A =",B2.decOut())
##Подтверждение
C = scalarMultPoint(P,a*b)
print("Обе стороны имеют общий ключ",C.out())
print("Обе стороны имеют общий ключ",C.decOut())
##get Maximal Points
#print("Maximal Points")
#m = maximalPoints(P,N)

'''
