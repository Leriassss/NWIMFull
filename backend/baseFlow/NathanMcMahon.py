from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.contracts.Bundle import DataBaseFlow

import numpy as np
from backend.baseFlow.models.NathanMcMahonModel import NathanMcMahonModel

class NathanMcMahon(BaseFlowRoutine, BaseFlow):
    """
    Classe Chapman, héritant de BaseFlowRoutine pour intégrer 
    les fonctions de calibration et validation avec la méthode de Chapman.
    """
    def __init__(self, nathanMcMahonModel: NathanMcMahonModel):
        super().__init__()
        self.k = nathanMcMahonModel.k

    def compute(self, flow_series):
        Q_base = np.zeros_like(flow_series)
        for k in range(1, len(flow_series)):
            Q_base[k] = self.k*Q_base[k-1] + (1-self.k)*(flow_series[k]-flow_series[k-1])/2
        return Q_base


    def reverse_compute(self, previous_qbase, Q_direct):
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0] = previous_qbase

        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = (1-self.k)*(Q_direct[k-1])/(1+self.k) + Q_base_rev[k-1]

        return Q_base_rev

    def calibration_routine(self,data : DataBaseFlow):
        qbase = self.compute(data["qObs"])
        qbase_previous = self.get_qbase_previous(data,qbase)
        qbase_rev = self.reverse_compute(qbase_previous, data['qsim'])
        
        qbase_rev_corr = self.get_qbase_rev_corr(qbase_rev,qbase)
        return qbase_rev_corr
    
    def validation_routine(self, data : DataBaseFlow):
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = self.modele_baseflow(data["prevObs"], self.a, self.b)
        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        qbase_rev = self.reverse_compute(q_base_previous, data['qsim'])
        return qbase_rev
    
    def help():
        pass