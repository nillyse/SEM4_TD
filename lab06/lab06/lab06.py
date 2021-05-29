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
    plt.title('Funkcja: ' + title)
    plt.xlabel('Czas')
    plt.ylabel(title)
    


def widmo_amplitudowa(fourier):
    widmo = []
    for x in fourier:
        widmo.append(m.sqrt(m.pow(x.real, 2) + m.pow(x.imag, 2))/len(fourier))
    return widmo

def skala_decybelowa(widmo):
    skala = []
    for x in widmo:
        skala.append(10 * m.log10(x))
    return skala

def skala_czestotliwosci(czestotliwosc, n):
    skala = []
    i = 0
    while i<n:
        skala.append(i* (czestotliwosc/n))
        i = i + 1
    return skala


def filtr(wartosci, skala_cz, prog):
    wynik = []
    wynik_s = []
    for x, y in zip(wartosci, skala_cz):
        if (x > prog):
            wynik.append(x)
            wynik_s.append(y)
    return wynik, wynik_s


#STAŁE
N = 2
czas_jednego_bitu = 1
ilosc_probek_na_bit = 250
A1 = 0.4
A2 = 3
f = N * pow(czas_jednego_bitu, -1)

a = S2BS("kot", 1)
#kot - 01101010110111101110100 - big endian 
#00101110111101101010110 - little endian
czasy, probki = sygnal_prosty(a, czas_jednego_bitu, ilosc_probek_na_bit)
za = kluczowanie_amplitudowe(czasy, probki, f, A1, A2)
zf = kluczowanie_czestotliwosciowe(czasy, probki, N, czas_jednego_bitu)
zp = kluczowanie_fazowe(czasy, probki, f)

plt.figure(figsize = (12,8))
plt.subplot(3, 1, 1)
drawPlot(czasy, probki)
drawPlot(czasy, za,  "S(t), kluczowanie amplitudowe")
plt.subplot(3, 1, 2)
drawPlot(czasy, probki)
drawPlot(czasy, zf,  "S(t), kluczowanie czestotliwosciowe")
plt.subplot(3, 1, 3)
drawPlot(czasy, probki)
drawPlot(czasy, zp, "S(t), kluczowanie fazowe")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab06\\lab06\\' + 'zad2' + '.png')


end = 10 * ilosc_probek_na_bit

plt.figure(figsize = (12,8))
plt.subplot(3, 1, 1)
drawPlot(czasy[0:end], probki[0:end])
drawPlot(czasy[0:end], za[0:end], "S(t), kluczowanie amplitudowe")
plt.subplot(3, 1, 2)
drawPlot(czasy[0:end], probki[0:end])
drawPlot(czasy[0:end], zf[0:end], "S(t), kluczowanie czestotliwosciowe")
plt.subplot(3, 1, 3)
drawPlot(czasy[0:end], probki[0:end])
drawPlot(czasy[0:end], zp[0:end], "S(t), kluczowanie fazowe")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab06\\lab06\\' + 'zad3' + '.png')


skala_cz = skala_czestotliwosci(ilosc_probek_na_bit/czas_jednego_bitu, len(probki))

fourier_za = dft.fft(za)
fourier_zf = dft.fft(zf)
fourier_zp = dft.fft(zp)

widmo_a_za = widmo_amplitudowa(fourier_za)
widmo_a_zf = widmo_amplitudowa(fourier_zf)
widmo_a_zp = widmo_amplitudowa(fourier_zp)

skala_cz = skala_cz[0:round(len(widmo_a_za)/2)]
widmo_a_za = widmo_a_za[0:round(len(widmo_a_za)/2)]
widmo_a_zf = widmo_a_zf[0:round(len(widmo_a_zf)/2)]
widmo_a_zp = widmo_a_zp[0:round(len(widmo_a_zp)/2)]

widmo_a_za = skala_decybelowa(widmo_a_za)
widmo_a_zf = skala_decybelowa(widmo_a_zf)
widmo_a_zp = skala_decybelowa(widmo_a_zp)

widmo_a_za, skala_cz_za = filtr(widmo_a_za, skala_cz, -3)
widmo_a_zf, skala_cz_zf = filtr(widmo_a_zf, skala_cz, -10)
widmo_a_zp, skala_cz_zp = filtr(widmo_a_zp, skala_cz, -10)




plt.figure(figsize = (12,8))
plt.subplot(3, 1, 1)
draw(skala_cz_za, widmo_a_za, "S(t), kluczowanie amplitudowe")
plt.subplot(3, 1, 2)
draw(skala_cz_zf, widmo_a_zf, "S(t), kluczowanie czestotliwosciowe")
plt.subplot(3, 1, 3)
draw(skala_cz_zp, widmo_a_zp, "S(t), kluczowanie fazowe")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab06\\lab06\\' + 'zad4' + '.png')

#5
# f(min) = 2 f(max) = 2 W = 0 - amplitudowe
# f(min) = 3 f(max) = 4  W = 1 - czestotliwosciowe
# f(min) =  1.62 f(max) = 2.38 W = 0.76 - fazowe