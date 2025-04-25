import numpy as np
import pandas as pd

from backend.production.Production import Production
from backend.production.models.WMinModel import WMinModel
from backend.ptq.PTQ import PTQ


class WMin(Production) :
    def __init__(self, ptq : PTQ, data_model: WMinModel):
        self.data_model = data_model
        self.ptq = ptq
        
    def compute(self):
        prec = self.ptq.p.copy()
        smax = float(self.data_model.S)
        alpha = float(self.data_model.alpha)
        loss_days = int(self.data_model.loss_days)

        rainfall_ini_loss = self.adapter(prec,loss_days, smax)

        rainfall_without_loss = self.w_runoff(rainfall_ini_loss,self.ptq.p.copy(), alpha)
        return rainfall_without_loss
    
    def init_loss(self, prec,loss_days, smax):
        valeurs = np.array(prec, dtype=float)  
        pertes_restantes = smax  
        seq = np.arange(loss_days) if len(valeurs) >= loss_days else np.arange(len(valeurs))
        for i in seq:
            if pertes_restantes > 0:
                if valeurs[i] >= pertes_restantes:
                    valeurs[i] -= pertes_restantes
                else:
                    pertes_restantes -= valeurs[i]
                    valeurs[i] = 0 
        return pd.Series(valeurs)
    
    def w_runoff(self,rain,etp, alpha):
        return np.maximum(0, rain - alpha*etp)


    def adapter(self,prec:pd.Series, loss_days, smax):
        non_null_groups = prec.groupby((np.round(prec,2) == 0.0).cumsum())
        sequences = pd.Series([group.values for key, group in non_null_groups])
        r_h = list()
        for element in sequences :
            r_h.append(self.init_loss(element, loss_days, smax))
        return pd.Series(np.concatenate(r_h).tolist()).reindex_like(prec)
    
    def help():
        pass


    
