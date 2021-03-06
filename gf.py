from environment import *


class Lead(object):

    def __init__(self, D00, D01, D11):
        self.D00 = D00
        self.D01 = D01
        self.D11 = D11
        self.size = D00.shape[0]
        self.gf = None

    def cal_surface_gf(self, E, order=2, delta=0.000001, epsilon=0.000001):
        I = matrix(eye(self.size))
        if order == 1:
            ws = (E + 1j*delta)*I - self.D00
            wb = (E + 1j*delta)*I - self.D11
        else:
            ws = ((E + 1j*delta)**2)*I - self.D00
            wb = ((E + 1j*delta)**2)*I - self.D11
        tau1 = self.D01
        tau2 = tau1.H
        while abs(tau1).max() > epsilon:
            wb_I = wb.I
            ws = ws - tau1*wb_I*tau2
            wb = wb - tau1*wb_I*tau2 - tau2*wb_I*tau1
            tau1 = tau1*wb_I*tau1
            tau2 = tau2*wb_I*tau2
        self.gf= ws.I


class Coupling(object):

    def __init__(self, lead, position, D_couple):
        self.lead = lead
        self.position = position
        self.D_couple = D_couple
        self.self_energy = None

    def cal_self_engergy(self, E, order=2, delta=0.000001, epsilon=0.000001):
        lead = self.lead
        lead.cal_surface_gf(E, order, delta, epsilon)
        D_couple = self.D_couple
        self.self_energy = D_couple*lead.gf*D_couple.H


class System(object):

    def __init__(self, D, couplings, E, order=2, delta=0.000001, epsilon=0.000001):
        """
        :param D: should be something like {'on_site': [D00, D11, ...], 'couple': [D01, D12, ...]}
        :param leads: should be something like [coupling, ..]
        """
        # store values
        self.D = D
        self.E = E
        self.couplings = couplings
        self.delta = delta
        self.epsilon = epsilon
        self.order = order

        # initializing
        self.length = len(D['on_site'])
        self.self_energy = [0]*self.length
        self.gf = [[None]*self.length for i in range(self.length)]
        self.T = matrix(zeros((len(couplings), len(couplings))))
        self.g = [0]*self.length

        for coupling in couplings:
            coupling.cal_self_engergy(E, order, delta, epsilon)
            self.self_energy[coupling.position] += coupling.self_energy


    def M(self, i, j):
        """
        return M matrices according to indices
        """
        if i == j:
            size = self.D['on_site'][i].shape[0]
            if self.order == 1:
                return (self.E + 1j*self.delta)*matrix(eye(size)) - self.D['on_site'][i] - self.self_energy[i]
            else:
                return (self.E + 1j*self.delta)**2*matrix(eye(size)) - self.D['on_site'][i] - self.self_energy[i]
        if i + 1 == j:
            return -self.D['couple'][i]
        if i == j + 1:
            return -self.D['couple'][j].H

    def cal_diag_gf(self):
        """
        calculate diagonal green's function for center area.
        """
        length = self.length
        g = self.g
        # forward iterating
        g[0] = self.M(0, 0).I
        for j in range(1, length):
            g[j] = (self.M(j, j) -
                    self.M(j, j-1)*g[j-1]*self.M(j-1, j)).I

        G = self.gf
        G[self.length - 1][self.length - 1] = g[self.length - 1]
        # calculate more green's function according to the flag
        # backward iterating
        for j in list(range(self.length - 1))[::-1]:
            G[j][j] = g[j] + g[j]*self.M(j, j+1)*G[j+1][j+1]*self.M(j+1, j)*g[j]

    def cal_gf(self, i, j):
        """
        calculate G_ij for center area
        """
        from operator import mul
        G = self.gf
        if i == j or G[i][j] is not None:
            return None
        if i > j:
            i, j = j, i
        g = self.g
        G[i][j] = reduce(mul, [g[k]*-self.M(k, k+1) for k in range(i, j)], 1)*G[j][j]
        G[j][i] = G[i][j]


    def cal_T(self, i, j):
        """
        calculating transmission probability from lead i to lead j
        """
        ic= self.couplings[i].position
        jc= self.couplings[j].position
        self.cal_gf(ic, jc)
        gamma_i = 1j*(self.couplings[i].self_energy - self.couplings[i].self_energy.H)
        gamma_j = 1j*(self.couplings[j].self_energy - self.couplings[j].self_energy.H)
        self.T[i, j] = trace(gamma_j*self.gf[ic][jc].H*gamma_i*self.gf[ic][jc]).real
        self.T[j, i] = self.T[i, j]
