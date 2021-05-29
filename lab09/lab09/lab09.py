import math as m
import csv
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as dft


def S2BS(text, isLittle):
    res = ''.join(format(ord(i), '08b') for i in text) 
    res = [char == "1" for char in res]
    res = [int(char) for char in res]
    if(isLittle):
        res.reverse()
    print(res)
    return res

def hamming_coding(bits):
    p = []
    for i in range(0, len(bits), 4):
        p.append((bits[i] + bits[i+1] + bits[i+3])%2)
        p.append((bits[i] + bits[i+2] + bits[i+3])%2)
        p.append(bits[i])
        p.append((bits[i+1] + bits[i+2] + bits[i+3])%2)
        p.append(bits[i+1])
        p.append(bits[i+2])
        p.append(bits[i+3])
    return p

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

def hamming_decoding(bits):
    d = []
    for i in range(0, len(bits), 7):
        p1 = ((bits[i] + bits[i+2] + bits[i+4]+ bits[i+6])%2)
        p2 = ((bits[i+1] + bits[i+2] + bits[i+5]+ bits[i+6])%2)
        p3 = ((bits[i+3] + bits[i+4] + bits[i+5]+ bits[i+6])%2)
        n = (p1 + p2 * 2 + p3 * 4) - 1
        if(n>=0):
            print("Bit nr.", i+n, "jest niepoprawny")
            bits[i+n] = int(not bits[i+n])    
        d.append(bits[i+2])
        d.append(bits[i+4])
        d.append(bits[i+5])
        d.append(bits[i+6])
    return d

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

def zepsuj(bits, nr):
    bits[nr] = int(not bits[nr])
    return bits


bits = S2BS('kot', 0)
# 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0
ham = hamming_coding(bits)
print(ham)
#1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0
ham = zepsuj(ham, 2)
ham_d = hamming_decoding(ham)
print(ham_d)
#0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0


ham = hamming_coding_secdec(bits)
print(ham)
#1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1
ham = zepsuj(ham, 1)
ham_d = hamming_decoding_secdec(ham)
print(ham_d)
#0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0
ham = zepsuj(ham, 1)
ham = zepsuj(ham, 2)
ham_d = hamming_decoding_secdec(ham)
#Nie można zdekodować

