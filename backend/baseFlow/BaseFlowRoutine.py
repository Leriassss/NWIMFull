import pandas as pd
from scipy.optimize import curve_fit

import numpy as np

from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataBaseFlow
class BaseFlowRoutine:
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self, baseflowModel : BaseFlow):
        self.baseflowModel = baseflowModel
        self.a,self.b,self.correc_factor = 0, 0, 0
        self.hun = []

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
        
    def calibration_routine(self,data : DataBaseFlow):
        dates = data['ptq'].dates
        qobs = data['ptq'].q

        prev_day = self.get_qobs_mean(dates[0])

        #FITTING DES COEFFICIENTS POUR LA RELATION QBASE-QOBS
        self.a,self.b  = self.regBaseFlow(data['qbase'] , qobs)
        #DETERMINATION DU DEBIT MOYEN JOURNALIER CORRESPONDANT
        print("--------- BFR -----------")
        print(prev_day-1)
        print(data)
        q_obs_mean = data["qmean"][prev_day-1]
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = self.modele_baseflow(q_obs_mean, self.a, self.b)

        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        qbase_rev = self.baseflowModel.reverse_compute(q_base_previous, data['qsim'])
        
        # CALCUL DU FACTEUR DE CORRECTION
        self.correc_factor = self.correction_factor(qbase_rev, data['qbase'])
        qbase_rev_corr =  self.correc_factor * qbase_rev
        return qbase_rev_corr
    
    def validation_routine(self, data : DataBaseFlow):
        dates = data['ptq'].dates

        prev_day = self.get_qobs_mean(dates[0])
        
        #DETERMINATION DU DEBIT MOYEN JOURNALIER CORRESPONDANT
        q_obs_mean = data["qmean"][prev_day-1]
        
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = self.modele_baseflow(q_obs_mean, self.a, self.b)
        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        
        qbase_rev = self.baseflowModel.reverse_compute(q_base_previous, data['qsim'])

        
        qbase_rev_corr =  self.correc_factor * qbase_rev

        return qbase_rev_corr
    
    
    def corr_qbase(self,Q_base_rev, Q_base):            
        correc_factor = self.correction_factor(Q_base_rev, Q_base)
        return correc_factor * Q_base_rev


    def correction_factor_model(self, q_base,a):
        return  a*q_base

    def correction_factor(self, Q_base_rev, Q_base):
        correc_factor, _ = curve_fit(self.correction_factor_model, Q_base_rev, Q_base, p0=[0.01])
        return correc_factor[0]

    def modele_baseflow(self, Q_obs, a, b):
            return a * Q_obs ** b
        
    def regBaseFlow(self,Q_base, Q_obs):
        params_opt, _ = curve_fit(self.modele_baseflow, Q_obs, Q_base, p0=[1, 1], maxfev=10000)
        return params_opt

    def daily_qobs_mean(self, dates, Q_obs):
        df = pd.DataFrame({
                    "Date": pd.to_datetime(dates),
                    "Q_obs": Q_obs
        })
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day

        
        daily_avg = df.groupby(["month", "day"])[["Q_obs"]].mean().reset_index()

        full_days = pd.date_range(start="2020-01-01", end="2020-12-31")
        full_days_df = pd.DataFrame({
            "month": full_days.month,
            "day": full_days.day
        })

        # Merge pour garantir 366 jours dans le résultat
        merged = full_days_df.merge(daily_avg, on=["month", "day"], how="left")
        idx_29_feb = merged[(merged["month"] == 2) & (merged["day"] == 29)].index

        if not idx_29_feb.empty:
            idx = idx_29_feb[0]
            # On récupère les valeurs du 28 février et du 1er mars
            val_before = merged.loc[idx - 1, "Q_obs"]
            val_after = merged.loc[idx + 1, "Q_obs"]
            # On remplace le NaN du 29 février par leur moyenne
            merged.loc[idx, "Q_obs"] = np.nanmean([val_before, val_after])
        
        return merged["Q_obs"]
    

    def get_qobs_mean(self, date_str):
        date = pd.to_datetime(date_str)

        prev_day = date - pd.Timedelta(days=1)

        jour_annee = prev_day.dayofyear
        return jour_annee
