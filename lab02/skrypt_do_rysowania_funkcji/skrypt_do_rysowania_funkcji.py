import matplotlib.pyplot as plt
import numpy as np

def drawPlot(filename, title):
    x, y = np.loadtxt('I:\\transmisja_danych\\lab02\\lab02\\' + filename + '.csv', delimiter=';', unpack=True)
    plt.clf()
    plt.scatter(x, y, 1)
    plt.title('Wykres funkcji: ' + title)
    plt.xlabel('t')
    plt.ylabel('s(t)')
    plt.savefig('I:\\transmisja_danych\\lab02\\lab02\\' + filename + '.png')


drawPlot("probkowanie", "S(t)")
drawPlot("kwantyzacja","S(t)(skwantyzowane)")
drawPlot("kwantyzacja2","S(t)(skwantyzowane ze zmniejszonym q i fs")