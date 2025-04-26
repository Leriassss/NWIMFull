from backend.baseFlow.BaseFlow import BaseFlow
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from backend.contracts.Bundle import DataInitialLoss, DataSimulation, RoutingData, DataBaseFlow
from backend.factory.RoutingFactory import RoutingFactory
from backend.factory.InitialLossFactory import InitialLossFactory
from backend.factory.ProductionFactory import ProductionFactory
from backend.factory.RecessionFactory import RecessionFactory
from backend.ptq.PTQ import PTQ
from backend.routing.Routing import Routing

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

        inf_rainfall = ProductionFactory.createInstance(self.methods["production"],self.ptq_calage.p,*kwargs["pn"]).compute()
        ia_bundle : DataInitialLoss = {
            "net_rainfall" : inf_rainfall,
            "etp" : self.ptq_calage.etp
        }
        initial_loss = InitialLossFactory.createInstance(self.methods["initial_loss"],ia_bundle,*kwargs["loss"]).compute()
        net_rainfall = pd.Series(np.maximum(0, inf_rainfall - initial_loss))

        self.qbase_model : BaseFlow = RecessionFactory.createInstance(self.methods["recession"],*kwargs["qb"])
        
        """ --------------- TRANSFER ROUTINE ----------------"""
        q_base = self.qbase_model.compute(self.ptq_calage)

        routing_bundle : DataSimulation = {
            "pn" : net_rainfall,
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

        #plt.plot(qbase_rev_corr, "r")
        #plt.plot(q_base, "b")

        evaluator = RegressionMetric(np.array(self.ptq_calage.q), np.array(qsim_total))
        self.calibration_metric = evaluator.get_metrics_by_list_names(self.Metrics)
        """
        print("NSE BASEFLOW CALAGE -----------")
        print(rain_lost.sum())
        evaluator = RegressionMetric(np.array(q_base), np.array(qbase_rev_corr))
        print(evaluator.get_metrics_by_list_names(self.Metrics))
        """
        return qsim_total
    

    def validation(self):
        print("***** VALIDATION DANS SIMULATION ")
        #print(self.kwargs)
        inf_rainfall = ProductionFactory.createInstance(self.methods["production"],self.ptq_validation.p,*self.kwargs["pn"]).compute()
        ia_bundle : DataInitialLoss = {
            "net_rainfall" : inf_rainfall,
            "etp" : self.ptq_validation.etp
        }
        initial_loss = InitialLossFactory.createInstance(self.methods["initial_loss"],ia_bundle,*self.kwargs["loss"]).compute()
        net_rainfall = pd.Series(np.maximum(0, inf_rainfall - initial_loss))
        
        datas_bundle : DataSimulation = {
            "pn" : net_rainfall
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
        print((self.ptq_validation.p - net_rainfall).sum())
        
        evaluator = RegressionMetric(np.array(self.baseflow_routine.baseflowModel.compute(self.ptq_validation)),
                                      np.array(qbase_rev_corr))
        print(evaluator.get_metrics_by_list_names(self.Metrics))

        #plt.plot(qbase_rev_corr, "r")
        #plt.plot(self.qbase_model.compute(self.ptq_validation), "b")
        
        evaluator = RegressionMetric(np.array(self.ptq_validation.q), np.array(qsim_total))
        print("----------- NSE --------------")
        results = evaluator.get_metrics_by_list_names(self.Metrics)
        print(results)
        
        return results, qsim_total
