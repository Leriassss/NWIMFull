import numpy as np
import pandas as pd

from backend.initialLoss.Loss import Loss
from backend.initialLoss.models.EToLossModel import EToLossModel
from backend.ptq.PTQ import PTQ


class EToLoss(Loss) :
    def __init__(self, ptq : PTQ, data_model: EToLossModel):
        self.data_model = data_model
        self.ptq = ptq
        
    def compute(self):
        prec = self.ptq.p.copy()
        alpha = self.data_model.alpha
        rainfall_without_loss = self.etp_loss(prec,self.ptq.etp, alpha)
        return rainfall_without_loss
    
    
    def etp_loss(self,rain,etp, alpha):
        return np.maximum(0, rain - alpha*etp)
    
    def help():
        pass


    
