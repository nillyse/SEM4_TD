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
        for one_b in range(int(ilosc_probek_na_bit)):
            czasy.append(czas)
            czas = czas + czas_jednego_bitu
            probki.append(b)
    czasy = [czas / ilosc_probek_na_bit for czas in czasy]
    return czasy, probki

def menchester(clk, ttl):
    res = []
    res.append(0)
    for i in range(1, len(clk)):
        if (clk[i-1] == 0 and clk[i] == 1): #narastajace
            if(ttl[i-1] == ttl[i]):
                res.append(-res[i-1])
            else:
                res.append(res[i-1])
        elif(clk[i-1] == 1 & clk[i] == 0):
            if(ttl[i] == 1):
                res.append(-1)
            else:
                res.append(1)
        else:
            res.append(res[i-1])
    return res

def nrzi(clk, ttl):
    res = []
    res.append(0)
    for i in range(1, len(clk)):
         if (clk[i-1] == 1 and clk[i] == 0): #opadajace
            if(ttl[i-1] == 1):
                if res[i-1] == 0:
                    #zaczynami od 1
                    res.append(-1)
                else:
                    res.append(-res[i-1])
            else:
                res.append(res[i-1])
         else:
             res.append(res[i-1])
    return res


def bami(clk, ttl):
    res = []
    res.append(0)
    previous = 0
    for i in range(1, len(clk)):
        if(ttl[i] == 0):
            res.append(0)
        elif(clk[i-1] == 0 and clk[i] == 1): #narastajace
            if(previous == 0):
                res.append(1)
                previous = 1
            else:
                res.append(-previous)
                previous = -previous
        else:
            res.append(res[i-1])
    return res


def drawPlot(x, y, title = ""):
    if (type(x) == "float"):
         x = [x]
         y = [y]
    plt.plot(x, y, 1)
    plt.title(title)
    plt.xlim(0, max(x))
    plt.xlabel('Czas')
    plt.ylabel('S(t)')


clk = []






czas_jednego_bitu = 1
ilosc_probek_na_bit = 250

ttl = S2BS("kot", 1)
for i in range(len(ttl)):
    clk.append(1)
    clk.append(0)
ttl_time, ttl = sygnal_prosty(ttl, czas_jednego_bitu, ilosc_probek_na_bit)
clk_time, clk = sygnal_prosty(clk, czas_jednego_bitu/2, ilosc_probek_na_bit/2)
res_m = menchester(clk, ttl)
res_nrzi = nrzi(clk, ttl)
res_bami = bami(clk, ttl)

plt.figure(figsize = (12,8))
plt.subplot(5, 1, 1)
drawPlot(clk_time, clk,  "clk")
plt.subplot(5, 1, 2)
drawPlot(ttl_time ,ttl,  "ttl")
plt.subplot(5, 1, 3)
drawPlot(clk_time, res_m, "Kodowanie Manchester")
plt.subplot(5, 1, 4)
drawPlot(clk_time, res_nrzi, "Kodowanie NRZI")
plt.subplot(5, 1, 5)
drawPlot(clk_time, res_bami, "Kodowanie BAMI")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab08\\lab08\\' + 'kodowanie' + '.png')


