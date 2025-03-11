import numpy as np
from backend.initialLoss.Loss import Loss
from backend.initialLoss.models.NoLossModel import NoLossModel
from backend.ptq.PTQ import PTQ


class NoLoss(Loss) :
    def __init__(self, ptq : PTQ, data_model: NoLossModel):
        self.data_model = data_model
        self.ptq = ptq
        
    def compute(self):
        rainfall_without_loss = np.maximum(0, self.ptq.p.copy()-self.ptq.etp)
        return rainfall_without_loss
    
    def help():
        pass


    
