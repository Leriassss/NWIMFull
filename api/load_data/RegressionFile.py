# This Python file uses the following encoding: utf-8

import pandas as pd
import numpy as np
import datetime

from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement

from backend.ptq.PTQ import PTQ

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
        self._data_qsim_list = []
        self._metrics = Simulation.Metrics
        self._sim = {"CALIBRATION":None,
                    "VALIDATION" : None}
        self._metrics_summary = { }
        self._regressor = {"model" : None, "hyperparameters" : None}
        self._sim_finished = False


    parameters_type = ["pn","qb","sim","loss"]
    dataParametersListChanged = Signal()
    dataQSimListChanged = Signal()
    simvaluesChanged = Signal()
    metricsSummaryChanged = Signal()
    currentRegressorChanged = Signal()
    errorsChanged = Signal()

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    @Property(list, constant = True)
    def regressors(self):
        return Regressor.methodsList()

    @Property(list, notify = dataQSimListChanged)
    def qSimList(self):
        return self._data_qsim_list

    @Property(list, notify = dataParametersListChanged)
    def parametersList(self):
        return self._data_parameters_list

    @Property(dict, notify = currentRegressorChanged)
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

    @Slot(list)
    def getQSim(self, paths):
        for path in paths :
            path = path.toString()[8:]
            self._data_qsim_list.append({"id" : path,"data" : pd.read_table(path, sep= '\t', header = 0)})
        self.dataQSimListChanged.emit()

    @Slot(dict, str)
    def singleCalibration(self, ptq, regressor):
        self._sim_finished = False
        self._errors = []
        self._sim = {"CALIBRATION":None,
                    "VALIDATION" : None,
                    "HYPERPARAMETERS" : None}
        self._ptq = ptq
        print("-------- SC RF -------")
        print(self._ptq.keys())
        if not set(self._ptq.keys()) == set(["CALIBRATION","VALIDATION"]) :
            self._errors.append("Calibration and validation datas not found")
            self.errorsChanged.emit()
            return

        if len(self._ptq["CALIBRATION"]) == 0 or len(self._ptq["VALIDATION"]) == 0:
            self._errors.append("Calibration and validation datas not not provided")
            self.errorsChanged.emit()
            return

        if not regressor in Regressor.methodsList():
            self._errors.append("Provided regressor or metric are non-correct")
            self.errorsChanged.emit()
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
                self.errorsChanged.emit()

            if any(item is None for values in dict_params.values() for item in values):
                self._errors.append("Provided parameters are non-correct")
                self.errorsChanged.emit()
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

        self._regressor = {"model" : regressor, "hyperparameters" : reg_method[0].params}


        self._sim_finished = True
        metrics_calibration = reg_method[1][0]
        metrics_validation = reg_method[1][1]

        self._metrics_summary = merged = {k: [float(metrics_calibration[k]), float(metrics_validation[k])] for k in metrics_calibration}

        self.simvaluesChanged.emit()
        self.metricsSummaryChanged.emit()
        self.currentRegressorChanged.emit()


    @Slot(dict, str)
    def qSimRegression(self, ptq, regressor):
            self._sim_finished = False
            self._errors = []
            self._ptq = ptq
            print("-------- QSR RF -------")
            print(self._ptq.keys())
            if not set(self._ptq.keys()) == set(["CALIBRATION","VALIDATION"]) :
                self._errors.append("Calibration and validation datas not found")
                self.errorsChanged.emit()
                return

            if len(self._ptq["CALIBRATION"]) == 0 or len(self._ptq["VALIDATION"]) == 0:
                self._errors.append("Calibration and validation datas not not provided")
                self.errorsChanged.emit()
                return

            if not regressor in Regressor.methodsList():
                self._errors.append("Provided regressor or metric are non-correct")
                self.errorsChanged.emit()
                return
            calibration_df = pd.DataFrame(ptq["CALIBRATION"])
            validation_df = pd.DataFrame(ptq["VALIDATION"])


            ptq_calibration = PTQ(calibration_df["P"], calibration_df["ETP"],
            calibration_df["Q"], calibration_df["Dates"])

            ptq_validation = PTQ(validation_df["P"], validation_df["ETP"],
            validation_df["Q"], validation_df["Dates"])

            sm_list = []
            reg = None
            calibration_dates = pd.to_datetime(calibration_df["Dates"])
            validation_dates = pd.to_datetime(validation_df["Dates"])
            print("RF SC; self._data_qsim_list : ", self._data_qsim_list)
            for json_data_dict in self._data_qsim_list.copy() :
                if set(json_data_dict["data"].columns.tolist()) != set(['Dates', 'Obs', 'Sim']) :
                    self._errors.append("Wrong data format")
                    self.errorsChanged.emit()
                    return

                df = dict(json_data_dict)["data"]
                df["Dates"] = pd.to_datetime(df["Dates"])
                df.index = df["Dates"]

                sm = SimulationModel(df["Sim"].loc[calibration_dates].tolist(),
                                    df["Sim"].loc[validation_dates].tolist(), None, None, None)

                reg = Regressor(ptq_calibration,ptq_validation)
                sm_list.append(sm)


            reg_method = reg.methods()[regressor](sm_list)

            self._sim["CALIBRATION"] = (reg_method[0].calibration_sim).tolist()
            self._sim["VALIDATION"] = (reg_method[0].validation_sim).tolist()

            self._sim_finished = True
            metrics_calibration = reg_method[1][0]
            metrics_validation = reg_method[1][1]

            self._metrics_summary = merged = {k: [float(metrics_calibration[k]), float(metrics_validation[k])] for k in metrics_calibration}

            self.simvaluesChanged.emit()
            self.metricsSummaryChanged.emit()
            self.currentRegressorChanged.emit()


    @Slot(str)
    def saveQSim(self, path):
        self._errors = []
        if self._sim_finished :
            print("**- SQS/**")
            print(len(np.concatenate([self._ptq["CALIBRATION"]["Dates"],self._ptq["VALIDATION"]["Dates"]])))
            print(len(np.concatenate([self._ptq["CALIBRATION"]["Q"],self._ptq["VALIDATION"]["Q"]])))
            print(len(np.concatenate([self._sim["CALIBRATION"],self._sim["VALIDATION"]])))
            df = pd.DataFrame({
                    "Dates":np.concatenate([self._ptq["CALIBRATION"]["Dates"],self._ptq["VALIDATION"]["Dates"]]),
                    "Obs" : np.concatenate([self._ptq["CALIBRATION"]["Q"],self._ptq["VALIDATION"]["Q"]]),
                    "Sim" : np.concatenate([self._sim["CALIBRATION"],self._sim["VALIDATION"]])
                    })
            ResultsFileManager.saveData(df, path)
        else :
            self._errors.append("No data found... Please run a model before")
            self.errorsChanged.emit()


    @Slot(str, str)
    def saveParameters(self,regressor,path):
        parameter_bundle = {
            "datalist" : self._data_parameters_list,
            "regressor" : self._regressor
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
    def deleteQSim(self,id):
        ids = [ model["id"] for model in self._data_qsim_list]
        index = ids.index(id)
        if(index != -1):
            self._data_qsim_list.pop(index)
            self.dataQSimListChanged.emit()

    @Slot(str)
    def loadParameters(self,path):
        parameter_bundle = ResultsFileManager.load_regression_results(path)
        self._data_parameters_list = parameter_bundle["datalist"]
        self._regressor = parameter_bundle["regressor"]
        self.dataParametersListChanged.emit()
        self.currentRegressorChanged.emit()


    def check_keys_match(self, d, keys_list):
        dict_keys = set(d.keys())
        list_keys = set(keys_list)
        return dict_keys == list_keys
