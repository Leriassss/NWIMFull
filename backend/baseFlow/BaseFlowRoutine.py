import pandas as pd
from scipy.optimize import curve_fit

import numpy as np

from backend.contracts.Bundle import DataBaseFlow
class BaseFlowRoutine:
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self):
        self.a,self.b,self.correc_factor = 0, 0, 0
            
    def corr_qbase(self,Q_base_rev, Q_base):            
        correc_factor = self.correction_factor(Q_base_rev, Q_base)
        return correc_factor * Q_base_rev


    def correction_factor_model(self, q_base,a):
        return  a*q_base

    def correction_factor(self, Q_base_rev, Q_base):
        correc_factor, _ = curve_fit(self.correction_factor_model, Q_base_rev, Q_base, p0=[0.01])
        return correc_factor[0]

    @staticmethod
    def modele_baseflow(Q_obs, a, b):
            return a * Q_obs ** b
        
    @staticmethod
    def regBaseFlow(Q_base, Q_obs):
        params_opt, _ = curve_fit(BaseFlowRoutine.modele_baseflow, Q_obs, Q_base, p0=[1, 1], maxfev=10000)
        return params_opt


    def get_qbase_previous(self,data : DataBaseFlow, qbase):
        qobs = data["qObs"] 

        #FITTING DES COEFFICIENTS POUR LA RELATION QBASE-QOBS
        self.a,self.b  = self.regBaseFlow(qbase , qobs)

        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = self.modele_baseflow(data["prevObs"], self.a, self.b)
        
        return q_base_previous
    
    def get_qbase_rev_corr(self, qbase_rev, qbase):
        self.correc_factor = self.correction_factor(qbase_rev, qbase)
        qbase_rev_corr =  self.correc_factor * qbase_rev
        return qbase_rev_corr
