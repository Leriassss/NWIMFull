from contracts.Bundle import DataSimulation, RoutingData
from factory.RoutingFactory import RoutingFactory
from factory.InitialLossFactory import InitialLossFactory
from factory.ProductionFactory import ProductionFactory
from factory.RecessionFactory import RecessionFactory
from ptq.PTQ import PTQ
from criteria.Criteria import Criteria
from routing.Routing import Routing
from permetrics.regression import RegressionMetric
import numpy as np

class Simulation:
    def __init__(self,production_method,recession_method,routing_method, loss_method,
                 ptq_calage: PTQ,ptq_validation : PTQ):
        self.methods = {
            "production" : production_method,
            "recession" : recession_method,
            "routing" : routing_method,
            "initial_loss" : loss_method
        }
        self.calibration_results = []
        self.crit = "nse"
        self.criteria = Criteria()
        self.ptq_calage = ptq_calage
        self.ptq_validation = ptq_validation
        self.kwargs = {}

    def manual_calibration(self,kwargs: RoutingData):
        self.kwargs = kwargs
        initial_loss = InitialLossFactory.createInstance(self.methods["initial_loss"],self.ptq_calage,*kwargs["loss"]).compute()
        net_rainfall = ProductionFactory.createInstance(self.methods["production"],initial_loss,*kwargs["pn"]).compute()
        q_base = RecessionFactory.createInstance(self.methods["recession"],self.ptq_calage,*kwargs["qb"]).compute()

        datas_bundle : DataSimulation = {
            "pn" : net_rainfall,
            "qbase" : q_base,
            "qobs" : self.ptq_calage.q,
            "p" : self.ptq_calage.p
        }
        
        self.calibration_results : Routing = RoutingFactory.createInstance(self.methods["routing"],
                                                                    self.kwargs["sim"])
        qsim = self.calibration_results.calage(datas_bundle)
        return qsim
    

    def validation(self):
        print("***** VALIDATION DANS SIMULATION ")
        print(self.kwargs)
        initial_loss = InitialLossFactory.createInstance(self.methods["initial_loss"],self.ptq_validation,*self.kwargs["loss"]).compute()
        net_rainfall = ProductionFactory.createInstance(self.methods["production"],initial_loss,*self.kwargs["pn"]).compute()
        q_base = RecessionFactory.createInstance(self.methods["recession"],self.ptq_validation,*self.kwargs["qb"]).compute()

        datas_bundle : DataSimulation = {
            "pn" : net_rainfall,
            "qbase" : q_base,
            "qobs" : self.ptq_validation.q
        }
        qsim = self.calibration_results.validation(datas_bundle)
        criteria_value = self.criteria.methods()[self.crit](self.ptq_validation.q, qsim)
        evaluator = RegressionMetric(np.array(self.ptq_validation.q), np.array(qsim))
        print("----------- NSE --------------")
        print(evaluator.NSE(multi_output="raw_values"))
        return criteria_value, qsim