# -*- coding: utf-8 -*-

import numpy as np
from geneticalgorithm import geneticalgorithm as ga

from backend.contracts.Bundle import RoutingData
from backend.optimization.Optimization import Optimization
from backend.optimization.models.GAModel import GAModel
from backend.simulation.Simulation import Simulation
from backend.simulation.models.SimulationModel import SimulationModel

class GeneticalAlgorithmOptimization(Optimization):
    def __init__(self, simulation : Simulation, kwargs : RoutingData, params_algo : GAModel):
        self.simulation = simulation
        self.kwargs = {key : kwargs[key] for key in ["pn", "qb", "loss", "sim"]}
        self.kwargs_length = np.array([len(v) for v in self.kwargs.values()])
        self.params_algo = params_algo

    def optim(self):
        values = [v for category in self.kwargs.values() for v in category.values()]
        
        params_bounds = np.array(values, dtype=float)

        dim = sum(self.kwargs_length)
        

        model=ga(function=self.ga_func,dimension=dim,variable_type='real', 
                 variable_boundaries=params_bounds,algorithm_parameters=self.params_algo.to_dict(),
                 convergence_curve = False)
        out_p= model.run()
        results =  model.output_dict
        

        ga_variable = results['variable']
        ga_crit = results['function']
        
        qsim_calage, best_ = self.get_qsim_calibration(ga_variable)
        
        best_pars = {key : value.tolist() for key, value in best_.items()}
        criteria_validation, qsim_validation = self.simulation.validation() 

        return SimulationModel(qsim_calage, qsim_validation, best_pars, abs(ga_crit) , criteria_validation[self.simulation.crit])


    def ga_func(self,X):
        args = {
            'pn' : X[0: self.kwargs_length[0]],
            'qb' : X[self.kwargs_length[0] : sum(self.kwargs_length[:2])],
            'loss': X[sum(self.kwargs_length[:2]) : sum(self.kwargs_length[:3])],
            'sim':X[sum(self.kwargs_length[:3]) : sum(self.kwargs_length[:4])]
        }
        
        qsim = self.simulation.manual_calibration(args)
        criteria_value = self.simulation.calibration_metric[self.simulation.crit]
        return -criteria_value

    def get_qsim_calibration(self, ga_variable):
        kwl = self.kwargs_length
        args = {
                'pn' : ga_variable[0: kwl[0]],
                'qb' : ga_variable[kwl[0] : sum(kwl[:2])],
                'loss': ga_variable[sum(kwl[:2]) : sum(kwl[:3])],
                'sim': ga_variable[sum(kwl[:3]) : sum(kwl[:4])]
                }
        qsim = self.simulation.manual_calibration(args)
        return qsim , args
