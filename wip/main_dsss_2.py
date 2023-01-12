from math import pi, sin
from utils.prn_codes import create_G2i_code
from utils.iq_file_loader import load_iq_file
import pylab as plt
import numpy as np
from numpy import fft
from scipy.signal import periodogram, welch

import matplotlib.pyplot as plt
from matplotlib import rcParams

f = 154*10.23e6 # Carrier frequency
f_prn = 10.23e6 / 10 # PRN frequency
sample_rate = 1.0e-11

carrier = lambda x: sin(2*pi*f*x)
sat_11 = [-1 if x == False else x for x in create_G2i_code(11)]
prn = lambda x: sat_11[int(x*f_prn)%1023]


signal = load_iq_file('./data/sample.dat')
# complex_data = np.array(load_iq_file('./data/sample-xl.dat'))
# despreaded = load_iq_file('./data/sample-sm.dat')

signal_len = len(signal)
# signal = []
despreaded = []
sine = []
for i in range(10000000):
  t = i*sample_rate
  c = carrier(t)
  sine.append(c)
  despreaded.append(signal[i%signal_len]*prn(t))
  # signal.append(c*prn(t))

f_s, P_s = periodogram(signal, 1/sample_rate, scaling='spectrum')
f_c, P_c = periodogram(sine, 1/sample_rate, scaling='spectrum')
f_d, P_d = periodogram(despreaded, 1/sample_rate, scaling='spectrum')


# rcParams.update({'font.size': 12})

ax = plt.figure(figsize=(15,8))
plt.title("GPS Spreading")
plt.xlabel("Frequency [GHz]")
plt.ylabel(r"Relative Power [$\frac{V^2}{Hz}$]")
ax.axes[0].grid(color='grey', alpha=0.2, linestyle='dashed', linewidth=0.5)

# chart signal and carrier
plt.semilogy(f_s, P_s, '#e31d1d', alpha=0.9, label="Spread GPS signal")
plt.semilogy(f_c, P_c, '#709afa', label="Plain sine wave")
plt.semilogy(f_d, P_d, label="Despreaded signal")
plt.legend(loc=1)

# show 30 MHz on either side of the center frequency
ax.axes[0].set_xlim([(1.57542e9-30e6), (1.57542e9+30e6)])
ax.axes[0].set_ylim([1e-32, 1])
plt.show()

























# def cconv(x, y):
#     """Calculate the circular convolution of 1-D input numpy arrays using DFT
#     From the Signal Processing Library: http://mubeta06.github.io/python/sp/filter.html
#     """
#     return fft.ifft(fft.fft(x)*fft.fft(y))

# def ccorr(x, y):
#     """Calculate the circular correlation of 1-D input numpy arrays using DFT
#     From the Signal Processing Library: http://mubeta06.github.io/python/sp/filter.html
#     """
#     return fft.ifft(fft.fft(x)*fft.fft(y).conj())

# def despread(composite, code, codelength):
#     l = len(composite)/codelength
#     despread = composite*(code*-2.0+1)
#     recovered = []
#     for i in range(round(l)):
#         recovered = np.append(recovered, 1.0*sum(despread[i*codelength:i*codelength+codelength])/codelength)
#     recovered = np.repeat(recovered, codelength)
#     return recovered


# def bitfield(n):
#     """Convert integer into bitfield (as list)
#     From StackOverflow: http://stackoverflow.com/a/10322018/
#     """
#     return [int(digit) for digit in bin(n)[2:]] 


# signal = np.array(load_iq_file('./data/sample.dat'))

# # Two Gold codes. See 
# # Gold, R. "Optimal binary sequences for spread spectrum multiplexing (Corresp.)"
# # IEEE Transactions on Information Theory. (October 1967)
# # g0 = np.array([1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1,
# #        0, 0, 1, 0, 1, 1, 0, 0], dtype=int)
# g0 = np.array([1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], dtype=int)
# # g30 = np.array([0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0,
# #        0, 1, 1, 1, 1, 1, 0, 1])

# # codelength = len(g0) # 2^8 - 1 = 255
# codelength = len(g0) # 2^10 - 1 = 1023

# # # Primary user data
# # p = 0x91
# # p = np.array(bitfield(p))
# # p_len = len(p)
# # p = np.repeat(p, codelength)

# # First secondary user and his code
# # q = 0xc1
# # q = np.array(bitfield(q))
# # q_len = len(q)
# # q = np.repeat(q, codelength)
# q_code = []
# # for i in range(q_len):
#   # q_code = np.append(q_code, g30)
#   # q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)
# q_code = np.append(q_code, g0)


# # q_spread = np.logical_xor(q_code, q).astype(int)

