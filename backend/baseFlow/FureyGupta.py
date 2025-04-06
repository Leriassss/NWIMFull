from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataBaseFlow
from backend.baseFlow.models.FureyGuptaModel import FureyGuptaModel
from backend.ptq.PTQ import PTQ
import numpy as np
import pandas as pd

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from permetrics.regression import RegressionMetric

class FureyGupta(BaseFlow):
    """
    Classe pour implémenter la méthode de récession Furey-Gupta.
    """
    def __init__(self,ptq : PTQ, fureyGuptaModel : FureyGuptaModel):
        self.flow_series = ptq.q
        self.gamma = fureyGuptaModel.gamma
        self.cs_over_c = fureyGuptaModel.cs_over_c
        self.hun_base_flow = []
        self.q = ptq.q

    def compute(self, datas_base_flow : DataBaseFlow):
        """
        Implémente le filtre basé sur les paramètres physiques selon la méthode de Furey-Gupta.
        
        Args:
            flow_series : Série temporelle des débits [mm/jour]
            gamma  : Coefficient lié au retard des eaux souterraines
            cs_over_c (float) : Ratio des coefficients (par défaut 1.1)
            
        Returns:
            np.array : Série des débits de base (Qk).
        """
        
        pl = datas_base_flow["pl"]
        Q_base = self.flow_series.copy()
        for k in range(3, len(self.flow_series)):
            Q_base[k] =np.maximum(0, 
                                  (1 - self.gamma) * Q_base[k - 1] + self.gamma * (self.cs_over_c) * (self.flow_series[k - 3] - Q_base[k - 3])
                                  ) 
        return Q_base
    
    def hunBaseFlow(self, rain_lost : pd.Series, Q_base, Q):
        self.hun_base_flow = Q_base/rain_lost.sum()
        time_base = 5
        
        seq_hun = np.arange(0,len(rain_lost),time_base)
        hun_time_base = []        
        for k in seq_hun:
            production_seq = rain_lost[k:k+time_base]
            hun_seq = self.hun_base_flow[k:k+time_base]
            hun_time_base.append(pd.Series(np.convolve(production_seq,hun_seq))[:time_base])
        q_base_cal =  pd.concat(hun_time_base).reset_index(drop=True)[:len(rain_lost)]

        print(" NASHEUUU ----------------")
        print(rain_lost)
        plt.plot(np.array(Q)) 
        plt.plot(np.array(q_base_cal))

        evaluator_qbase = RegressionMetric(np.array(Q_base),np.array(q_base_cal))
        print(evaluator_qbase.NSE(multi_output="raw_values"))


    def baseflow_reservoir(Sb, Ib, k):
        Qb = k * Sb
        Sb_next = Sb + Ib - Qb
        return Qb, Sb_next

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

    
        
