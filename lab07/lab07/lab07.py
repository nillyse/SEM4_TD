
import math as m
import csv
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as dft

def S2BS(text, isLittle):
    res = ''.join(format(ord(i), '08b') for i in text) 
    res = [char == "1" for char in res]
    if(isLittle):
        res.reverse()
    print(res)
    return res
     
def sygnal_prosty(bity, czas_jednego_bitu, ilosc_probek_na_bit):
    czasy = []
    probki = []
    i = 0
    czas = 0
    for b in bity:
        for one_b in range(ilosc_probek_na_bit):
            czasy.append(czas)
            czas = czas + czas_jednego_bitu
            probki.append(b)
    czasy = [czas / ilosc_probek_na_bit for czas in czasy]
    return czasy, probki

       
       


def kluczowanie_amplitudowe(czasy, probki, f, A1, A2):
    res = []
    for cz, p in zip(czasy,probki):
        if (p == 0):
            res.append(A1* m.sin(2*m.pi * f * cz))
        else:
            res.append(A2* m.sin(2*m.pi * f * cz))
    return res


def kluczowanie_czestotliwosciowe(czasy, probki, N, czas_jednego_bitu):
    f0 = (N+1)/czas_jednego_bitu
    f1 = (N+2)/czas_jednego_bitu
    res = []
    for cz, p in zip(czasy,probki):
        if (p == 0):
            res.append(m.sin(2*m.pi * f0 * cz))
        else:
            res.append(m.sin(2*m.pi * f1 * cz))
    return res


def kluczowanie_fazowe(czasy, probki, f):
     res = []
     for cz, p in zip(czasy,probki):
        if (p == 0):
            res.append(m.sin(2*m.pi * f * cz))
        else:
            res.append(m.sin(2*m.pi * f * cz + m.pi))
     return res



def demodulacja_amplitudowa_fazowa(kluczowanie, kluczowanie_ones, ilosc_probek_na_bit, h):
    iloczyn_kluczowania = []
    for i, j in zip(kluczowanie, kluczowanie_ones):
        iloczyn_kluczowania.append(i*j)
    calki = []
    index = 0
    for i in range(round(len(iloczyn_kluczowania)/ilosc_probek_na_bit)):
        for j in range(ilosc_probek_na_bit):
            if(index == i * ilosc_probek_na_bit or (i == 0 and j == 0)):
                calki.append(iloczyn_kluczowania[index])
            else:
                calki.append(calki[index - 1] + iloczyn_kluczowania[index])
            index += 1
    demodulacja = []
    for i in calki:
        if(i < h):
            demodulacja.append(0)
        else:
            demodulacja.append(1)
    return iloczyn_kluczowania, calki, demodulacja


            
def demodulacja_czestotliwosciowa(kluczowanie, kluczowanie_ones, kluczowanie_zeros, ilosc_probek_na_bit, h):
    iloczyn_kluczowania_zeros = []
    iloczyn_kluczowania_ones = []
    for i, j, k in zip(kluczowanie, kluczowanie_zeros, kluczowanie_ones):
            iloczyn_kluczowania_zeros.append(i*j)
            iloczyn_kluczowania_ones.append(i*k)
    calki_zeros = []
    calki_ones = []
    index = 0
    for i in range(round(len(iloczyn_kluczowania_zeros)/ilosc_probek_na_bit)):
        for j in range(ilosc_probek_na_bit):
            if(index == i * ilosc_probek_na_bit or (i == 0 and j == 0)):
                calki_zeros.append(iloczyn_kluczowania_zeros[index])
                calki_ones.append(iloczyn_kluczowania_ones[index])
            else:
                calki_zeros.append(calki_zeros[index - 1] + iloczyn_kluczowania_zeros[index])
                calki_ones.append(calki_ones[index - 1] + iloczyn_kluczowania_ones[index])
            index += 1
    calki = []
    for i, j in zip(calki_zeros, calki_ones):
        calki.append(j-i)
    demodulacja = []
    for i in calki:
        if(i < h):
            demodulacja.append(0)
        else:
            demodulacja.append(1)
    return iloczyn_kluczowania_zeros, iloczyn_kluczowania_ones, calki, demodulacja



