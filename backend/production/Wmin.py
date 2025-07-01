import numpy as np
import pandas as pd

from backend.production.Production import Production
from backend.production.models.WMinModel import WMinModel


class WMin(Production) :
    def __init__(self, initialLoss : pd.Series, data_model: WMinModel):
        self.data_model = data_model
        self.initial_loss = initialLoss
        
    def compute(self):
        prec = self.initial_loss
        smax = float(self.data_model.S)
        alpha = float(self.data_model.alpha)

        rainfall_ini_loss = self.init_loss(prec, smax, alpha)

        return rainfall_ini_loss
    
    def init_loss(self, prec, smax, alpha):
        valeurs = np.array(prec, dtype=float)  
        pertes_restantes = smax  
        i = 0
        while i < len(valeurs):
            if pertes_restantes > 0:
                if valeurs[i] >= pertes_restantes:
                    valeurs[i] -= pertes_restantes
                    valeurs[i] *= alpha
                else:
                    pertes_restantes -= valeurs[i]
                    valeurs[i] = 0 
            i+=1
        return pd.Series(valeurs)

    def adapter(self,prec:pd.Series, loss_days, smax):
        non_null_groups = prec.groupby((np.round(prec,2) == 0.0).cumsum())
        sequences = pd.Series([group.values for key, group in non_null_groups])
        r_h = list()
        for element in sequences :
            r_h.append(self.init_loss(element, loss_days, smax))
        return pd.Series(np.concatenate(r_h).tolist()).reindex_like(prec)
    
    def help():
        pass


    
