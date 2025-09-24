# -*- coding: utf-8 -*-

import numpy as np
from scipy.optimize import differential_evolution

from backend.contracts.Bundle import RoutingData
from backend.optimization.models.DEModel import DEModel
from backend.simulation.Simulation import Simulation
from backend.simulation.models.SimulationModel import SimulationModel

class DifferentialEvolutionOptimization:
    def __init__(self, simulation : Simulation, kwargs : RoutingData, de_model : DEModel):
        self.simulation = simulation
        self.kwargs_length = np.array([len(v) for v in kwargs.values()])

        self.de_model = de_model 
        desired_order = ["pn","qb","sim","loss"]

        #REORDONNE LES KWARGS POUR SE CONFORMER AU FORMATING UNIVERSEL ROUTINGDATA
        self.kwargs = {key: kwargs[key] for key in desired_order if key in kwargs}


    def optim(self): 
        pars_bounds = [v for category in self.kwargs.values() for v in category.values()]   
                        
        model = differential_evolution(func = self.de_func, bounds = pars_bounds,
                                        updating='deferred', workers=-1)

        qsim_calage, best_= self.get_qsim_calibration(model["x"])
        criteria_validation, qsim_validation = self.simulation.validation()
        best_pars = {key : value.tolist() for key, value in best_.items()}
        
        return SimulationModel(qsim_calage, qsim_validation, best_pars,  abs(model["fun"]), criteria_validation[self.simulation.crit])
    
    
    def de_func(self,X):
        args = {
            'pn' : X[0: self.kwargs_length[0]],
            'qb' : X[self.kwargs_length[0] : sum(self.kwargs_length[:2])],
            'sim': X[sum(self.kwargs_length[:2]) : sum(self.kwargs_length[:3])],
            'loss':X[sum(self.kwargs_length[:3]) : sum(self.kwargs_length[:4])]
        }
        #criteria_method =  self.simulation.crit
        qsim = self.simulation.manual_calibration(args)
        #criteria_value = self.simulation.calibration_metric[self.simulation.crit]
        try :
            criteria_value = self.simulation.calibration_metric["NSE"]*self.simulation.weightNSE + self.simulation.calibration_metric["KGE"]*self.simulation.weightKGE
        except Exception as e:
            print(e, criteria_value)

        return -criteria_value

    def get_qsim_calibration(self, ga_variable):
        kwl = self.kwargs_length
        args = {
                'pn' : ga_variable[0: kwl[0]],
                'qb' : ga_variable[kwl[0] : sum(kwl[:2])],
                'sim': ga_variable[sum(kwl[:2]) : sum(kwl[:3])],
                'loss': ga_variable[sum(kwl[:3]) : sum(kwl[:4])]
                }
        qsim = self.simulation.manual_calibration(args)
        return qsim , args