def draw(x, y, title = ""):    
    if (type(x) == "float"):
         x = [x]
         y = [y]
    plt.stem(x, y, use_line_collection = True)
    plt.title('Funkcja: ' + title)
    plt.xlabel('Czestotliwosc')
    plt.ylabel('Amplituda')

def drawPlot(x, y, title = ""):
    if (type(x) == "float"):
         x = [x]
         y = [y]
    plt.plot(x, y, 1)
    plt.title(title)
    plt.xlabel('Czas')
    plt.ylabel('S(t)')


#STAŁE
N = 2
czas_jednego_bitu = 1
ilosc_probek_na_bit = 250
A1 = 0
A2 = 3
f = N * pow(czas_jednego_bitu, -1)

a = S2BS("kot", 1)
#kot - 01101010110111101110100 - big endian 
#00101110111101101010110 - little endian
czasy, probki = sygnal_prosty(a, czas_jednego_bitu, ilosc_probek_na_bit)
za = kluczowanie_amplitudowe(czasy, probki, f, A1, A2)
zf = kluczowanie_czestotliwosciowe(czasy, probki, N, czas_jednego_bitu)
zp = kluczowanie_fazowe(czasy, probki, f)
end = 10 * ilosc_probek_na_bit





h = 50
ones = []
zeros = []
for i in range(len(a)):
    ones.append(1)
    zeros.append(0)
czasy, probki_ones = sygnal_prosty(ones, czas_jednego_bitu, ilosc_probek_na_bit)
czasy, probki_zeros = sygnal_prosty(zeros, czas_jednego_bitu, ilosc_probek_na_bit)
za_ones = kluczowanie_amplitudowe(czasy, probki_ones, f, A1, A2)
zf_ones = kluczowanie_czestotliwosciowe(czasy, probki_ones, N, czas_jednego_bitu)
zf_zeros = kluczowanie_czestotliwosciowe(czasy, probki_zeros, N, czas_jednego_bitu)
zp_ones = kluczowanie_fazowe(czasy, probki_ones, f)

iloczyn_a, calki_a, demodulacja_a = demodulacja_amplitudowa_fazowa(za, za_ones, ilosc_probek_na_bit, h)
iloczyn_p, calki_p, demodulacja_p = demodulacja_amplitudowa_fazowa(zp, zp_ones, ilosc_probek_na_bit, h)
iloczyn_f_zeros, iloczyn_f_ones, calki_f, demodulacja_f = demodulacja_czestotliwosciowa(zf, zf_ones, zf_zeros, ilosc_probek_na_bit, h)


plt.figure(figsize = (12,8))
plt.subplot(4, 1, 1)
drawPlot(czasy, za,  "Kluczowanie amplitudowe")
plt.subplot(4, 1, 2)
drawPlot(czasy, iloczyn_a,  "Iloczyn")
plt.subplot(4, 1, 3)
drawPlot(czasy, calki_a, "Całka")
plt.subplot(4, 1, 4)
drawPlot(czasy, demodulacja_a, "Demodulacja")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab07\\lab07\\' + 'Demodulacja_amplitudowa' + '.png')



plt.figure(figsize = (12,8))
plt.subplot(4, 1, 1)
drawPlot(czasy, zp,  "Kluczowanie fazowe")
plt.subplot(4, 1, 2)
drawPlot(czasy, iloczyn_p,  "Iloczyn")
plt.subplot(4, 1, 3)
drawPlot(czasy, calki_p, "Całka")
plt.subplot(4, 1, 4)
drawPlot(czasy, demodulacja_p, "Demodulacja")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab07\\lab07\\' + 'Demodulacja_fazowa' + '.png')



plt.figure(figsize = (12,8))
plt.subplot(5, 1, 1)
drawPlot(czasy, zf,  "Kluczowanie częstotliwościowe")
plt.subplot(5, 1, 2)
drawPlot(czasy, iloczyn_f_ones,  "Iloczyn(jedynki)")
plt.subplot(5, 1, 3)
drawPlot(czasy, iloczyn_f_zeros,  "Iloczyn(zera)")
plt.subplot(5, 1, 4)
drawPlot(czasy, calki_f, "Całki")
plt.subplot(5, 1, 5)
drawPlot(czasy, demodulacja_f, "Demodulacja")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab07\\lab07\\' + 'Demodulacja_czestotliwosciowa' + '.png')
plt.show()