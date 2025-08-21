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
        self.q_means = ptq_calage.daily_mean(ptq_calage.dates, self.ptq_calage.q)
        self.prev_q_calib = ptq_calage.get_prev_q_obs()
        self.prev_q_valid = ptq_validation.get_prev_q_obs()
        
        #--------- ROUTING WARMUP ------------------------------------
        self.qdirect_means = None
        #-------- RECESSION WARMUP--------------------------------------
        self.qbase_default = None
        """
        self.qdirect_means = pd.Series(np.maximum(0, 
            self.ptq_calage.q - RecessionFactory.createInstance("Chapman",*[0.925]).compute(self.ptq_calage.q)))
        
        self.qdirect_means = self.qdirect_means.groupby(self.ptq_calage.dates.dt.strftime("%m-%d")).mean()
        """
        self.direct_flow_default = None

        self.recession_factors = None

        
    

    def manual_calibration(self,kwargs: RoutingData):
        self.kwargs = kwargs
        prod_rainfall = ProductionFactory.createInstance(self.methods["production"],self.ptq_calage.p,*kwargs["pn"]).compute()
                
        ia_bundle : DataInitialLoss = {
            "net_rainfall" : prod_rainfall,
            "etp" : self.ptq_calage.etp
        }
        net_rainfall = InitialLossFactory.createInstance(self.methods["initial_loss"],ia_bundle,*kwargs["loss"]).compute()

        net_rainfall = np.nan_to_num(net_rainfall)

        self.qbase_model : BaseFlow = RecessionFactory.createInstance(self.methods["recession"],*kwargs["qb"])


        #-------- RECESSION WARMUP--------------------------------------
        #self.qbase_default = self.qbase_model.compute(self.ptq_calage.q)

        """ --------------- TRANSFER ROUTINE ----------------"""
        self.qdirect_means = np.maximum(0, self.q_means - self.qbase_model.compute(self.q_means, self.prev_q_calib))
        routing_bundle : DataSimulation = {
            "pn" : net_rainfall,
            "qdirect_means": self.ptq_calage.expand_flow(self.ptq_calage.dates,self.qdirect_means)
        }

        self.routing_model : Routing = RoutingFactory.createInstance(self.methods["routing"],self.kwargs["sim"])
        
        qsim = self.routing_model.calage(routing_bundle)

        """ --------------- BASE FLOW ROUTINE ----------------"""

        baseflow_bundle : DataBaseFlow = {
            "qObs" : self.ptq_calage.q,
            "qsim" : pd.Series(qsim),
            "prevObs" : self.prev_q_calib,
            "p" : self.ptq_calage.p
        }


        qbase_rev_corr = self.qbase_model.calibration_routine(baseflow_bundle)
        #raise ValueError("len(qbase_rev_corr) : ",len(qbase_rev_corr), "len(qsim) ", len(qsim))
        print("qsim_total ------------------------ :", len(qsim))
        print("qbase_rev_corr *****************************************:", len(qbase_rev_corr))
        qsim_total = qsim+qbase_rev_corr

        
        q = pd.DataFrame({"obs" : self.ptq_calage.q,"sim" : qsim_total}).dropna()
        evaluator = RegressionMetric((np.array(q["obs"]) + 1e-10) , (np.array(q["sim"]) + 1e-10))
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
        net_rainfall = np.nan_to_num(net_rainfall)

        datas_bundle : DataSimulation = {
            "pn" : net_rainfall,
            "qdirect_means": self.ptq_validation.expand_flow(self.ptq_validation.dates,self.qdirect_means)
        }
        qsim = self.routing_model.validation(datas_bundle)

        baseflow_bundle : DataBaseFlow = {
            "p" : self.ptq_validation.p,
            "qbase" : pd.Series(),
            "qsim" : pd.Series(qsim),
            "prevObs" : self.prev_q_valid
        }


        qbase_rev_corr = pd.Series(self.qbase_model.validation_routine(baseflow_bundle))
        qsim_total = qsim + qbase_rev_corr
        q = pd.DataFrame({"obs" : self.ptq_validation.q,"sim" : qsim_total}).dropna()
        evaluator = RegressionMetric((np.array(q["obs"]) + 1e-10) , (np.array(q["sim"]) + 1e-10))

        results = evaluator.get_metrics_by_list_names(self.Metrics)
        print("NSE VALIDATION ----------- : ", evaluator.get_metrics_by_list_names(self.Metrics))
        plt.plot(qsim_total, "r")
        plt.plot(self.ptq_validation.q, "b")
        return results, qsim_total
