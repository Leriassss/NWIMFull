
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from permetrics.regression import RegressionMetric
class Model : 
    Metrics = ["NSE", "KGE", "RMSE", "MAE", "MAPE", "R2"]
    def __init__(self,dates_calibration, dates_validation,
                 rain_calibration, rain_validation, pet_calage, pet_validation,  q_obs_calage, q_obs_validation):
        qbase_default = self.chapman(q_obs_calage)
        self.q_obs_means_calibration = self.daily_qobs_mean(dates_calibration,q_obs_calage)
        self.qdirect_means = np.maximum(0, self.q_obs_means_calibration  - self.chapman(self.q_obs_means_calibration))

        direct_flow_default = pd.Series(np.maximum(0, q_obs_calage-qbase_default))
        direct_sim = direct_flow_default.where(rain_calibration != 0).dropna()
        baseflow_sim = qbase_default.where(rain_calibration != 0).dropna()

        # ----------- INITIALISATION ---------------------
        self.dates_calibration = dates_calibration
        self.dates_validation = dates_validation
        self.recession_factors = Model.regBaseFlow(baseflow_sim,direct_sim)  
        self.rain_calibration = rain_calibration
        self.rain_validation = rain_validation
        self.pet_calage = pet_calage
        self.pet_validation = pet_validation
        self.q_obs_calage = q_obs_calage
        self.q_obs_validation = q_obs_validation
        self.qsim_calibration = None
        self.qsim_validation = None

    def compute_w_min_loss(self, prec, smax, w):
        """
        prec : la pluie brute
        smax : la quantité de perte initiale
        w : le coefficient de ruissellement
        """
        valeurs = np.array(prec, dtype=float)  
        pertes_restantes = smax  
        i = 0
        while i < len(valeurs):
            if pertes_restantes > 0:
                if valeurs[i] >= pertes_restantes:
                    valeurs[i] -= pertes_restantes
                    valeurs[i] *= w
                else:
                    pertes_restantes -= valeurs[i]
                    valeurs[i] = 0 
            i+=1
        return pd.Series(valeurs)
    
    def compute_etp_loss(self,production, etp, etp_adj = 1):
        """
        Estimation de la pluie nette par retrait de l'etp

        production : la pluie nette
        etp : l'etp
        etp_adj : un coefficient d'ajustement (par défaut 1)
        """
        return np.maximum(0, production - etp_adj *etp)
    
    def compute_hun(self, pn, q_direct,time_base):
        """
        Estimation du débit ruissellé direct par la méthode de l'HUN

        Paramètres :
        - pn : La pluie nette
        - q_direct : le débit de ruissellement direct moyen

        Retourne :
        - Serie de débit direct 
        """
        transformed_production = pd.Series(np.where(np.round(pn, 0) == 0, 1, pn))
        initial_production = pn
        seq_hun = np.arange(0,len(q_direct),time_base)
        hun_time_base = []
        interm_hun = []
        xtra_flow = np.zeros(time_base-1)
        for k in seq_hun:
            initial_production_seq = initial_production[k:k+time_base]
            len_ips = len(initial_production_seq)
            transformed_production_seq = transformed_production[k:k+time_base]
            q_direct_seq = q_direct[k:k+time_base]
            hun_k = q_direct_seq/(transformed_production_seq.sum())
            interm_hun.append(pd.Series(hun_k))
            total_sim = np.convolve(initial_production_seq,hun_k)
            sim_flow = total_sim[:len_ips]    
            sim_flow[:len(xtra_flow)] += xtra_flow[:len(sim_flow)]
            xtra_flow = total_sim[len_ips:]
            hun_time_base.append(pd.Series(sim_flow))
        q_sim_direct =  pd.concat(hun_time_base).reset_index(drop=True)[:len(initial_production)]
        return q_sim_direct
    
    def compute_exponential_recession(self, k, qsim : pd.Series, p: pd.Series, prevQObs : float) :
        """
        Estimation du débit de base par décroissance exponentielle.
        
        Paramètres :
        - k : taux de décroissance
        - qsim : débit direct simulé
        - p : pluie brute
        - prevQObs : débit moyen total du jour avant le début de la série de simulation
        
        Retourne :
        - Serie de débit de base estimé
        """
        a = self.recession_factors[0]
        b = self.recession_factors[1]
        # Étape 1 : considérer les périodes sans pluie
        debit_modifie = qsim.where(p != 0)
        
        # Étape 2 : appliquer la loi a * Q^b quand c’est défini
        debit_modifie = debit_modifie.apply(lambda q: a * q**b if pd.notna(q) else np.nan)
        
        # Étape 3 : appliquer la décroissance exponentielle aux périodes manquantes
        debit_base = debit_modifie.copy()
        debit_base.iloc[0] = prevQObs  # initialisation
        
        i = 1
        while i < len(debit_base):
            if pd.isna(debit_base.iloc[i]):
                q0 = debit_base.iloc[i - 1] if i == 1 else debit_base.iloc[i - 1] + qsim.iloc[i-1]
                t = 1
                j = i
                while j < len(debit_base) and pd.isna(debit_base.iloc[j]):
                    debit_base.iloc[j] = q0 * np.exp(-k * t)

                    t += 1
                    j += 1
                i = j
            else:
                i += 1
        debit_base = debit_base.rolling(window=10, center=True, min_periods=1).mean()
        return debit_base

    def calibration(self, smax, w, etp_adj, time_base, k):
        production = self.compute_w_min_loss(self.rain_calibration, smax, w)
        net_rainfall = self.compute_etp_loss(production, self.pet_calage, etp_adj)
        qdirect_means =  self.expand_flow(self.dates_calibration, self.qdirect_means)
        prevObs = self.get_prev_q_obs(self.dates_calibration, self.q_obs_calage)
        qsim_direct = self.compute_hun(net_rainfall, qdirect_means, time_base)
        qbase = self.compute_exponential_recession(k, qsim_direct, self.rain_calibration, prevObs)
        self.qsim_calibration = (qsim_direct + qbase)
        
        return self.qsim_calibration

    def validation(self, smax, w, etp_adj, time_base, k):
        production = self.compute_w_min_loss(self.rain_validation, smax, w)
        net_rainfall = self.compute_etp_loss(production, self.pet_validation, etp_adj)
        qdirect_means =  self.expand_flow(self.dates_validation, self.qdirect_means)
        prevObs = self.get_prev_q_obs(self.dates_validation, self.q_obs_validation)
        qsim_direct = self.compute_hun(net_rainfall, qdirect_means, time_base)
        qbase = self.compute_exponential_recession(k, qsim_direct, self.rain_validation, prevObs)
        self.qsim_validation = (qsim_direct + qbase).fillna(0)
        return self.qsim_validation

    def performance(self, obs, sim):
        evaluator = RegressionMetric(np.array(obs), np.array(sim))
        return evaluator.get_metrics_by_list_names(self.Metrics)
    
    def calibration_graphic(self):
        plt.plot(self.qsim_calibration, "r")
        plt.plot(self.q_obs_calage, "b")

    def validation_graphic(self):
        plt.plot(self.qsim_validation, "r")
        plt.plot(self.q_obs_validation, "b")

    @staticmethod
    def modele_baseflow(Q_obs, a, b):
            return a * Q_obs ** b
        
    @staticmethod
    def regBaseFlow(Q_base, Q_obs):
        params_opt, _ = curve_fit(Model.modele_baseflow, Q_obs, Q_base, p0=[1, 1], maxfev=10000)
        return params_opt
    

    def chapman(self, flow_series : pd.Series, alpha = 0.925):
        """
        Methode de séparation des ecoulements par la méthode du filtre de Chapman 

        flow_series : Le débit total
        alpha : Le coefficient de recession de chapman (0.925 par défaut)
        """
        Q_base = flow_series.copy()
        factor1 = (3 * alpha - 1) / (3 - alpha)
        factor2 = (1 - alpha) / (3 - alpha)

        for k in range(1, len(flow_series)):
            Q_base[k] = (
                factor1 * Q_base[k - 1]
                + factor2 * (flow_series[k] + flow_series[k - 1])
            )

        return Q_base
    

    def get_prev_q_obs(self, dates : pd.Series, q_obs: pd.Series):
        date = pd.to_datetime(dates.iloc[0])
        prev_day = date - pd.Timedelta(days=1)
        jour_annee = prev_day.dayofyear
        prev_qobs = self.daily_qobs_mean(dates, q_obs)[jour_annee-1]
        return prev_qobs
    
    def daily_qobs_mean(self, dates, q_obs):
        df = pd.DataFrame({
            "Date": pd.to_datetime(dates),
            "Q_obs": q_obs
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
    
    def expand_flow(self, dates, qdirect_means):
        df = pd.DataFrame({
            "Date": pd.to_datetime(dates),
        })
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day


        daily_avg = pd.DataFrame({
            "Date" : pd.date_range(start="2020-01-01", end="2020-12-31"),
            "Qdirect" : qdirect_means
        })

        daily_avg["month"] = daily_avg["Date"].dt.month
        daily_avg["day"] = daily_avg["Date"].dt.day

        # Merge pour garantir 366 jours dans le résultat
        merged = df.merge(daily_avg, on=["month", "day"])

        return merged["Qdirect"]
    
    def laminage(self, o_l, a, index):
        c = a.copy()
        excess = a[index] - o_l
        c[index] = o_l
        i = index
        while excess > 0 and i < len(c):
            a = c[i]
            c[i] = np.minimum(o_l, a + excess)
            excess = a + excess - o_l
            i += 1
        return c
    
    def compute_laminage(self, output_limit, qsim):
        limit_reach = True
        c = qsim
        while limit_reach :
            indexes = np.where(c > output_limit)[0]
            if len(indexes) > 0 :
                index = indexes[0]
                c = self.laminage(output_limit, c, index)
            else :
                limit_reach = False
        return c
    
    def compute_lissage(self, qsim, window):
        return pd.Series(qsim).rolling(window=window, center=True, min_periods=1).mean() 
    
    def filter(self, qsim, output_lim, window):
        qsim_laminage = self.compute_laminage(output_lim, qsim)
        qsim_lissage = self.compute_lissage(qsim_laminage, window)
        return qsim_lissage