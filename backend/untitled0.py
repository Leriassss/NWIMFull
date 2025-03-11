# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 12:11:07 2025

@author: HP
"""

#-------------------------------------------------------------
from factory.ProductionFactory import ProductionFactory
from factory.RecessionFactory import RecessionFactory
from factory.RoutingFactory import Factory
from criteria.Criteria import Criteria

sim_dpft = Simulation("Wmin", "FureyGupta", "DPFT")
best_run_dpft, best_sim_dpft = sim_dpft.automatic_calibration(ptq__calage_dats,
                                                  ptq_validation_dats,
                                                  calibration_bundle_dpft,
                                                  2, "nse")

validation_pars = best_run_dpft["parameters"].reset_index(level='Parameter', drop=True).groupby("Category").apply(list).to_dict()

nse_validation_dpft, q_sim_validation_dpft = sim_dpft.validation()
nse_validation_hun, q_sim_validation_hun = sim_hun.validation()

validation_pars = best_run_hun["parameters"].reset_index(level='Parameter', drop=True).groupby("Category").apply(list).to_dict()

pn = ProductionFactory.createInstance("Wmin",ptq__calage_dats, 0.1235442).compute()
qbase = RecessionFactory.createInstance("FureyGupta", ptq__calage_dats, 0.07107444,1.95121197).compute()

hun = []

production = np.maximum(0, pn - ptq__calage_dats.etp)
time_base = 13
q_direct = np.maximum(0,ptq__calage_dats.q - qbase)
seq_hun = np.arange(0,q_direct.count(),time_base)
hun_time_base = []
for k in seq_hun:
    production_seq = production[k:k+time_base]
    q_direct_seq = q_direct[k:k+time_base]
    if production_seq.sum()>0:
        hun_k = q_direct_seq/(production_seq.sum())
    else:
        hun_k = np.zeros_like(q_direct_seq)
    hun.append(pd.Series(hun_k))
    hun_time_base.append(pd.Series(np.convolve(production_seq,hun_k))[:len(production_seq)])
hun = pd.concat(hun).reset_index(drop=True)
q_sim_direct =  pd.concat(hun_time_base).reset_index(drop=True)[:len(production)] + qbase

Criteria.nse(Criteria, ptq__calage_dats.q, q_sim_direct)
plt.plot(ptq__calage_dats.q)
plt.plot(q_sim_direct)

hun_ = hun.copy()
pn = ProductionFactory.createInstance("Wmin",ptq_validation_dats, 0.1235442).compute()
qbase = RecessionFactory.createInstance("FureyGupta", ptq_validation_dats , 0.07107444,1.95121197).compute()

production = np.maximum(0, pn - ptq_validation_dats.etp)
time_base = 13
seq_hun = np.arange(0,len(production),time_base)
hun_time_base = []        
for k in seq_hun:
    production_seq = production[k:k+time_base]
    hun_seq = hun_[k:k+time_base]
    hun_time_base.append(pd.Series(np.convolve(production_seq,hun_seq))[:time_base])
q_sim_direct_val =  pd.concat(hun_time_base).reset_index(drop=True)[:len(production)].add(qbase)

Criteria().nse(ptq_validation_dats.q, q_sim_direct_val)
Criteria.nse(Criteria, ptq_validation_dats.q, q_sim_direct_val)
plt.plot(ptq_validation_dats.q)
plt.plot(q_sim_direct)

np.convolve(production[8:16],hun_[8:16])



import numpy as np
from factory.RecessionFactory import RecessionFactory
from ptq.PTQ import PTQ

from routing.Routing import Routing
from routing.models.PLAModel import PLAModel

class PLA(Routing):
    def __init__(self,methods, ptq_calage: PTQ,ptq_validation : PTQ, kwargs):
        self.kwargs = kwargs
        self.indexes = list(kwargs.keys())
        self.methods = methods
        self.ptq_calage = ptq_calage
        self.ptq_validation = ptq_validation


    def calage(self):
        production = np.maximum(0, self.ptq_calage.p - self.ptq_calage.etp)
        q_base = RecessionFactory.createInstance(self.methods["recession"],self.ptq_calage,*self.kwargs[self.indexes[0]]).compute()
        return self.sim(production,q_base)
    
    def validation(self):
        production = np.maximum(0, self.ptq_validation.p - self.ptq_validation.etp)
        q_base = RecessionFactory.createInstance(self.methods["recession"],self.ptq_validation,*self.kwargs[self.indexes[0]]).compute()
        return self.sim(production,q_base)
        
    def sim(self,q,q_base):
        indexes = list(self.kwargs.keys())
        plaModel = PLAModel(*self.kwargs[indexes[1]])
        mu= plaModel.mu
        landa = plaModel.landa
        t_x = plaModel.t_x 
        s_f = plaModel.s_f
        
        n = len(q)
        x = np.zeros(n)
        for i in range(3, n):
            if q[i] == 0:
                x[i] = x[i - 1] - (mu/landa) * x[i - 1]
            else:
                x[i] = x[i - 1] + (mu/landa) * (q[i] ** (2 * mu- 1))
        
        q_sim = np.zeros(n)
        for i in range(2, n):
            if x[i] * s_f > t_x:
                q_sim[i] = max(0, q_sim[i - 1] - (mu/landa) * (q_sim[i - 1] ** (2 * mu- 1)) + s_f * x[i] * q[i - 1] /landa)
            else:
                q_sim[i] =max(0,q_sim[i - 1] - (mu/landa) * (q_sim[i - 1] ** (2 * mu- 1))) 
        return q_sim + q_base
    
    @staticmethod
    def help():
        """
        Affiche l'aide pour l'utilisation de la classe PLA.

        Returns
        -------
        None
        """
        print(
            """
            Classe PLA : Simulation des débits par le Principe de Moindre Action (PLA).

            Méthodes :
            ----------
            - __init__(production) : Initialise l'objet PLA avec la série de production.
            - hydrogramm(MU, LANDA, TX, SF, P, ETP) : Calcule le débit simulé à partir des paramètres et des séries d'entrée.
            - help() : Affiche cette aide.

            Paramètres des méthodes :
            -------------------------
            - MU : Coefficient d'humidité spécifique.
            - LANDA : Coefficient de transfert des flux.
            - TX : Valeur seuil pour le débit.
            - SF : Facteur de redistribution.
            - P : Série des précipitations [mm/j].
            - ETP : Série de l'évapotranspiration potentielle [mm/j].
            """
        )
            

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim_nash,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation_nash,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_validation_nash.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(best_run_nash["nse"].round(2)))
plt.legend(["QObs","QSim Calage","QObs","QSim Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')