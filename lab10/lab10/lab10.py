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
    #print(res)
    return res

def hamming_coding_secdec(bits):
    p = []
    for i in range(0, len(bits), 4):
        p.append((bits[i] + bits[i+1] + bits[i+3])%2)
        p.append((bits[i] + bits[i+2] + bits[i+3])%2)
        p.append(bits[i])
        p.append((bits[i+1] + bits[i+2] + bits[i+3])%2)
        p.append(bits[i+1])
        p.append(bits[i+2])
        p.append(bits[i+3])
        parity_bit = sum(bits[i:i+3])%2
        p.append(parity_bit)
    return p


def sygnal_prosty(bity, czas_jednego_bitu, ilosc_probek_na_bit):
    czasy = []
    probki = []
    i = 0
    czas = 0
    for b in bity:
        for one_b in range(int(ilosc_probek_na_bit)):
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

def drawPlot(x, y, title = ""):
    if (type(x) == "float"):
         x = [x]
         y = [y]
    plt.plot(x, y, 1)
    plt.title(title)
    plt.xlabel('Czas')
    plt.ylabel('S(t)')




def demodulacja_amplitudowa(kluczowanie, kluczowanie_ones, ilosc_probek_na_bit, h):
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
    #return iloczyn_kluczowania, calki, demodulacja
    return demodulacja

def divide(bits, ilosc_probek_na_bit):
    n_bits = []
    for i in range(1, len(bits), ilosc_probek_na_bit):
        if((sum(bits[i:i+ilosc_probek_na_bit]) > ilosc_probek_na_bit/2)):
            n_bits.append(1)
        else:
            n_bits.append(0)
    return n_bits

def hamming_decoding_secdec(bits):
    d = []
    for i in range(0, len(bits), 8):
        p1 = ((bits[i] + bits[i+2] + bits[i+4]+ bits[i+6])%2)
        p2 = ((bits[i+1] + bits[i+2] + bits[i+5]+ bits[i+6])%2)
        p3 = ((bits[i+3] + bits[i+4] + bits[i+5]+ bits[i+6])%2)
        n = (p1 + p2 * 2 + p3 * 4) - 1
        if((sum(bits[i:i+7])%2) == bits[i+7] and n>=0):
            print("Blad")
            return None
        if(n>=0):
            print("Bit nr.", i+n, "jest niepoprawny")
            bits[i+n] = int(not bits[i+n])    
        d.append(bits[i+2])
        d.append(bits[i+4])
        d.append(bits[i+5])
        d.append(bits[i+6])
    return d

def convert_to_string(bits, littleEndian = False):
    values = [2 ** x for x in range(0, 8)]
    if not littleEndian:
        bits=bits[::-1]
    text = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        byte = 0
        for bit, value in zip(byte_bits, values):
            byte += bit * value
        text.append(chr(byte))
    return ''.join(text[::-1])


#zamiana tekstu na bity
text = "kot"
bits = S2BS(text, 0)
#kodowanie hammingiem
ham = hamming_coding_secdec(bits)
#syngal prosty
czas_jednego_bitu = 0.1
ilosc_probek_na_bit = 1000
czasy, probki = sygnal_prosty(ham, czas_jednego_bitu, ilosc_probek_na_bit)
#modulacja
f = 10
A1 = 0
A2 = 1
ask = kluczowanie_amplitudowe(czasy, probki, f, A1, A2)



#demodulacja
ones = []
prog = 2
for i in range(len(bits)*2):
    ones.append(1)

czasy, probki_ones = sygnal_prosty(ones, czas_jednego_bitu, ilosc_probek_na_bit)
ask_ones = kluczowanie_amplitudowe(czasy, probki_ones, f, A1, A2)
dask = demodulacja_amplitudowa(ask, ask_ones, ilosc_probek_na_bit, prog)
dem = divide(dask, ilosc_probek_na_bit)
#dekodowanie hamming
ham_d = hamming_decoding_secdec(dem)
print(ham_d)
print(bits)
print(np.array_equal(ham_d, bits))
#zamiana na string
text = convert_to_string(ham_d)
#rysowanko
plt.figure(figsize = (12,8))
plt.subplot(2, 1, 1)
drawPlot(czasy, probki,  "Sygnal prosty")
plt.subplot(2, 1, 2)
drawPlot(czasy, ask,  "Kluczowanie amplitudowe")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab10\\lab10\\' + 'modulacja' + '.png')






