from utils.iq_file_loader import load_iq_file
from scipy.fftpack import fft
from matplotlib import pyplot
import numpy as np

complex_data = np.array(load_iq_file('./data/sample-xl.dat'))

fig, ax = pyplot.subplots(2)
for i in range(50):
    sample = complex_data[i*1000:i*1000+10000]

    # Number of samplepoints
    N = 6000
    # sample spacing
    T = 1.0 / 800.0
    x = np.linspace(0.0, N*T, N)

    yf = fft(sample)

    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    # xf = np.linspace(0.0, 1.0/(2.0*T), N)

    ax[0].clear()
    ax[1].clear()
    ax[0].plot(sample.imag)
    ax[0].plot(sample.real)
    # ax[1].plot(xf, yf)
    ax[1].plot(xf, 2.0/N * np.abs(yf[:N//2]))
    pyplot.pause(0.1)


# spectrum = fft(complex_data)

# N=200
# T=100
# nf = np.linspace(0, 1.0/(2.0*T), N/2)
# pyplot.plot(nf, spectrum[0:N/2])

