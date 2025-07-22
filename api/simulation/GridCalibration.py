import pandas as pd
import numpy as np
import datetime

from backend.simulation.Simulation import Simulation
from backend.grid.Grid import Grid,GridModel
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
    def gridCalibration(self, params_dict, optim_list, ptq):
        self._errors = []

        self._parameter_bundle =  {
        "pn":None,"qb":None,"sim": None,"loss" : None
        }
        self._parameters_methods = {
            "pn":None,"qb":None,"sim": None,"loss" : None
        }
        print("GC GridCalibration--------")
        print(params_dict)
        self._ptq = ptq

        if self.check_keys_match(params_dict, self.parameters_type):
            for key in self.parameters_type :
                range_parameter_model_list = params_dict[key]
                if len(range_parameter_model_list) == 0 :
                    self._errors.append("Required methods not provided")
                    return

                self._parameter_bundle[key] = []
                self._parameters_methods[key] = []
                for range_parameter_model in range_parameter_model_list:
                    #A CHANGER POUR FAIRE PASSER DU KEY A VALUE
                    methodKeys = list(range_parameter_model.property('methodKeys').keys())
                    parameters_dict = dict(zip(range_parameter_model.property('parameterNames'), range_parameter_model.property('parameterValues')))
                    #parameters_dict = range_parameter_model.property('parameters')
                    if self.check_keys_match(parameters_dict, methodKeys) :
                        self._parameter_bundle[key].append(parameters_dict)
                        self._parameters_methods[key].append(range_parameter_model.property('currentMethod'))

                        self.paramsBundleChanged.emit()
                    else:
                        self._errors.append("Required parameters not provided")
        else:
            self._errors.append("Required methods not provided")


        print("GC GC--- 1 : ", self._parameter_bundle)
        print("GC GC--- 2 : ",self._parameters_methods)


        if any(item is None for values in self._parameter_bundle.values() for item in values):
            self._errors.append("Provided parameters are non-correct")
            return

        grid_bundle = {key : {self._parameters_methods[key][index] : self._parameter_bundle[key][index] for index in  range(0, len(self._parameters_methods[key]))} for key in self.parameters_type}
        print("grid_bundle : ", grid_bundle)

        calibration_df = pd.DataFrame(self._ptq["CALIBRATION"])
        validation_df = pd.DataFrame(self._ptq["VALIDATION"])

        ptq_calibration = PTQ(calibration_df["P"], calibration_df["ETP"],
            calibration_df["Q"], calibration_df["Dates"])

        ptq_validation = PTQ(validation_df["P"], validation_df["ETP"],
            validation_df["Q"], validation_df["Dates"])

        optim = optim_list[0]
        optim_parameters = optim.property('parameters')
        optimizator_name = optim.property('currentMethod')

        gm = GridModel(grid_bundle["pn"], grid_bundle["qb"], grid_bundle["sim"], grid_bundle["loss"])

        grid_search_ga = Grid(gm, ptq_calibration, ptq_validation)


        grid_results_ga, combn = grid_search_ga.grid_optimization(optimizator_name, **optim_parameters)

        #sim.crit = self._optim_metric

        print(" ------ optim res -------")

        best_results = {
            method_name : {
                param: paramValue for param, paramValue in zip(grid_bundle[key][method_name].keys(),grid_results_ga.params[key])
            }
            for key, method_name in dict(zip(['pn', 'qb', 'sim', 'loss'], combn)).items()
        }
        print(best_results)
        print(grid_results_ga.calibration_metric)
        print(grid_results_ga.validation_metric)





    def check_keys_match(self, d, keys_list):
        dict_keys = set(d.keys())
        list_keys = set(keys_list)
        return dict_keys == list_keys
