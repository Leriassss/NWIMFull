# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 22:32:09 2025

@author: HP
"""

# ------------------------------------- FOR TESTS -------------------
import sys
sys.path.append("C:/Users/HP/Documents/p")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ptq.PTQ import PTQ
 
datas = pd.read_table("F:/MEM MA/tests/ptq.txt",header=0,skiprows=1)
prec =  P = datas['Prec.']
q_obs = datas.Qobs
etp = ETP = pd.read_table("F:/MEM MA/tests/EVAP.txt",header=0)["Etpot"]
datas_dates = dates =pd.to_datetime(datas.date, format='%Y%m%d')

calage_ptq = datas[:1096]
calage_etp = etp[:1096]
calage_datas_dates= datas_dates[:1096]

validation_ptq = datas[1096:].reset_index(drop=True)
validation_etp = etp[1096:].reset_index(drop=True)
validation_datas_dates = datas_dates[1096:].reset_index(drop=True)


ptq__calage_dats = PTQ(calage_ptq['Prec.'], calage_etp, calage_ptq["Qobs"], calage_datas_dates)

ptq_validation_dats = PTQ(validation_ptq['Prec.'], validation_etp, validation_ptq.Qobs, validation_datas_dates)

# ---------------------- AUTOMATIC CALIBRATION TEST -------------------------
#---------------------- DPFT ------------------------------------------
from simulation.Simulation import Simulation
#from factory.InitialLossFactory import InitialLossFactory
sim = Simulation("WMin", "FureyGupta", "DPFT", "s_loss", ptq__calage_dats, ptq_validation_dats)
calibration_bundle_dpft = {
    "pn": [0.5],
    "qb": [0.1, 1.1],
    "sim": [20],
    "loss" : [50,10]
}

dpft_sim = sim.manual_calibration(calibration_bundle_dpft)

plt.plot(dpft_sim)
plt.plot(ptq__calage_dats.q)
dpft_sim
#-----------------------------GRID SIMULATION 2 -----------------------
from graphics.SimulationGraph import SimulationGraph
from grid.Grid import Grid,GridModel
from functools import reduce

productionBundle = {
    "WMin": {"w": [0.1, 0.9]},
    "Horton": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3]},
    "SCS": {"cn": [10, 90], "i_a" : [0.1,0.5]},
    "Holtan": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3], "sc": [1,20]},
    "Philip":{"S":[1,20], "K":[1,20]}
}

recessionBundle = {
    "FureyGupta": {"gamma": [0.08, 0.1], "cs_over_c": [0.5, 2]},
    "Chapman": {"alpha": [0.7, 1]},
    "Quadratic": {"lambda" : [0.1,0.7]},
    "Exponential": {"lambda" : [0.1,0.7]}
}

lossBundle = {
    "ia_loss": {"s": [0, 50], "alpha": [0, 1], "loss_days": [0, 100]},
    "eto_loss" : {"alpha" : [0.1, 0.5]},
    "s_loss" : {"s":[0,50], "loss_days": [0, 10]},
    "p_loss" : {"p" : [0.2, 0.5]},
    "no_loss" : {"no" : [0, 1]}
}


routingBundle = {
    #"Muskingum": {"k" : [1,50],"x" : [0.2,0.5],"dt" : [1,50]},
    "PLA": {"mu" : [1,5],"landa" : [1,20],"t_x" : [0.1, 0.9],"s_f" : [0.01, 0.09]},
    #"Nash": {"nash_k": [1, 50], "nash_n": [1, 50], "time_base": [1, 20]},
    #"HUN": {"dt": [1, 1.1], "time_base": [1, 25]}
}


gm = GridModel(productionBundle, recessionBundle, routingBundle, lossBundle)
      

grid_search = Grid(gm, ptq__calage_dats, ptq_validation_dats)

grid_results = grid_search.grid_optimization("lhc", n_samples=150)

simGraph = SimulationGraph(ptq__calage_dats, ptq_validation_dats, grid_results)
simGraph.plot("AFFON - " + reduce((lambda x,y: x+", "+y), [v for  v in grid_search.combin])) 

#--------------------------------- FILE -------------------------------------------
from results.CalibrationResults import CalibrationResults
calib_res = CalibrationResults()
calib_res.save_calibration(grid_results,"PLA_lhc")
file_model = calib_res.load_calibration("Essai")

sim_file = SimulationGraph(ptq__calage_dats, ptq_validation_dats, file_model)
sim_file.plot("AFFON")
#--------------------------------MANUAL CALIBRATION ----------------------------
from calibration.ManualCalibration import ManualCalibration
from simulation.Simulation import Simulation

sim = Simulation(*grid_search.combin, ptq__calage_dats, ptq_validation_dats)

manual_calib = ManualCalibration(sim)  

res_m_c = manual_calib.sim(grid_results.params)   

simGraph = SimulationGraph(ptq__calage_dats, ptq_validation_dats, grid_results)
simGraph.plot("AFFON - " + reduce((lambda x,y: x+","+y), grid_search.combin)) 
# --------------------------------------GA------------------------------------
from graphics.SimulationGraph import SimulationGraph
from grid.Grid import Grid,GridModel
from functools import reduce

productionBundle = {
    "WMin": {"w": [0.1, 0.9]},
    "Horton": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3]},
    "SCS": {"cn": [10, 90], "i_a" : [0.1,0.5]},
    "Holtan": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3], "sc": [1,20]},
    "Philip":{"S":[1,20], "K":[1,20]}
}

recessionBundle = {
    "FureyGupta": {"gamma": [0.08, 0.1], "cs_over_c": [0.5, 2]},
    "Chapman": {"alpha": [0.7, 1]},
    "Quadratic": {"lambda" : [0.1,0.7]},
    "Exponential": {"lambda" : [0.1,0.7]}
}

lossBundle = {
    "ia_loss": {"s": [0, 50], "alpha": [0, 1], "loss_days": [0, 100]},
    "eto_loss" : {"alpha" : [0.1, 0.5]},
    "s_loss" : {"s":[0,50], "loss_days": [0, 10]},
    "p_loss" : {"p" : [0.2, 0.5]},
    "no_loss" : {"no" : [0, 1]}
}


routingBundle = {
    #"Muskingum": {"k" : [1,50],"x" : [0.2,0.5],"dt" : [1,50]},
    #"PLA": {"mu" : [1,5],"landa" : [1,20],"t_x" : [0.1, 0.9],"s_f" : [0.01, 0.09]},
    #"Nash": {"nash_k": [1, 50], "nash_n": [1, 50], "time_base": [1, 20]},
    "HUN": {"dt": [1, 1.1], "time_base": [1, 25]}
}


gm = GridModel(productionBundle, recessionBundle, routingBundle, lossBundle)
grid_search_ga = Grid(gm, ptq__calage_dats, ptq_validation_dats)
grid_results_ga = grid_search_ga.grid_optimization("ga", max_num_iteration=10)

simGraph_ga = SimulationGraph(ptq__calage_dats, ptq_validation_dats, grid_results_ga)
simGraph_ga.plot("AFFON - " + reduce((lambda x,y: x+","+y), [v for  v in grid_search_ga.combin])) 

grid_results_ga.params
from results.CalibrationResults import CalibrationResults
calib_res = CalibrationResults()
calib_res.save_calibration(grid_results_ga,"HUN_ga")
# --------------------------------------DE------------------------------------
from optimization.DifferentialEvolutionOptimization import DifferentialEvolutionOptimization
from contracts.Bundle import RoutingData
from graphics.SimulationGraph import SimulationGraph
from optimization.models.DEModel import DEModel
from functools import reduce

calibration_bundle_deo : RoutingData = {
    "pn": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3]},
    "qb": {"alpha": [0.7, 1]},
    "sim": {"mu" : [1,5],"landa" : [1,20],"t_x" : [0.1, 0.9],"s_f" : [0.01, 0.09]},
    "loss" : {"s":[0,50], "loss_days": [0, 10]}
}

sim_deo = Simulation('Horton', 'Chapman', 'PLA', 's_loss', ptq__calage_dats,ptq_validation_dats)

deo = DifferentialEvolutionOptimization(sim_deo, calibration_bundle_deo, DEModel()) 
de_results = deo.optim()


simGraph_de = SimulationGraph(ptq__calage_dats, ptq_validation_dats, de_results)
simGraph_de.plot("AFFON - " + 'Horton ' + 'Chapman ' + 'PLA ' + 's_loss') 
#-------------------------------- REGRESSION ------------------------------
from regressor.Regressor import Regressor
simulation_list = [grid_results, grid_results_ga]
reg = Regressor(ptq__calage_dats,ptq_validation_dats)
reg_res = reg.knn(simulation_list,35)

grid_results.calibration_sim
simGraph_reg = SimulationGraph(ptq__calage_dats, ptq_validation_dats, reg_res)
simGraph_reg.plot("AFFON - KNN " + "nb Voisins : " + str(reg_res.params['n_neighbors'])) 

simulation_list = [grid_results, grid_results_ga]
reg = Regressor(ptq__calage_dats,ptq_validation_dats)
reg_lin = reg.linreg(simulation_list)
simGraph_reg = SimulationGraph(ptq__calage_dats, ptq_validation_dats, reg_lin)
simGraph_reg.plot("AFFON - LINREG")

#-------------------------------- OBJECTIVE ----------------------------
from objective.Objective import Objective
from contracts.Bundle import RoutingData
calibration_bundle_obj : RoutingData = {
    "pn": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3]},
    "qb": {"alpha": [0.7, 1]},
    "sim": {"mu" : [1,5],"landa" : [1,20],"t_x" : [0.1, 0.9],"s_f" : [0.01, 0.09]},
    "loss" : {"s":[0,50], "loss_days": [0, 10]}
}

sim_obj = Simulation('Horton', 'Chapman', 'PLA', 's_loss', ptq__calage_dats,ptq_validation_dats)

obj_search = Objective(sim_obj)

obj_res = obj_search.sim(0.90, "lhc", calibration_bundle_obj,n_sim=100, n_samples = 35)

simGraph_obj = SimulationGraph(ptq__calage_dats, ptq_validation_dats, obj_res)
simGraph_obj.plot("AFFON - OBJ")