import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from backend.ptq.PTQ import PTQ
from backend.simulation.models.SimulationModel import SimulationModel


class SimulationGraph:
    def __init__(self, ptq_calage : PTQ, ptq_validation : PTQ, sim_model : SimulationModel):
        self.sim_model = sim_model
        self.ptq_calage = ptq_calage
        self.ptq_validation = ptq_validation
    
    def plot(self, title):
        q = pd.concat([self.ptq_calage.q, self.ptq_validation.q]).reset_index(drop=True)
        dts = pd.concat([self.ptq_calage.dates, self.ptq_validation.dates]).reset_index(drop=True)
        plt.plot(dts,q,"b")
        plt.plot(self.ptq_calage.dates,self.sim_model.calibration_sim,"r")
        plt.plot(self.ptq_validation.dates,self.sim_model.validation_sim,"y")
        plt.text(self.ptq_validation.dates[300],10,"NSE VALIDATION: " + str(np.round(self.sim_model.validation_metric,2)))
        plt.text(self.ptq_validation.dates[300],9,"NSE CALAGE: " + str(np.round(self.sim_model.calibration_metric,2)))
        plt.legend(["QObs","QSim Calage","QSim Validation"],loc=2)
        plt.title(title,fontsize=15,fontname='Times New Roman')
    
    def help():
        pass


    
