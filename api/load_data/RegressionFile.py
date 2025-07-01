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
from backend.results.ResultsFileManager import ResultsFileManager
class RegressionFile(QObject):
    def __init__(self):
        super().__init__()
        self._errors = []
        self._data_parameters = {}
        self._data_parameters_list = []
        self._metrics = Simulation.Metrics
        self._sim = {"CALIBRATION":None,
                    "VALIDATION" : None}
        self._metrics_summary = { }
        self._regressor = "NSE"

    parameters_type = ["pn","qb","sim","loss"]
    dataParametersListChanged = Signal()
    simvaluesChanged = Signal()
    metricsSummaryChanged = Signal()
    currentRegressorChanged = Signal()

    @Property(list, constant = True)
    def regressors(self):
        return Regressor.methodsList()

    @Property(str, notify = currentRegressorChanged)
    def currentRegressor(self):
        return self._regressor

    @Property(dict, notify = simvaluesChanged)
    def simValues(self):
        return self._sim


    @Property(dict, notify = metricsSummaryChanged)
    def metricsSummary(self):
        return self._metrics_summary

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
            print("-------- GP RF -------")
            print(model_data)
            model_data["id"] = path
            self._data_parameters_list.append(model_data)
        self.dataParametersListChanged.emit()

    @Slot(dict, str)
    def singleCalibration(self, ptq, regressor):
        if not regressor in Regressor.methodsList():
            self._errors.append("Provided regressor or metric are non-correct")
            return
        calibration_df = pd.DataFrame(ptq["CALIBRATION"])
        validation_df = pd.DataFrame(ptq["VALIDATION"])

        ptq_calibration = PTQ(calibration_df["P"], calibration_df["ETP"],
        calibration_df["Q"], calibration_df["Dates"])

        ptq_validation = PTQ(validation_df["P"], validation_df["ETP"],
        validation_df["Q"], validation_df["Dates"])

        sm_list = []
        reg = None
        print("RF SC; self._data_parameters_list : ", self._data_parameters_list)
        for json_data_dict in self._data_parameters_list.copy() :
            original_dict = dict(json_data_dict)
            del original_dict['id']

            dict_params = {}
            dict_methods = {}

            for key, model_dict in original_dict.items():
                # Récupérer le nom du modèle (il y a une seule clé à ce niveau)
                model_name = next(iter(model_dict))
                model_params = model_dict[model_name]

                dict_methods[key] = model_name
                dict_params[key] = list(model_params.values())

            else:
                self._errors.append("Required methods not provided")

            if any(item is None for values in dict_params.values() for item in values):
                self._errors.append("Provided parameters are non-correct")
                return

            sim = Simulation(dict_methods["pn"],dict_methods["qb"],
            dict_methods["sim"],dict_methods["loss"], ptq_calibration, ptq_validation)

            hun_sim_cal = sim.manual_calibration(dict_params)

            hun_sim_val = sim.validation()

            sm = SimulationModel(hun_sim_cal.tolist(), hun_sim_val[1].tolist(), None, None, None)

            reg = Regressor(ptq_calibration,ptq_validation)
            sm_list.append(sm)


        reg_method = reg.methods()[regressor](sm_list)

        self._sim["CALIBRATION"] = (reg_method[0].calibration_sim).tolist()
        self._sim["VALIDATION"] = (reg_method[0].validation_sim).tolist()

        metrics_calibration = reg_method[1][0]
        metrics_validation = reg_method[1][1]



        self._metrics_summary = merged = {k: [float(metrics_calibration[k]), float(metrics_validation[k])] for k in metrics_calibration}

        self.simvaluesChanged.emit()
        self.metricsSummaryChanged.emit()

    @Slot(str, str)
    def saveParameters(self,regressor,path):
        parameter_bundle = {
            "datalist" : self._data_parameters_list,
            "regressor" : regressor
        }
        ResultsFileManager.save_regression_results(parameter_bundle, path)

    @Slot(str)
    def deleteModel(self,id):
        ids = [ model["id"] for model in self._data_parameters_list]
        index = ids.index(id)
        if(index != -1):
            self._data_parameters_list.pop(index)
            self.dataParametersListChanged.emit()

    @Slot(str)
    def loadParameters(self,path):
        parameter_bundle = ResultsFileManager.load_regression_results(path)
        self._data_parameters_list = parameter_bundle["datalist"]
        self._regressor = parameter_bundle["regressor"]
        self.dataParametersListChanged.emit()
        self.currentRegressorChanged.emit()



    @Property(list, notify = dataParametersListChanged)
    def parametersList(self):
        return self._data_parameters_list


    def check_keys_match(self, d, keys_list):
        dict_keys = set(d.keys())
        list_keys = set(keys_list)
        return dict_keys == list_keys
