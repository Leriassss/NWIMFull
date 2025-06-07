# This Python file uses the following encoding: utf-8

import pandas as pd
import numpy as np
import datetime

from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement

from backend.ptq.PTQ import PTQ
from backend.results.ResultsFileManager import ResultsFileManager
from backend.simulation.Simulation import Simulation
from backend.simulation.models.SimulationModel import SimulationModel
from backend.regressor.Regressor import Regressor
class RegressionFile(QObject):
    def __init__(self):
        super().__init__()
        self._errors = []
        self._data_parameters = {}
        self._data_parameters_list = []
        self._metrics = Simulation.Metrics
        self._sim = {"CALIBRATION":None,
                    "VALIDATION" : None}

    parameters_type = ["pn","qb","sim","loss"]
    dataParametersListChanged = Signal()
    simvaluesChanged = Signal()

    @Property(list, constant = True)
    def regressors(self):
        print("/*/-*/-*/-*/*/-*/-*/ RF F")
        print(Regressor.methodsList())
        return Regressor.methodsList()

    @Property(dict, notify = simvaluesChanged)
    def simValues(self):
        return self._sim


    @Slot(str)
    def setRegressor(self, metric):
        if metric in list(Regressor.methods().keys()):
            self._optim_metric = metric
        else:
            raise Exception("Metric not found")

    @Slot(list)
    def getParameters(self, paths):
        for path in paths :
            path = path.toString()[8:]
            model_data = ResultsFileManager.load_calibration_results(path)
            model_data["id"] = path
            self._data_parameters_list.append(model_data)
        self.dataParametersListChanged.emit()

    @Slot(dict, dict, str)
    def singleCalibration(self,original_dict, ptq, regressor):
        if not regressor in Regressor.methodsList():
            self._errors.append("Provided regressor or metric are non-correct")
            return

        del original_dict['id']

        dict_params = {}
        dict_methods = {}

        for key, model_dict in original_dict.items():
            # Récupérer le nom du modèle (il y a une seule clé à ce niveau)
            model_name = next(iter(model_dict))
            model_params = model_dict[model_name]

            dict_methods[key] = model_name
            dict_params[key] = list(model_params.values())

            print("-----singleCalibration-----")
            print(dict_methods)
            print(dict_params)
        else:
            self._errors.append("Required methods not provided")

        if any(item is None for values in dict_params.values() for item in values):
            self._errors.append("Provided parameters are non-correct")
            return


        calibration_df = pd.DataFrame(ptq["CALIBRATION"])
        validation_df = pd.DataFrame(ptq["VALIDATION"])

        ptq_calibration = PTQ(calibration_df["P"], calibration_df["ETP"],
        calibration_df["Q"], calibration_df["Dates"])

        ptq_validation = PTQ(validation_df["P"], validation_df["ETP"],
        validation_df["Q"], validation_df["Dates"])

        sim = Simulation(dict_methods["pn"],dict_methods["qb"],
        dict_methods["sim"],dict_methods["loss"], ptq_calibration, ptq_validation)

        hun_sim_cal = sim.manual_calibration(dict_params)

        hun_sim_val = sim.validation()

        sm = SimulationModel(hun_sim_cal.tolist(), hun_sim_val[1].tolist(), None, None, None)


        reg = Regressor(ptq_calibration,ptq_validation)

        reg_method = reg.methods()[regressor]([sm])



        self._sim["CALIBRATION"] = (reg_method[0].calibration_sim).tolist()
        self._sim["VALIDATION"] = (reg_method[0].validation_sim).tolist()

        metrics_calibration = reg_method[1][0]
        metrics_validation = reg_method[1][1]

        print("-*-*-*-*-*-RF SC-*-*-*-*-*-**")
        print(reg_method)
        print(self._sim)

        print(metrics_calibration, metrics_validation)

        self.simvaluesChanged.emit()




    @Property(list, notify = dataParametersListChanged)
    def parametersList(self):
        return self._data_parameters_list


    def check_keys_match(self, d, keys_list):
        dict_keys = set(d.keys())
        list_keys = set(keys_list)
        return dict_keys == list_keys
