import pandas as pd
import numpy as np
import datetime

from backend.simulation.Simulation import Simulation
from backend.results.ResultsFileManager import ResultsFileManager
from backend.ptq.PTQ import PTQ
from api.load_data.DataManager import DataManager
from dateutil import parser
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement
from itertools import zip_longest

class ManualCalibration(QObject):
    def __init__(self):
        super().__init__()
        self._parameter_bundle =  {}
        self._parameters_methods = {}
        self._ptq = {}

        self._errors = []
        self._sim = {
                    "SIM" : {"CALIBRATION":[], "VALIDATION":[]},
                     "OBS" : {"CALIBRATION":[], "VALIDATION":[]},
                    "DATES" : {"CALIBRATION":[], "VALIDATION":[]},
                    "CRITERIA" : {"CALIBRATION":[], "VALIDATION":[]}
                    }
        self._sim_finished = False


    parameters_type = ["pn","qb","sim","loss"]
    paramsBundleChanged = Signal()
    errorsChanged = Signal()
    simChanged = Signal()

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    @Property(dict, notify=simChanged)
    def simulationValues(self):
        return self._sim

    @Property(dict, notify=paramsBundleChanged)
    def paramsBundle(self):
            return self._parameter_bundle

    @Slot(dict, dict)
    def setParameters(self, params_dict, ptq):
        self._errors = []

        self._parameter_bundle =  {
        "pn":None,"qb":None,"sim": None,"loss" : None
        }
        self._parameters_methods = {
        "pn":None,"qb":None,"sim": None,"loss" : None
        }
        self._sim = {
                    "SIM" : {"CALIBRATION":[], "VALIDATION":[]},
                     "OBS" : {"CALIBRATION":[], "VALIDATION":[]},
                    "DATES" : {"CALIBRATION":[], "VALIDATION":[]},
                    "CRITERIA" : {"CALIBRATION":[], "VALIDATION":[]}
                    }
        self._sim_finished = False

        self._ptq = ptq

        if self.check_keys_match(params_dict, self.parameters_type):
            if not set(self._ptq.keys()) == set(["CALIBRATION","VALIDATION"]) :
                self._errors.append("Calibration and validation datas not found")
                return

            if len(self._ptq["CALIBRATION"]) == 0 or len(self._ptq["VALIDATION"]) == 0:
                self._errors.append("Calibration and validation datas not not provided")
                return

            for key in self.parameters_type :
                obj = params_dict[key]

                #A CHANGER POUR FAIRE PASSER DU KEY A VALUE
                methodKeys = list(obj.property('methodKeys').keys())
                parameters_dict = dict(zip(obj.property('parameterNames'), obj.property('parameterValues')))
                #parameters_dict = obj.property('parameters')
                print("---- setParameters2 MC --------")
                print(parameters_dict)
                print(methodKeys)
                if self.check_keys_match(parameters_dict, methodKeys) :
                    self._parameter_bundle[key] = list(parameters_dict.values())
                    self._parameters_methods[key] = obj.property('currentMethod')

                    self.paramsBundleChanged.emit()
                else:
                    self._errors.append("Required parameters not provided")
        else:
            self._errors.append("Required methods not provided")


        print("---- setParameters MC --------")
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

        hun_sim_cal = sim.manual_calibration(self._parameter_bundle)

        hun_sim_val = sim.validation()

        self._sim["SIM"]["CALIBRATION"] = hun_sim_cal.tolist()
        self._sim["SIM"]["VALIDATION"] = hun_sim_val[1].tolist()
        self._sim["OBS"]["CALIBRATION"] = calibration_df["Q"].tolist()
        self._sim["OBS"]["VALIDATION"] = validation_df["Q"].tolist()

        self._sim["DATES"]["CALIBRATION"] = calibration_df["Dates"].tolist()
        self._sim["DATES"]["VALIDATION"] = validation_df["Dates"].tolist()

        self._sim["CRITERIA"]["CALIBRATION"] = {key : np.round(value,3).tolist() for key,value in  sim.calibration_metric.items()}
        self._sim["CRITERIA"]["VALIDATION"] = {key : np.round(value,3).tolist() for key,value in  hun_sim_val[0].items()}
        self._sim_finished = True
        print("------------------------- SIM (MC)---------------")
        self.simChanged.emit()

    @Slot(str)
    def saveQSim(self, path):
        if self._sim_finished :
            print("MC ------saveQSim")
            df = pd.DataFrame({
                "Dates":np.concatenate([self._sim["DATES"]["CALIBRATION"],self._sim["DATES"]["VALIDATION"]]),
                "Obs" : np.concatenate([self._sim["OBS"]["CALIBRATION"],self._sim["OBS"]["VALIDATION"]]),
                "Sim" : np.concatenate([self._sim["SIM"]["CALIBRATION"],self._sim["SIM"]["VALIDATION"]])
                })
            ResultsFileManager.saveData(df, path)

    @Slot(dict, str)
    def saveParameters(self, params_dict, path):
        parameter_bundle = {}
        parameters_methods = {}
        if self.check_keys_match(params_dict, self.parameters_type):
            for key in self.parameters_type :
                obj = params_dict[key]

                #A CHANGER POUR FAIRE PASSER DU KEY A VALUE
                methodKeys = list(obj.property('methodKeys').keys())
                parameters_dict = dict(zip(obj.property('parameterNames'), obj.property('parameterValues')))
                #parameters_dict = obj.property('parameters')
                print("---- setParameters2 MC --------")
                print(parameters_dict)
                if self.check_keys_match(parameters_dict, methodKeys) :
                    parameter_bundle[key] = {obj.property('currentMethod') :  parameters_dict }
                else:
                    raise("Required parameters not provided")
        else:
            raise("Required parameters not provided")

        ResultsFileManager.save_calibration_results(parameter_bundle, path)





    @Slot(str, dict)
    def loadParameters(self, path,params_dict):
        model_data = ResultsFileManager.load_calibration_results(path)
        print("--------------- MC LP----------------")
        print(model_data)

        if self.check_keys_match(params_dict, self.parameters_type) and self.check_keys_match(model_data, self.parameters_type):
            for key in self.parameters_type :
                obj = params_dict[key]
                method = next(iter(model_data[key]))
                obj.setParameter(model_data[key][method],method)
        else:
            self._errors.append("Required methods not provided")

        print(path)

    def check_keys_match(self, d, keys_list):
        dict_keys = set(d.keys())
        list_keys = set(keys_list)
        return dict_keys == list_keys
