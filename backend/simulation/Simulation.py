from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataInitialLoss, DataSimulation, RoutingData, DataBaseFlow
from backend.factory.RoutingFactory import RoutingFactory
from backend.factory.InitialLossFactory import InitialLossFactory
from backend.factory.ProductionFactory import ProductionFactory
from backend.factory.RecessionFactory import RecessionFactory
from backend.ptq.PTQ import PTQ
from backend.routing.Routing import Routing
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.smooth.Smooth import Smooth

from permetrics.regression import RegressionMetric

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
class Simulation:
    Metrics2 = ["RMSE", "MAE", "MAPE", "R2", "NSE", "KGE"]
    Metrics = ["NSE", "KGE", "RMSE", "MAE", "MAPE", "R2"]
    def __init__(self,production_method,recession_method,routing_method, loss_method,
                 ptq_calage: PTQ,ptq_validation : PTQ):
        self.methods = {
            "production" : production_method,
            "recession" : recession_method,
            "routing" : routing_method,
            "initial_loss" : loss_method
        }
        self.routing_model = []

        self.crit = "NSE"

        self.ptq_calage = ptq_calage
        self.ptq_validation = ptq_validation
        self.kwargs = {}
        self.calibration_metric = 0
        self.q_means = ptq_calage.daily_qobs_mean()
        self.prev_q_calib = ptq_calage.get_prev_q_obs()
        self.prev_q_valid = ptq_validation.get_prev_q_obs()
        
        #--------- ROUTING WARMUP ------------------------------------
        self.qdirect_means = np.maximum(0, self.q_means - RecessionFactory.createInstance("Chapman",*[0.925]).compute(self.q_means))
        #-------- RECESSION WARMUP--------------------------------------
        self.qbase_default = RecessionFactory.createInstance("Chapman",*[0.925]).compute(self.ptq_calage.q)
        """
        self.qdirect_means = pd.Series(np.maximum(0, 
            self.ptq_calage.q - RecessionFactory.createInstance("Chapman",*[0.925]).compute(self.ptq_calage.q)))
        
        self.qdirect_means = self.qdirect_means.groupby(self.ptq_calage.dates.dt.strftime("%m-%d")).mean()
        """
        self.direct_flow_default = pd.Series(np.maximum(0, self.ptq_calage.q-
                                              RecessionFactory.createInstance("Chapman",*[0.925]).compute(self.ptq_calage.q)))
        
        debit_sim = self.direct_flow_default.where(self.ptq_calage.p != 0).dropna()
        debit_base = (self.qbase_default.where(self.ptq_calage.p != 0)).dropna()
        self.recession_factors = BaseFlowRoutine.regBaseFlow(debit_base,debit_sim)

        self.output_lim = 3.5
        self.window = 1

        
    

    def manual_calibration(self,kwargs: RoutingData):
        self.kwargs = kwargs
        prod_rainfall = ProductionFactory.createInstance(self.methods["production"],self.ptq_calage.p,*kwargs["pn"]).compute()
                
        ia_bundle : DataInitialLoss = {
            "net_rainfall" : prod_rainfall,
            "etp" : self.ptq_calage.etp
        }
        net_rainfall = InitialLossFactory.createInstance(self.methods["initial_loss"],ia_bundle,*kwargs["loss"]).compute()

        self.qbase_model : BaseFlow = RecessionFactory.createInstance(self.methods["recession"],*kwargs["qb"])
        
        """ --------------- TRANSFER ROUTINE ----------------"""

        routing_bundle : DataSimulation = {
            "pn" : net_rainfall,
            "qbase" : self.qbase_default,
            "qobs" : self.ptq_calage.q,
            "p" : self.ptq_calage.p,
            "dates" : self.ptq_calage.dates,
            "qdirect_means": self.ptq_calage.expand_flow(self.ptq_calage.dates,self.qdirect_means)
        }

        self.routing_model : Routing = RoutingFactory.createInstance(self.methods["routing"],self.kwargs["sim"])
        
        qsim = self.routing_model.calage(routing_bundle)

        """ --------------- BASE FLOW ROUTINE ----------------"""

        baseflow_bundle : DataBaseFlow = {
            "p" : self.ptq_calage.p,
            "qObs" : self.ptq_calage.q,
            "qsim" : pd.Series(qsim),
            "prevObs" : self.prev_q_calib,
            "factors" : self.recession_factors
        }


        qbase_rev_corr = self.qbase_model.calibration_routine(baseflow_bundle)

        qsim_total = qsim+qbase_rev_corr
        
        evaluator = RegressionMetric(np.array(self.ptq_calage.q), np.array(qsim_total))
        self.calibration_metric = evaluator.get_metrics_by_list_names(self.Metrics)
        print("NSE CALIBRATION ----------- : ", evaluator.get_metrics_by_list_names(self.calibration_metric))
        #◘plt.plot(qsim_total, "r")
        #plt.plot(self.ptq_calage.q, "b")
        return qsim_total
    

    def validation(self):
        print("***** VALIDATION DANS SIMULATION ", self.kwargs)
        prod_rainfall = ProductionFactory.createInstance(self.methods["production"],self.ptq_validation.p,*self.kwargs["pn"]).compute()

        ia_bundle : DataInitialLoss = {
            "net_rainfall" : prod_rainfall,
            "etp" : self.ptq_validation.etp
        }
        net_rainfall = InitialLossFactory.createInstance(self.methods["initial_loss"],ia_bundle,*self.kwargs["loss"]).compute()
        

        datas_bundle : DataSimulation = {
            "pn" : net_rainfall,
            "dates" : self.ptq_validation.dates,
            "qdirect_means": self.ptq_validation.expand_flow(self.ptq_validation.dates,self.qdirect_means)
        }
        qsim = self.routing_model.validation(datas_bundle)

        baseflow_bundle : DataBaseFlow = {
            "p" : self.ptq_validation.p,
            "qbase" : pd.Series(),
            "qsim" : pd.Series(qsim),
            "prevObs" : self.prev_q_valid,
            "factors" : self.recession_factors
        }


        qbase_rev_corr = pd.Series(self.qbase_model.validation_routine(baseflow_bundle))
        qsim_total = qsim + qbase_rev_corr

        evaluator = RegressionMetric(np.array(self.ptq_validation.q), np.array(qsim_total))
        results = evaluator.get_metrics_by_list_names(self.Metrics)
        print("NSE VALIDATION ----------- : ", evaluator.get_metrics_by_list_names(self.Metrics))
        plt.plot(qsim_total, "r")
        plt.plot(self.ptq_validation.q, "b")
        return results, qsim_total
