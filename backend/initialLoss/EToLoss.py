import numpy as np
import pandas as pd

from backend.contracts.Bundle import DataInitialLoss
from backend.initialLoss.Loss import Loss
from backend.initialLoss.models.EToLossModel import EToLossModel


class EToLoss(Loss) :
    def __init__(self, ia_bundle : DataInitialLoss, data_model: EToLossModel):
        self.data_model = data_model
        self.ia_bundle = ia_bundle
        
    def compute(self):
        prec = self.ia_bundle['net_rainfall']
        alpha = self.data_model.alpha
        rainfall_without_loss = self.etp_loss(prec,self.ia_bundle['etp'], alpha)
        return rainfall_without_loss
    
    
    def etp_loss(self,rain,etp, alpha):
        return np.maximum(0, rain - alpha*etp)
    
    def help():
        pass


    
