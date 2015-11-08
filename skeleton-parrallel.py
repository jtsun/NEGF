from phonon_GF import Phonon
from environment import *
from scoop import futures
from random_line import D
import pickle
from datetime import datetime
N = 100
omega_range =  linspace(0.00000001, 5, N)

start_time = datetime.now()
def cal_T(omega):
    system = Phonon(D, omega)
    system.cal_surface_GF()
    system.cal_self_energy()
    system.cal_GF(flag='all')
    system.cal_T()
    return system.T.real

if __name__ == '__main__':
    data = list(futures.map(cal_T, omega_range))
    file = open('data.dat','wb')
    pickle.dump(data, file)
    file.close()
    print(datetime.now() - start_time)

