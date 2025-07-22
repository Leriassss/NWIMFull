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
        return pd.Series(np.maximum(0, (prec-smax)*alpha))

    def adapter(self,prec:pd.Series, loss_days, smax):
        non_null_groups = prec.groupby((np.round(prec,2) == 0.0).cumsum())
        sequences = pd.Series([group.values for key, group in non_null_groups])
        r_h = list()
        for element in sequences :
            r_h.append(self.init_loss(element, loss_days, smax))
        return pd.Series(np.concatenate(r_h).tolist()).reindex_like(prec)
    
    def help():
        pass


    
