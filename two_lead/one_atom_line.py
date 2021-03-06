##
from environment import *
from two_lead.phonon_GF import Phonon
f = 1.0
omega = 1.5
D00 = matrix([2*f])
D11 = matrix([2*f])
D22 = matrix([2*f])
D33 = matrix([2*f])
D44 = matrix([2*f])
D55 = matrix([2*f])
D66 = matrix([2*f])
D77 = matrix([2*f])
Dl00 = matrix([2*f])
Dl01 = matrix([-f])
Dl11 = matrix([2*f])
Dr00 = matrix([2*f])
Dr01 = matrix([-f])
Dr11 = matrix([2*f])
D01 = matrix([-f])
D12 = matrix([-f])
D23 = matrix([-f])
D34 = matrix([-f])
D45 = matrix([-f])
D56 = matrix([-f])
D67 = matrix([-f])
Dlcl = matrix([-f])
Dlcr = matrix([-f])
D = {'on_site': [D00, D11, D22, D33, D44, D55, D66, D77], 'lead':{'l': [Dl00, Dl01, Dl11], 'r': [Dr00, Dr01, Dr11]},
     'couple': [D01, D12, D23, D34, D45, D56, D67], 'lead_center':{'l': Dlcl, 'r': Dlcr}}
system = Phonon(D, omega)
system.cal_surface_GF()
system.cal_self_energy()
system.cal_GF(flag='all')
system.cal_T()
print(system.T)
print('------------------')
print(system.GF['center'][0])
print('------------------')
print(system.GF['center'][7])
##