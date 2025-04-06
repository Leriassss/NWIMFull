from backend.contracts.Bundle import DataSimulation, RoutingData, DataBaseFlow
from backend.factory.RoutingFactory import RoutingFactory
from backend.factory.InitialLossFactory import InitialLossFactory
from backend.factory.ProductionFactory import ProductionFactory
from backend.factory.RecessionFactory import RecessionFactory
from backend.ptq.PTQ import PTQ
from backend.criteria.Criteria import Criteria
from backend.routing.Routing import Routing
from backend.baseFlow.BaseFlowRoutine import BaseFlowRoutine
from permetrics.regression import RegressionMetric
import numpy as np

import matplotlib.pyplot as plt
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
        self.baseFlowRoutine = BaseFlowRoutine(ptq_calage)
        self.a,self.b,self.correc_factor = 0, 0, 0

    def manual_calibration(self,kwargs: RoutingData):
        self.kwargs = kwargs
        initial_loss = InitialLossFactory.createInstance(self.methods["initial_loss"],self.ptq_calage,*kwargs["loss"]).compute()
        net_rainfall = ProductionFactory.createInstance(self.methods["production"],initial_loss,*kwargs["pn"]).compute()
        
        q_base_model = RecessionFactory.createInstance(self.methods["recession"],self.ptq_calage,*kwargs["qb"])
        
        q_base = q_base_model.compute()
        
        prev_day = self.ptq_calage.get_qobs_mean(self.ptq_calage.dates[0])
        #FITTING DES COEFFICIENTS POUR LA RELATION QBASE-QOBS
        self.a,self.b  = self.baseFlowRoutine.regBaseFlow(q_base , self.ptq_calage.q)
        #DETERMINATION DU DEBIT MOYEN JOURNALIER CORRESPONDANT
        q_means = np.array(self.ptq_calage.daily_qobs_mean())
        q_obs_mean = q_means[prev_day]
        #DETERMINATION DU DEBIT DE BASE PRECEDENT
        q_base_previous = self.baseFlowRoutine.modele_baseflow(q_obs_mean, self.a, self.b)
        
        datas_bundle : DataSimulation = {
            "pn" : net_rainfall,
            "qbase" : q_base,
            "qobs" : self.ptq_calage.q,
            "p" : self.ptq_calage.p,
            "dates" : self.ptq_calage.dates
        }
        
        self.calibration_results : Routing = RoutingFactory.createInstance(self.methods["routing"],
                                                                    self.kwargs["sim"])
        qsim = self.calibration_results.calage(datas_bundle)

        #CALCUL DU DEBIT DE BASE PAR LA METHODE REVERSE
        qbase_rev = q_base_model.reverse_compute(q_base_previous, qsim)
        
        # CALCUL DU FACTEUR DE CORRECTION
        self.correc_factor = self.baseFlowRoutine.correction_factor(qbase_rev, q_base)

        qbase_rev_corr =  self.correc_factor * qbase_rev


        qsim_total = np.array(qsim + qbase_rev_corr )
        qsim_total2 = np.array(qsim + q_base)

        plt.plot(self.ptq_calage.q)
        plt.plot(qsim_total)
        print("--------------- REVERSE ---------------------")

        evaluator_qt = RegressionMetric(np.array(self.ptq_calage.q),qsim_total)
        print(evaluator_qt.NSE(multi_output="raw_values"))

        evaluator_qt = RegressionMetric(np.array(self.ptq_calage.q),qsim_total2)
        print(evaluator_qt.NSE(multi_output="raw_values"))

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
