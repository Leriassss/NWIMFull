import pandas as pd
import numpy as np
import datetime

from backend.simulation.Simulation import Simulation
from backend.ptq.PTQ import PTQ
from backend.factory.OptimizationFactory import OptimizationFactory
from PySide6.QtCore import QObject, Signal, Slot, Property

class GridCalibration(QObject):
    def __init__(self):
        super().__init__()
        self._parameter_bundle =  {}
        self._parameters_methods = {}
        self._ptq = {}

        self._errors = []
        self._sim = None
        self._metrics = Simulation.Metrics
        self._optim_metric = "NSE"

    metricsChanged = Signal()
    errorsChanged = Signal()
    paramsBundleChanged = Signal()
    parameters_type = ["pn","qb","sim","loss"]

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    @Property(list, constant=True)
    def metrics(self):
        return self._metrics

    @Slot(str)
    def setMetric(self, metric):
        print("---------- setMetric AC------------")
        print(self._metrics)
        print(metric)
        if metric in self._metrics:
            self._optim_metric = metric
        else:
            raise Exception("Metric not found")

    @Property(dict, notify=paramsBundleChanged)
    def paramsBundle(self):
        return self._parameter_bundle

    @Slot(dict, list, dict)
    def setParameters(self, params_dict, optim_list, ptq):
        self._errors = []

        self._parameter_bundle =  {
        "pn":None,"qb":None,"sim": None,"loss" : None
        }
        self._parameters_methods = {
            "pn":None,"qb":None,"sim": None,"loss" : None
        }

        self._ptq = ptq

        if self.check_keys_match(params_dict, self.parameters_type):
            for key in self.parameters_type :
                range_parameter_model = params_dict[key]
                    #A CHANGER POUR FAIRE PASSER DU KEY A VALUE
                methodKeys = list(range_parameter_model.property('methodKeys').keys())
                parameters_dict = range_parameter_model.property('parameters')
                if self.check_keys_match(parameters_dict, methodKeys) :
                    self._parameter_bundle[key] = parameters_dict
                    self._parameters_methods[key] = range_parameter_model.property('currentMethod')

                    self.paramsBundleChanged.emit()
                else:
                    self._errors.append("Required parameters not provided")
        else:
            self._errors.append("Required methods not provided")

        print("---- setParameters AC --------")
        print(self._parameter_bundle)
        print(self._parameters_methods)

        if any(item is None for values in self._parameter_bundle.values() for item in values):
            self._errors.append("Provided parameters are non-correct")
            return

        calibration_df = pd.DataFrame(self._ptq["CALIBRATION"])
        validation_df = pd.DataFrame(self._ptq["VALIDATION"])

        ptq_calibration = PTQ(calibration_df["P"], calibration_df["ETP"],
            calibration_df["Q"], calibration_df["Dates"])

        ptq_validation = PTQ(validation_df["P"], validation_df["ETP"],
            validation_df["Q"], validation_df["Dates"])

        sim = Simulation(self._parameters_methods["pn"],self._parameters_methods["qb"],
        self._parameters_methods["sim"],self._parameters_methods["loss"], ptq_calibration, ptq_validation)

        sim.crit = self._optim_metric

        optim = optim_list[0]
        optim_parameters = optim.property('parameters')
        optimizator_name = optim.property('currentMethod')
        optimizator = OptimizationFactory.createInstance(optimizator_name, sim, self._parameter_bundle, optim_parameters)
        print("---- setParameters 2 AC --------")
        print(optim_parameters)
        print(optimizator)

        sim_r_hun = optimizator.optim()
        print(" ------ optim res -------")
        print(sim_r_hun.params)
        print(sim_r_hun.calibration_metric)
        print(sim_r_hun.validation_metric)





    def check_keys_match(self, d, keys_list):
        dict_keys = set(d.keys())
        list_keys = set(keys_list)
        return dict_keys == list_keys