# # # Second secondary user and her code
# # r = 0xa5
# # r = np.array(bitfield(r))
# # r_len = len(r)
# # r = np.repeat(r, codelength)
# # r_code = []
# # for i in range(r_len):
# #   r_code = np.append(r_code, g0)

# # r_spread = np.logical_xor(r_code, r).astype(int)

# # # Composite sigal from all three users
# # composite = (p*2-1) + (r_spread*2-1) + (q_spread*2-1)

# # p_recovered = np.array([], dtype = float)
# # for i in range(p_len):
# #     p_recovered = np.append(p_recovered, 1.0*sum(composite[i*codelength:i*codelength+codelength])/codelength)
# # p_recovered = np.repeat(p_recovered, codelength)

# # r_recovered = despread(composite, r_code, codelength)
# # q_recovered = despread(composite, q_code, codelength)
# q_recovered = despread(signal, q_code, codelength)

# # plt.figure()
# # plt.subplot(3,2,1)
# # # plt.title('Autocorrelation g0')
# # # plt.plot((np.roll(ccorr(g0, g0).real, len(g0)/2-1)), color="green")
# # # plt.xlim(0, len(g0))
# # # plt.ylim(0, 22)
# # # plt.subplot(3,2,2)
# # # plt.title('Autocorrelation g30')
# # # plt.plot((np.roll(ccorr(g30, g30).real, len(g30)/2-1)), color="purple")
# # # plt.xlim(0, len(g30))
# # # plt.ylim(0, 22)
# # # plt.subplot(3,2,3)
# # # plt.title('Crosscorrelation g0 g30')
# # # plt.plot((np.roll(ccorr(g0, g30).real, len(g0)/2-1)))
# # # plt.xlim(0, len(g0))
# # # plt.ylim(0, 22)
# # # plt.subplot(3,2,4)
# # # plt.title('Crosscorrelation g30 g0')
# # # plt.plot((np.roll(ccorr(g30, g0).real, len(g30)/2-1)))
# # # plt.xlim(0, len(g30))
# # # plt.ylim(0, 22)
# # # plt.subplot(3,2,5)
# # # plt.title('g0')
# # # plt.step(range(len(g0)), g0, color="green")
# # # plt.xlim(0, len(g0))
# # # plt.ylim(-0.5, 1.5)
# # # plt.subplot(3,2,6)
# # # plt.title('g30')
# # # plt.step(range(len(g30)), g30, color="purple")
# # # plt.xlim(0, len(g30))
# # # plt.ylim(-0.5, 1.5)
# # # plt.subplots_adjust(hspace=.5)
# # plt.show()



# # f, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(5, sharex=True, sharey=True)
# # ax0.set_title('Signals and codes of 3 users')
# # ax0.step(range(len(p)),p*2-1)
# # ax0.axis((0,len(r),-1.5,1.5))
# # ax1.step(range(len(r)),r*2-1, color="green")
# # ax2.step(range(len(r_code)),r_code*2-1, color="green")
# # ax3.step(range(len(q)),q*2-1, color="purple")
# # ax4.step(range(len(q_code)),q_code*2-1, color="purple")
# # f.subplots_adjust(hspace=0.1)
# # plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
# # plt.show()

# # f, (ax0, ax1, ax2) = plt.subplots(3, sharex=True, sharey=True)
# # ax0.set_title('Composite signal, and composite multiplied by code')
# # ax0.step(range(len(composite)),composite, color="brown")
# # ax0.axis((0,len(r),-4.5,4.5))
# # ax1.step(range(len(composite)),composite*r_code, color="green")
# # ax2.step(range(len(composite)),composite*q_code, color="purple")
# # f.subplots_adjust(hspace=0.1)
# # plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
# # plt.show()


# # g, (ax0, ax1, ax2) = plt.subplots(3, sharex=True, sharey=True)
# # ax0.set_title('Recovered signal of 3 users')
# # ax0.step(range(len(p)),p*2-1, color='gray')
# # ax0.step(range(len(p_recovered)),p_recovered)
# # ax0.axis((0,len(r),-2.5,2.5))
# # ax0.axhline(color="gray", linestyle="dashed")
# # ax1.step(range(len(r)),r*2-1, color='gray')
# # ax1.step(range(len(r_recovered)),r_recovered, color="green")
# # ax1.axhline(color="gray", linestyle="dashed")
# # ax2.step(range(len(q)),q*2-1, color='gray')
# # ax2.step(range(len(q_recovered)),q_recovered, color="purple")
# # ax2.axhline(color="gray", linestyle="dashed")
# # g.subplots_adjust(hspace=0.1)
# # plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
# # plt.show()
