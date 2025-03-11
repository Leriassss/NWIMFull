# -*- coding: utf-8 -*-

import numpy as np

class Criteria:
    def nse(self,obs, sim):
        """
        Calcule le Nash-Sutcliffe Efficiency (NSE).
        
        Parameters:
            obs (array-like): Valeurs observées.
            sim (array-like): Valeurs simulées.
        
        Returns:
            float: Valeur NSE.
        """
        obs = np.array(obs)
        sim = np.array(sim)
        
        numerator = np.sum((obs - sim)**2)
        denominator = np.sum((obs - np.mean(obs))**2)
        
        return 1 - (numerator / denominator)


    def kge(self,obs, sim):
        """
        Calcule le Kling-Gupta Efficiency (KGE).
        
        Parameters:
            obs (array-like): Valeurs observées.
            sim (array-like): Valeurs simulées.
        
        Returns:
            float: Valeur KGE.
        """
        obs = np.array(obs)
        sim = np.array(sim)
        
        # Moyennes
        mean_obs = np.mean(obs)
        mean_sim = np.mean(sim)
        
        # Coefficient de corrélation
        r = np.corrcoef(obs, sim)[0, 1]
        
        # Ratio de biais (bêta)
        beta = mean_sim / mean_obs
        
        # Ratio de variabilité (alpha)
        alpha = (np.std(sim) / np.std(obs))
        
        # KGE
        kge_value = 1 - np.sqrt((r - 1)**2 + (beta - 1)**2 + (alpha - 1)**2)
        
        return kge_value

    def methods(self):
        return  {
            "nse": self.nse,
            "kge": self.kge,
        }
        

