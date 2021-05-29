import matplotlib.pyplot as plt
import numpy as np

def drawPlot(functionName):
    x, y = np.loadtxt('I:\\transmisja_danych\\lab01\\lab01\\' + functionName + '.csv', delimiter=';', unpack=True, skiprows = 1)
    plt.clf()
    plt.plot(x, y)
    plt.title('Wykres funkcji: ' + functionName + '(x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('I:\\transmisja_danych\\lab01\\lab01\\' + functionName + '.png')

drawPlot('x')
drawPlot('y')
drawPlot('z')
drawPlot('u')
drawPlot('v')
drawPlot('p1')
drawPlot('p2')
drawPlot('p3')

