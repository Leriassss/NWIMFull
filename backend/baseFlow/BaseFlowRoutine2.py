import pandas as pd
from scipy.optimize import curve_fit

import numpy as np

from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataBaseFlow
class BaseFlowRoutine2:
    """
    Classe pour implémenter la méthode de récession Chapman.
    """
    def __init__(self, baseflowModel : BaseFlow):
        self.baseflowModel = baseflowModel
        self.a,self.b,self.c,self.d,self.correc_factor = 0, 0, 0, 0, 0
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
        qobs = data['ptq'].q

        #FITTING DES COEFFICIENTS POUR LA RELATION QR-QOBS
        self.c,self.d  = self.regDirectFlow(qobs, data['qsim'])

        qobs_estimated = self.modele_baseflow(data['qsim'], self.c, self.d)

        #FITTING DES COEFFICIENTS POUR LA RELATION QBASE-QOBS
        self.a,self.b  = self.regBaseFlow(data['qbase'] , qobs_estimated)

        qbase_estimated = self.modele_baseflow(qobs_estimated, self.a, self.b)

        self.correc_factor = self.correction_factor(qbase_estimated, data['qbase'])

        return self.correc_factor * qbase_estimated
    
    def validation_routine(self, data : DataBaseFlow):
        qobs_estimated = self.modele_baseflow(data['qsim'], self.c, self.d)

        qbase_estimated = self.modele_baseflow(qobs_estimated, self.a, self.b)

        return self.correc_factor * qbase_estimated
    
    
    def corr_qbase(self,Q_base_rev, Q_base):            
        correc_factor = self.correction_factor(Q_base_rev, Q_base)
        return correc_factor * Q_base_rev


    def correction_factor_model(self, q_base,a):
        return  a*q_base

    def correction_factor(self, Q_base_rev, Q_base):
        correc_factor, _ = curve_fit(self.correction_factor_model, Q_base_rev, Q_base, p0=[0.01])
        return correc_factor[0]

    def modele_baseflow(self, Q, a, b):
            return a * Q ** b
        
    def regBaseFlow(self,Q_base, Q_obs):
        params_opt, _ = curve_fit(self.modele_baseflow, Q_obs, Q_base, p0=[1, 1], maxfev=10000)
        return params_opt

    def regDirectFlow(self, Q_obs, Qr):
        params_opt, _ = curve_fit(self.modele_baseflow, Qr, Q_obs, p0=[1, 1], maxfev=10000)
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
