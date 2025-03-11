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

from simulation.Simulation import Simulation
from simulation.models.SimulationModel import SimulationModel

class ManualCalibration:
    def __init__(self,simulation : Simulation):
        self.simulation = simulation
        self.kwargs = []


    def sim(self,kwargs: RoutingData):
        qsim_calibration = self.simulation.manual_calibration(kwargs)
        criteria_calibration = self.simulation.criteria.methods()[self.simulation.crit](self.simulation.ptq_calage.q,
                                                                        qsim_calibration)
        
        criteria_validation,qsim_validation = self.simulation.validation()
        self.kwargs = self.simulation.kwargs
        return SimulationModel(qsim_calibration, qsim_validation , self.simulation.kwargs,  criteria_calibration, criteria_validation)


    
