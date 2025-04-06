from backend.ptq.PTQ import PTQ

from scipy.optimize import curve_fit

import numpy as np
class BaseFlowRoutine:
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self, ptq : PTQ ):
        self.correc_factor = 0
        self.a, self.b = 0, 0
        self.ptq = ptq


    @staticmethod
    def help():
        """
        Fournit une description des méthodes disponibles dans la classe Recession.
        """
        description = """
        Implémente le filtre de récession de Furey-Gupta.


        Arguments pour `furey_gupta`:
        - flow_series : Série temporelle des débits [mm/jour] (pd.Series ou np.ndarray).
        - gamma : Coefficient de récession (par défaut 0.03).
        - cs_over_c : Ratio des coefficients (par défaut 1.1).
        """
        print(description)
    

    def corr_qbase(self,Q_base_rev, Q_base):            
        correc_factor = self.correction_factor(Q_base_rev, Q_base)
        return correc_factor * Q_base_rev


    def correction_factor_model(self, q_base,a):
        return a * q_base

    def correction_factor(self, Q_base_rev, Q_base):
        correc_factor, _ = curve_fit(self.correction_factor_model, Q_base_rev, Q_base, p0=[0.01])
        return correc_factor

    def modele_baseflow(self, Q_obs, a, b):
            return a * Q_obs ** b
        
    def regBaseFlow(self,Q_base, Q_obs):
        params_opt, _ = curve_fit(self.modele_baseflow, Q_obs, Q_base, p0=[1, 1], maxfev=10000)
        return params_opt

