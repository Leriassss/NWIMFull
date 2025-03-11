import numpy as np
import pandas as pd

from backend.initialLoss.Loss import Loss
from backend.initialLoss.models.PLossModel import PLossModel
from backend.ptq.PTQ import PTQ


class PLoss(Loss) :
    def __init__(self, ptq : PTQ, data_model: PLossModel):
        self.data_model = data_model
        self.ptq = ptq
        
    def compute(self):
        p = self.data_model.p
        rainfall_without_loss = self.p_loss(self.ptq.p.copy(),self.ptq.etp, p)
        return rainfall_without_loss
    
    def p_loss(self,rain,etp, p):
        return np.maximum(0, (1-p)*rain - etp)
    
    def help():
        pass
