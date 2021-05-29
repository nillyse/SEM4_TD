import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def draw(filename, title):       
    x, y = np.loadtxt('I:\\transmisja_danych\\lab04\\lab04\\' + filename, delimiter=';', unpack=True)
    #plt.clf()
    if (type(x) == np.float64):
        x = [x]
        y = [y]
        

    plt.stem(x, y, use_line_collection = True)
    plt.title('Wykres funkcji: ' + title)
    plt.xlabel('Czestotliwosc')
    plt.ylabel('Amplituda')
    #plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\' + filename + '.png')

def drawPlot(filename, title):
    x, y = np.loadtxt('I:\\transmisja_danych\\lab04\\lab04\\' + filename, delimiter=';', unpack=True)
    if (type(x) == "float"):
         x = [x]
         y = [y]
    #plt.clf()
    plt.scatter(x, y, 1)
    plt.title('Wykres funkcji: ' + title)
    plt.xlabel('Czas')
    plt.ylabel(title)
    #plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\' + filename + '.png')


plt.figure(figsize=(12,8))
plt.subplot(5, 1, 1)
drawPlot("probkowanie.csv", "S(t), ka = 0.75, kp = 0")
plt.subplot(5, 1, 2)
drawPlot("modulacja_amplitudowa_1.csv", "S(t), modulacja amplitudowa")
plt.subplot(5, 1, 3)
draw("modulacja_amplitudowa_db_1.csv", "S(t), modulacja amplitudowa w db")
plt.subplot(5, 1, 4)
drawPlot("modulacja_fazowa_1.csv", "S(t) ,modulacja fazowa")
plt.subplot(5, 1, 5)
draw("modulacja_fazowa_db_1.csv", "S(t), modulacja fazowa w db")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab04\\lab04\\1.png')

plt.figure(figsize=(12,8))
plt.subplot(5, 1, 1)
drawPlot("probkowanie.csv", "S(t), ka = 8, kp = 2.5")
plt.subplot(5, 1, 2)
drawPlot("modulacja_amplitudowa_2.csv", "S(t), modulacja amplitudowa")
plt.subplot(5, 1, 3)
draw("modulacja_amplitudowa_db_2.csv", "S(t), modulacja amplitudowa w db")
plt.subplot(5, 1, 4)
drawPlot("modulacja_fazowa_2.csv", "S(t), modulacja fazowa")
plt.subplot(5, 1, 5)
draw("modulacja_fazowa_db_2.csv", "S(t), modulacja fazowa w db")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab04\\lab04\\2.png')

plt.figure(figsize=(12,8))
plt.subplot(5, 1, 1)
drawPlot("probkowanie.csv", "S(t), ka = 8, kp = 2.5")
plt.subplot(5, 1, 2)
drawPlot("modulacja_amplitudowa_3.csv", "S(t), modulacja amplitudowa")
plt.subplot(5, 1, 3)
draw("modulacja_amplitudowa_db_3.csv", "S(t), modulacja amplitudowa w db")
plt.subplot(5, 1, 4)
drawPlot("modulacja_fazowa_3.csv", "S(t), modulacja fazowa")
plt.subplot(5, 1, 5)
draw("modulacja_fazowa_db_3.csv", "S(t), modulacja fazowa w db")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\lab04\\lab04\\3.png')
