import matplotlib.pyplot as plt
import numpy as np

def draw(filename, title):       
    x, y = np.loadtxt('I:\\transmisja_danych\\LAB03\\LAB03\\wynik\\' + filename, delimiter=';', unpack=True)
    #plt.clf()
    plt.stem(x, y, use_line_collection = True)
    plt.title('Wykres funkcji: ' + title)
    plt.xlabel('Czestotliwosc')
    plt.ylabel('Amplituda')
    #plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\' + filename + '.png')

def drawPlot(filename, title):
    x, y = np.loadtxt('I:\\transmisja_danych\\LAB03\\LAB03\\wynik\\' + filename, delimiter=';', unpack=True)
    #plt.clf()
    plt.scatter(x, y, 1)
    plt.title('Wykres funkcji: ' + title)
    plt.xlabel('Czas')
    plt.ylabel(title)
    #plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\' + filename + '.png')


plt.figure(figsize=(12,8))
plt.subplot(3, 2, 1)
drawPlot("p1.csv", "p1")
plt.subplot(3, 2, 2)
draw("skala_decybelowa_p1.csv", "p1")
plt.subplot(3, 2, 3)
drawPlot("p2.csv", "p2")
plt.subplot(3, 2, 4)
draw("skala_decybelowa_p2.csv", "p2")
plt.subplot(3, 2, 5)
drawPlot("p3.csv", "p3")
plt.subplot(3, 2, 6)
draw("skala_decybelowa_p3.csv", "p3")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\p.png')

plt.figure(figsize=(12,8))
plt.subplot(2, 1, 1)
drawPlot("v.csv", "v")
plt.subplot(2, 1, 2)
draw("skala_decybelowa_v.csv", "v")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\v.png')

plt.figure(figsize=(12,8))
plt.subplot(2, 1, 1)
drawPlot("u.csv", "u")
plt.subplot(2, 1, 2)
draw("skala_decybelowa_u.csv", "u")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\u.png')

plt.figure(figsize=(12,8))
plt.subplot(2, 1, 1)
drawPlot("z.csv", "z")
plt.subplot(2, 1, 2)
draw("skala_decybelowa_z.csv", "z")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\z.png')

plt.figure(figsize=(12,8))
plt.subplot(2, 1, 1)
drawPlot("x.csv", "x")
plt.subplot(2, 1, 2)
draw("skala_decybelowa_x.csv", "x")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\x.png')

plt.figure(figsize=(12,8))
plt.subplot(2, 1, 1)
drawPlot("y.csv", "y")
plt.subplot(2, 1, 2)
draw("skala_decybelowa_y.csv", "y")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\y.png')

plt.figure(figsize=(12,8))
plt.subplot(1, 3, 1)
drawPlot("probkowanie.csv", "s(t)")
plt.subplot(1, 3, 2)
draw("widmo.csv", "s(t)(dft)")
plt.subplot(1, 3, 3)
draw("skala_decybelowa.csv", "s(t)(dft)(db)")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\zadanie2.png')

plt.figure(figsize=(12,8))
plt.subplot(1, 3, 1)
drawPlot("probkowanie.csv", "s(t)")
plt.subplot(1, 3, 2)
draw("skala_decybelowa.csv", "s(t)(dft)(db)")
plt.subplot(1, 3, 3)
drawPlot("odwrocenie.csv", "s(t)(dft)(db)")
plt.tight_layout()
plt.savefig('I:\\transmisja_danych\\LAB03\\LAB03\\wykresy\\zadanie3.png')