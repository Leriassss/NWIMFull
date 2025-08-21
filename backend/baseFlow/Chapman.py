from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.contracts.Bundle import DataBaseFlow

import numpy as np
from backend.baseFlow.models.ChapmanModel import ChapmanModel

class Chapman(BaseFlowRoutine, BaseFlow):
    """
    Classe Chapman, héritant de BaseFlowRoutine pour intégrer 
    les fonctions de calibration et validation avec la méthode de Chapman.
    """
    def __init__(self, chapmanModel: ChapmanModel):
        super().__init__()
        self.alpha = chapmanModel.alpha

    def compute(self, flow_series, prev_qbase):
        Q_base = np.zeros_like(flow_series)
        Q_base[0] = prev_qbase
        factor1 = (3 * self.alpha - 1) / (3 - self.alpha)
        factor2 = (1 - self.alpha) / (3 - self.alpha)

        for k in range(1, len(flow_series)):
            Q_base[k] = np.fmax(0,
                factor1 * Q_base[k - 1]
                + factor2 * (flow_series[k] + flow_series[k - 1])
            )

        return Q_base

    def compute2(self, flow_series):
        Q_base = flow_series.copy()
        factor1 = (3 * self.alpha - 1) / (3 - self.alpha)
        factor2 = (1 - self.alpha) / (3 - self.alpha)

        for k in range(1, len(flow_series)):
            Q_base[k] = (
                factor1 * Q_base[k - 1]
                + factor2 * (flow_series[k] + flow_series[k - 1])
            )

        return Q_base

    def reverse_compute(self, previous_qbase, Q_direct):
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0] = previous_qbase

        factor1 = ((3 * self.alpha) - 1) / (3 - self.alpha)
        factor2 = (1 - self.alpha) / (3 - self.alpha)

        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = (1 / (1 - factor2)) * (
                Q_base_rev[k - 1] * (factor1 + factor2)
                + factor2 * (Q_direct[k] + Q_direct[k - 1])
            )

        return Q_base_rev

    def calibration_routine(self,data : DataBaseFlow):
        qbase = self.compute(data["qObs"], data['prevObs'])
        
        qbase_previous = self.get_qbase_previous(data,qbase)

        qbase_rev = self.reverse_compute(qbase_previous, data['qsim'])
        qbase_rev_corr = self.get_qbase_rev_corr(qbase_rev,qbase)
        """
        raise ValueError("len(qbase) : ",len(qbase), " data['qsim'] :", 
                         len(data['qsim']), " qbase_previous :", qbase_previous,
                        " qbase_rev :", len(qbase_rev) , " qbase_rev_corr :", len(qbase_rev_corr))        
        """

        return qbase_rev_corr
    
    def validation_routine(self, data : DataBaseFlow):
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = self.modele_baseflow(data["prevObs"], self.a, self.b)
        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        qbase_rev = self.reverse_compute(q_base_previous, data['qsim'])
        return qbase_rev
    
    def help():
        pass