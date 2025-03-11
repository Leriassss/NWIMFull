
# ------------------------------------- FOR TESTS -------------------
import sys
sys.path.append("C:/Users/HP/Documents/p")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ptq.PTQ import PTQ

"""
from criteria.Criteria import Criteria


from routing.DPFT import DPFT, DPFTModel
from baseFlow.FureyGupta import FureyGupta, FureyGuptaModel
from routing.HUN import HUN, HUNModel
from routing.Muskingum import Muskingum, MuskingumModel

from production.Wmin import WMin, WMinModel
from production.SCS import SCS, SCSModel
from production.Horton import Horton, HortonModel
from production.Phi import Phi, PhiModel
"""

 
datas = pd.read_table("F:/Bassin_Rusizi.txt",header=0,skiprows=1)
prec =  P = datas['Prec.']
q_obs = datas.Qobs
etp = ETP = pd.read_table("F:/Etpot.txt",header=0)["Etpot"]
datas_dates = dates =pd.to_datetime(datas.date, format='%Y%m%d')

calage_ptq = datas[:3650]
calage_etp = etp[:3650]
calage_datas_dates= datas_dates[:3650]

validation_ptq = datas[3650:].reset_index(drop=True)
validation_etp = etp[3650:].reset_index(drop=True)
validation_datas_dates = datas_dates[3650:].reset_index(drop=True)


ptq__calage_dats = PTQ(calage_ptq['Prec.'], calage_etp, calage_ptq["Qobs"], calage_datas_dates)

ptq_validation_dats = PTQ(validation_ptq['Prec.'], validation_etp, validation_ptq.Qobs, validation_datas_dates)

# ---------------------- AUTOMATIC CALIBRATION TEST -------------------------
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

#--------------------------------------------------------------------


from optimization.DifferentialEvolutionOptimization import DifferentialEvolutionOptimization
from contracts.Bundle import RoutingData
from graphics.SimulationGraph import SimulationGraph
from optimization.models.DEModel import DEModel
from simulation.Simulation import Simulation

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


calibration_bundle_deo_2 : RoutingData = {
    "pn": {"f_0": [1, 20], "f_t": [1, 3], "k": [1, 3]},
    "qb": {"alpha": [0.7, 1]},
    "sim": {"dt": [1, 1.1], "time_base": [1, 25]},
    "loss" : {"s":[0,50], "loss_days": [0, 10]}
}

sim_deo_2 = Simulation('Horton', 'Chapman', 'PLA', 's_loss', ptq__calage_dats,ptq_validation_dats)

deo_2 = DifferentialEvolutionOptimization(sim_deo_2, calibration_bundle_deo_2, DEModel()) 
de_results_2 = deo_2.optim()


simGraph_de_2 = SimulationGraph(ptq__calage_dats, ptq_validation_dats, de_results_2)
simGraph_de_2.plot("AFFON - " + 'Horton ' + 'Chapman ' + 'HUN ' + 's_loss') 

from regressor.Regressor import Regressor
simulation_list = [de_results]
reg = Regressor(ptq__calage_dats,ptq_validation_dats)
reg_res = reg.knn(simulation_list,35)
simGraph_reg = SimulationGraph(ptq__calage_dats, ptq_validation_dats, reg_res)
simGraph_reg.plot("AFFON - KNN " + "nb Voisins : " + str(reg_res.params['n_neighbors'])) 
#---------------------------------------------------- PLA -----------------------------

from simulation.Simulation import Simulation

calibration_bundle_pla = {
    "pn": { 
        None
    },
    "qb": {
        None
    },
    "sim": {
        "mu" : [2,5],
        "landa" : [8,10],
        "t_x" : [0.24, 0.26],
        "s_f" : [0.024, 0.026]
    }
}


sim_pla = Simulation("", "", "PLA")
simulationModelPLA = sim_pla.objective(0.2, "latin_hypercube", ptq__calage_dats,
                                                  ptq_validation_dats,
                                                  calibration_bundle_pla,
                                                  100, "nse")



plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim_pla,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation_pla,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_validation_pla.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(best_run_pla["nse"].round(2)))
plt.legend(["QObs","PLA - QSim Calage","QObs","PLA - QSim Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')
# --------------------------------- NASH -----------------------------------

from simulation.Simulation import Simulation

calibration_bundle_nash = {
    "pn": { 
        "w": [0.1, 0.9]
    },
    "qb": {
        "gamma": [0.08, 0.1],
        "cs_over_c": [1.5, 2]
    },
    "sim": {
        "nash_k" : [1,50],
        "nash_n" : [1,100],
        "time_base" : [1,25],
    }
}


sim_nash = Simulation("Wmin", "FureyGupta", "Nash")

simulationModelNash = sim_nash.objective(0.01, "latin_hypercube", ptq__calage_dats,
                                                  ptq_validation_dats,
                                                  calibration_bundle_nash,
                                                  10, "nse")

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim_nash,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation_nash,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_validation_nash.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(best_run_nash["nse"].round(2)))
plt.legend(["QObs","QSim Calage","QObs","QSim Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')
# --------------------------------- MUSKINGUM -----------------------------------

from simulation.Simulation import Simulation

calibration_bundle_muskingum = {
    "pn": { 
        "w": [0.1, 0.9]
    },
    "qb": {
        "gamma": [0.025, 0.03],
        "cs_over_c": [1.1, 1.2]
    },
    "sim": {
        "k" : [0,100],
        "x" : [0.2,0.3],
        "dt" : [1,100],
    }
}


sim_muskingum = Simulation("Wmin", "FureyGupta", "Muskingum")
simulationModelMuskingum = sim_muskingum.objective(0.01, "latin_hypercube", ptq__calage_dats,
                                                  ptq_validation_dats,
                                                  calibration_bundle_muskingum,
                                                  100, "nse")


plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_validation.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(best_run["nse"].round(2)))
plt.legend(["QObs","QSim Calage","QObs","QSim Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')

#----------------------------------------------------------------------------------
from regressor.Regressor import Regressor
simulation_list = [simulationModel,simulationModelPLA,simulationModelNash, simulationModelMuskingum]
reg = Regressor(ptq__calage_dats,ptq_validation_dats)

q_sim_knn_calage, nse_knn_calage, q_sim_knn_validation, nse_knn_validation = reg.knn(simulation_list,35)
plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,q_sim_knn_calage,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_knn_validation,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_knn_validation.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(nse_knn_calage.round(2)))
plt.legend(["QObs","QSim KNN Calage","QObs","QSim KNN Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')



q_sim_lin_calage, nse_lin_calage, q_sim_lin_validation, nse_lin_validation = reg.linreg(simulation_list)
plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,q_sim_lin_calage,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_lin_validation,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_lin_validation.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(nse_lin_calage.round(2)))
plt.legend(["QObs","QSim LIN-REG Calage","QObs","QSim LIN-REG Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')


#------------------------- KNN --------------------------------------------
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from criteria.Criteria import Criteria

knn2 = KNeighborsRegressor(n_neighbors=10)

knn2.fit(pd.concat([calage_etp, ptq__calage_dats.p],axis=1),np.array(ptq__calage_dats.q))


q_sim_knn_validation2 = knn2.predict(pd.concat([validation_etp, ptq_validation_dats.p],axis=1))
q_sim_knn_calage2 = knn2.predict(pd.concat([calage_etp, ptq__calage_dats.p],axis=1))

nse_knn_validation2 = Criteria().kge(ptq_validation_dats.q , q_sim_knn_validation2)
nse_knn_calage2 = Criteria().kge(ptq__calage_dats.q , q_sim_knn_calage2)

plt.plot(ptq_validation_dats.q)
plt.plot(q_sim_knn_validation)

plt.plot(ptq__calage_dats.q)
plt.plot(q_sim_knn_calage)

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,q_sim_knn_calage,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_knn_validation,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_knn_validation.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(nse_knn_calage.round(2)))
plt.legend(["QObs","QSim KNN Calage","QObs","QSim KNN Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')

#------------------------- KNN CROSS --------------------------------------------
best_results = pd.concat([best_sim_hun,pd.Series(best_sim_pla),best_sim_nash,best_sim],axis=1)

best_results_validation = pd.concat([q_sim_validation_hun,pd.Series(q_sim_validation_pla),q_sim_validation_nash ,q_sim_validation],axis=1)

from sklearn.neighbors import KNeighborsRegressor
from criteria.Criteria import Criteria

knn = KNeighborsRegressor(n_neighbors=12)

knn.fit(best_results,np.array(ptq__calage_dats.q))
q_sim_knn_validation = np.maximum(0,knn.predict(best_results_validation))
q_sim_knn_calage = np.maximum(0,knn.predict(best_results))

nse_knn_validation = Criteria().kge(ptq_validation_dats.q , q_sim_knn_validation)
nse_knn_calage = Criteria().kge(ptq__calage_dats.q , q_sim_knn_calage)

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,q_sim_knn_calage,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_knn_validation,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_knn_validation.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(nse_knn_calage.round(2)))
plt.legend(["QObs","QSim KNN Calage","QObs","QSim KNN Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')

#----------------------------- LINEAR REGRESSION ----------------------------------------
best_results = pd.concat([best_sim_hun,pd.Series(best_sim_pla),best_sim_nash,best_sim],axis=1)

best_results_validation = pd.concat([q_sim_validation_hun,pd.Series(q_sim_validation_pla),q_sim_validation_nash ,q_sim_validation],axis=1)

from sklearn import linear_model

from criteria.Criteria import Criteria

linreg = linear_model.LinearRegression()
linreg.fit(best_results,np.array(ptq__calage_dats.q))
q_sim_lin_validation = np.maximum(0,linreg.predict(best_results_validation))
q_sim_lin_calage = np.maximum(0,linreg.predict(best_results))

nse_lin_validation = Criteria().kge(ptq_validation_dats.q , q_sim_lin_validation)
nse_lin_calage = Criteria().kge(ptq__calage_dats.q , q_sim_lin_calage)

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,q_sim_lin_calage,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_lin_validation,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_lin_validation.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(nse_lin_calage.round(2)))
plt.legend(["QObs","QSim LIN-REG Calage","QObs","QSim LIN-REG Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=15,fontname='Times New Roman')
#------------------------------ MANUAL CALIBRATION --------------------------------------
bundle = {
    "pn" : {"prec" : prec,"runoff_coef" : 0.35},
    "qb" : {"flow_series" : q_obs,"gamma":0.03,"cs_over_c": 1.1},
    "sim" : {"etp":pd.Series(etp), "q_obs" : q_obs, "time_base":5}
    }

bundle2 = {
    "pn" : [0.35],
    "qb" : [0.03, 1.1],
    "sim" : [15]
    }

qs = Simulation("Wmin", "FureyGupta", "HUN").calibration(**bundle)
qs2 = Simulation("Wmin", "FureyGupta", "HUN").calibration2(**bundle2)


#-------------------------- VALIDATION -------------------------------------------------
import sys
sys.path.append('C:/Users/HP/Documents/p')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from simulation.Simulation import Simulation
from ptq.PTQ import PTQ
#--------------------------------------------------------------------
calibration_bundle = {
    "pn": { 
        "w": [0.1, 0.8]
    },
    "qb": {
        "gamma": [0.001, 0.1],
        "cs_over_c": [0.1, 2]
    },
    "sim": {
        "k" : [1,30],
        "x" : [0.23,0.3],
        "dt" : [1,1.02],
    }
}


simulation = Simulation("Wmin", "FureyGupta", "Muskingum")
best_run, best_sim = simulation.automatic_calibration(ptq__calage_dats,calibration_bundle, 1000, "nse")
validation_pars = best_run["parameters"].reset_index(level='Parameter', drop=True).groupby("Category").apply(list).to_dict()


plt.plot(ptq__calage_dats.dates,best_sim)
plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q)
plt.text(ptq__calage_dats.dates[0],9,"NSE : " + str(best_run["nse"].round(2)))

nse_validation, q_sim_validation = simulation.validation(ptq_validation_dats,"nse",**validation_pars)

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation,"y")
plt.text(ptq_validation_dats.dates[0],10,"NSE VALIDATION: " + str(nse_validation.round(2)))
plt.text(ptq_validation_dats.dates[0],9,"NSE CALAGE: " + str(best_run["nse"].round(2)))
plt.legend(["QObs","QSim Calage","QObs","QSim Validation"])


#----------------------------------------------------------------------------------
import sys
sys.path.append('C:/Users/HP/Documents/p')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from ptq.PTQ import PTQ
from factory.RoutingFactory import Factory
from simulation.Simulation import Simulation

calibration_bundle_nash = {
    "pn": { 
        "w": [0.1, 0.5]
    },
    "qb": {
        "gamma": [0.001, 0.1],
        "cs_over_c": [1, 1.1]
    },
    "sim": {
        "nash_k" : [1,100],
        "nash_n" : [1,10],
        "time_base" : [1,20],
    }
}

simulation = Simulation("Wmin", "FureyGupta", "Nash")
best_run, best_sim = simulation.automatic_calibration(ptq__calage_dats,calibration_bundle_nash, 1000, "nse")
validation_pars = best_run["parameters"].reset_index(level='Parameter', drop=True).groupby("Category").apply(list).to_dict()
nse_validation, q_sim_validation = simulation.validation(ptq_validation_dats,"nse",**validation_pars)

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation,"y")
plt.text(ptq_validation_dats.dates[0],10,"NSE VALIDATION: " + str(nse_validation.round(2)))
plt.text(ptq_validation_dats.dates[0],9,"NSE CALAGE: " + str(best_run["nse"].round(2)))
plt.legend(["QObs","QSim Calage","QObs","QSim Validation"])

#---------------------------------------------------------------------------
from factory.RoutingFactory import Factory
from simulation.Simulation import Simulation


calibration_bundle_pla = {
    "pn": { 
        None
    },
    "qb": {
        None
    },
    "sim": {
        "mu" : [1,2],
        "landa" : [8,9],
        "t_x" : [0.25, 0.3],
        "s_f" : [0.02, 0.03]
    }
}

simulation = Simulation("None","None","PLA")
best_run, best_sim = simulation.automatic_calibration(ptq__calage_dats,calibration_bundle_pla, 1000, "nse")
validation_pars = best_run["parameters"].reset_index(level='Parameter', drop=True).groupby("Category").apply(list).to_dict()
nse_validation, q_sim_validation = simulation.validation(ptq_validation_dats,"nse",**validation_pars)

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation,"y")
plt.text(ptq_validation_dats.dates[0],10,"NSE VALIDATION: " + str(nse_validation.round(2)))
plt.text(ptq_validation_dats.dates[0],9,"NSE CALAGE: " + str(best_run["nse"].round(2)))
plt.legend(["QObs","QSim Calage","QObs","QSim Validation"])

#-------------------------------------------------------------------------------

from factory.RoutingFactory import Factory
from simulation.Simulation import Simulation


calibration_bundle_dpft = {
    "pn": { 
        "w": [0.1, 0.5]
    },
    "qb": {
        "gamma": [0.001, 0.1],
        "cs_over_c": [1, 1.1]
    },
    "sim": {
        None
    }
}

simulation = Simulation("None","None","PLA")
best_run, best_sim = simulation.automatic_calibration(ptq__calage_dats,calibration_bundle_pla, 1000, "nse")
validation_pars = best_run["parameters"].reset_index(level='Parameter', drop=True).groupby("Category").apply(list).to_dict()
nse_validation, q_sim_validation = simulation.validation(ptq_validation_dats,"nse",**validation_pars)

plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation,"y")
plt.text(ptq_validation_dats.dates[0],10,"NSE VALIDATION: " + str(nse_validation.round(2)))
plt.text(ptq_validation_dats.dates[0],9,"NSE CALAGE: " + str(best_run["nse"].round(2)))
plt.legend(["QObs","QSim Calage","QObs","QSim Validation"])

#--------------------------------------- DPFT ------------------------------
from simulation.Simulation import Simulation

calibration_bundle_dpft = {
    "pn": { 
        "w": [0.1, 0.3]
    },
    "qb": {
        "gamma": [0.025, 0.03],
        "cs_over_c": [1.1, 1.2]
    },
    "sim": {
        "iterations": [1,2]
    }
}


sim_dpft = Simulation("Wmin", "FureyGupta", "DPFT")
best_run_dpft, best_sim_dpft = sim_dpft.automatic_calibration(ptq__calage_dats,
                                                  ptq_validation_dats,
                                                  calibration_bundle_dpft,
                                                  2, "nse")

validation_pars = best_run_dpft["parameters"].reset_index(level='Parameter', drop=True).groupby("Category").apply(list).to_dict()

nse_validation_dpft, q_sim_validation_dpft = sim_dpft.validation()

hun_dpft = sim_dpft.calibration_results.transfer_function
plt.plot(ptq__calage_dats.dates,ptq__calage_dats.q,"b",ptq__calage_dats.dates,best_sim_dpft,"r")
plt.plot(ptq_validation_dats.dates,ptq_validation_dats.q,"b",ptq_validation_dats.dates,q_sim_validation_dpft,"y")
plt.text(ptq_validation_dats.dates[300],10,"NSE VALIDATION: " + str(nse_validation_dpft.round(2)))
plt.text(ptq_validation_dats.dates[300],9,"NSE CALAGE: " + str(best_run_dpft["nse"].round(2)))
plt.legend(["QObs","DPFT - QSim Calage","QObs","DPFT - QSim Validation"],loc=2)
plt.title('DONGA - AFFON ',fontsize=20,fontname='Times New Roman')
#-------------------------------- PLA --------------------------------------


# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:15:16 2025

@author: HP
"""


import numpy as np
from geneticalgorithm import geneticalgorithm as ga


def f(X):
    print(X)
    return np.sum(X)


varbound=np.array([[0,10]]*3)

model=ga(function=f,dimension=3,variable_type='int',variable_boundaries=varbound)

model.run()
