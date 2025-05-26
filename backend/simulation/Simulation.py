from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.baseFlow.BaseFlowRoutine2 import BaseFlowRoutine2
from backend.contracts.Bundle import DataInitialLoss, DataSimulation, RoutingData, DataBaseFlow
from backend.factory.RoutingFactory import RoutingFactory
from backend.factory.InitialLossFactory import InitialLossFactory
from backend.factory.ProductionFactory import ProductionFactory
from backend.factory.RecessionFactory import RecessionFactory
from backend.ptq.PTQ import PTQ
from backend.routing.Routing import Routing

from backend.baseFlow.ExponentialRecession import ExponentialRecessionCurve
from backend.baseFlow.IHACRES import IHACRES
from backend.baseFlow.NashBaseFlow import NashBaseFlow

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
        self.q_means = np.array(ptq_calage.daily_qobs_mean())

        self.baseflow_routine = None
        

    def manual_calibration(self,kwargs: RoutingData):
        self.kwargs = kwargs
        ia_bundle : DataInitialLoss = {
            "net_rainfall" : self.ptq_calage.p,
            "etp" : self.ptq_calage.etp
        }
        net_rainfall = InitialLossFactory.createInstance(self.methods["initial_loss"],ia_bundle,*kwargs["loss"]).compute()
        
        prod_rainfall = ProductionFactory.createInstance(self.methods["production"],net_rainfall,*kwargs["pn"]).compute()
                

        self.qbase_model : BaseFlow = RecessionFactory.createInstance(self.methods["recession"],*kwargs["qb"])
        

        """ --------------- TRANSFER ROUTINE ----------------"""
        q_base = self.qbase_model.compute(self.ptq_calage)

        routing_bundle : DataSimulation = {
            "pn" : prod_rainfall,
            "qbase" : q_base,
            "qobs" : self.ptq_calage.q,
            "p" : self.ptq_calage.p,
            "dates" : self.ptq_calage.dates
        }

        self.routing_model : Routing = RoutingFactory.createInstance(self.methods["routing"],self.kwargs["sim"])
        
        qsim = self.routing_model.calage(routing_bundle)

        """ --------------- BASE FLOW ROUTINE ----------------"""
        self.baseflow_routine = BaseFlowRoutine(self.qbase_model)

        baseflow_bundle : DataBaseFlow = {
            "ptq" : self.ptq_calage,
            "qbase" : q_base,
            "qsim" : qsim,
            "qmean" : self.q_means
        }

        qbase_rev_corr = pd.Series(self.baseflow_routine.calibration_routine(baseflow_bundle))
        qsim_total = qsim+qbase_rev_corr

        plt.plot(qbase_rev_corr, "r")
        plt.plot(q_base, "b")

        evaluator = RegressionMetric(np.array(self.ptq_calage.q), np.array(qsim_total))
        self.calibration_metric = evaluator.get_metrics_by_list_names(self.Metrics)
        
        print("NSE BASEFLOW CALAGE -----------")
        evaluator = RegressionMetric(np.array(q_base), np.array(qbase_rev_corr))
        evaluator2 = RegressionMetric(np.array(self.ptq_calage.q), np.array(qsim_total))
        print(evaluator.get_metrics_by_list_names(self.Metrics))
        print(evaluator2.get_metrics_by_list_names(self.Metrics))
        
        return qsim_total
    

    def validation(self):
        print("***** VALIDATION DANS SIMULATION ")
        #print(self.kwargs)
        ia_bundle : DataInitialLoss = {
            "net_rainfall" : self.ptq_validation.p,
            "etp" : self.ptq_validation.etp
        }
        net_rainfall = InitialLossFactory.createInstance(self.methods["initial_loss"],ia_bundle,*self.kwargs["loss"]).compute()
        
        prod_rainfall = ProductionFactory.createInstance(self.methods["production"],net_rainfall,*self.kwargs["pn"]).compute()

        
        datas_bundle : DataSimulation = {
            "pn" : prod_rainfall
        }
        qsim = self.routing_model.validation(datas_bundle)

        baseflow_bundle : DataBaseFlow = {
            "ptq" : self.ptq_validation,
            "qbase" : pd.Series(),
            "qsim" : qsim,
            "qmean" : self.q_means
        }


        qbase_rev_corr = pd.Series(self.baseflow_routine.validation_routine(baseflow_bundle))
        qsim_total = qsim + qbase_rev_corr
    
        print("NSE BASEFLOW VALIDATION -----------")
         
        bfm_values = self.baseflow_routine.baseflowModel.compute(self.ptq_validation)
        evaluator = RegressionMetric(np.array(bfm_values),np.array(qbase_rev_corr))
        print(evaluator.get_metrics_by_list_names(self.Metrics))

        #plt.plot(qbase_rev_corr, "r")
        #plt.plot(bfm_values, "b")
        plt.plot(self.ptq_validation.q, "b")
        plt.plot(qsim_total, "r")
        plt.plot(qbase_rev_corr, "black")
        #plt.plot(self.ptq_validation.q, "g")
        #plt.plot(qsim, "y")   
        #plt.plot(self.ptq_calage.q, "black")    
        evaluator2 = RegressionMetric(np.array(self.ptq_validation.q), np.array(qsim_total))
        print("----------- NSE --------------")
        results = evaluator2.get_metrics_by_list_names(self.Metrics)
        print(results)
        
        return results, qsim_total
