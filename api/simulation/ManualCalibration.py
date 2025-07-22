import pandas as pd
import numpy as np
import datetime

from backend.simulation.Simulation import Simulation
from backend.results.ResultsFileManager import ResultsFileManager
from backend.ptq.PTQ import PTQ
from backend.smooth.Smooth import Smooth
from api.load_data.DataManager import DataManager
from dateutil import parser
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement
from itertools import zip_longest

from permetrics.regression import RegressionMetric

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
        self._smooth = Smooth()
        self._smoothing = {}
        self._smoothness = {}
        self._rolling = {}


    parameters_type = ["pn","qb","sim","loss"]
    paramsBundleChanged = Signal()
    errorsChanged = Signal()
    simChanged = Signal()
    smoothingChanged = Signal()
    rollingChanged = Signal()
    smoothnessChanged = Signal()

    @Property(dict, notify=smoothingChanged)
    def smoothingValues(self):
        return self._smoothing

    @Property(dict, notify=smoothnessChanged)
    def smoothnessValues(self):
        return self._smoothness

    @Property(dict, notify=rollingChanged)
    def rollingValues(self):
        return self._rolling

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
        print("step 1 - MC ", datetime.datetime.now())
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
                print("methodKeys --- MC :", obj.property('methodKeys'))
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
        print("step 2 - MC ", datetime.datetime.now())
        sim = Simulation(self._parameters_methods["pn"],self._parameters_methods["qb"],
        self._parameters_methods["sim"],self._parameters_methods["loss"], ptq_calibration, ptq_validation)

        hun_sim_cal = sim.manual_calibration(self._parameter_bundle)

        hun_sim_val = sim.validation()
        print("step 3 - MC ", datetime.datetime.now())

        self._sim["SIM"]["CALIBRATION"] = hun_sim_cal.tolist()
        self._sim["SIM"]["VALIDATION"] = hun_sim_val[1].tolist()
        self._sim["OBS"]["CALIBRATION"] = calibration_df["Q"].tolist()
        self._sim["OBS"]["VALIDATION"] = validation_df["Q"].tolist()

        self._sim["DATES"]["CALIBRATION"] = calibration_df["Dates"].tolist()
        self._sim["DATES"]["VALIDATION"] = validation_df["Dates"].tolist()

        self._sim["CRITERIA"]["CALIBRATION"] = {key : np.round(value,3).tolist() for key,value in  sim.calibration_metric.items()}
        self._sim["CRITERIA"]["VALIDATION"] = {key : np.round(value,3).tolist() for key,value in  hun_sim_val[0].items()}
        print("step 4 - MC ", datetime.datetime.now())
        self._sim_finished = True
        print("------------------------- SIM (MC)---------------")
        self.simChanged.emit()
        print("step 5 - MC ", datetime.datetime.now())


    @Slot(str)
    def saveQSim(self, path):
        if self._sim_finished :
            print("MC ------saveQSim")
            if len(self._smoothness) == 0:
                df = pd.DataFrame({
                    "Dates":np.concatenate([self._sim["DATES"]["CALIBRATION"],self._sim["DATES"]["VALIDATION"]]),
                    "Obs" : np.concatenate([self._sim["OBS"]["CALIBRATION"],self._sim["OBS"]["VALIDATION"]]),
                    "Sim" : np.concatenate([self._sim["SIM"]["CALIBRATION"],self._sim["SIM"]["VALIDATION"]])
                    })
            else:
                df = pd.DataFrame({
                    "Dates":np.concatenate([self._sim["DATES"]["CALIBRATION"],self._sim["DATES"]["VALIDATION"]]),
                    "Obs" : np.concatenate([self._sim["OBS"]["CALIBRATION"],self._sim["OBS"]["VALIDATION"]]),
                    "Sim" : np.concatenate([self._smoothness["CALIBRATION"],self._smoothness["VALIDATION"]])
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



    @Slot(dict, float, int)
    def smoothness(self, sim, output_limit, window):
        print("window :", window)
        print("output_limit :", output_limit)
        self._smoothness = {}
        if output_limit == 0 and window != 0:
            self._smoothness = {
                    "CALIBRATION" : self._smooth.compute_lissage(sim["SIM"]["CALIBRATION"],window).tolist(),
                    "VALIDATION" : self._smooth.compute_lissage(sim["SIM"]["VALIDATION"],window).tolist()
                }
        elif window == 0 and output_limit !=0:
            self._smoothness = {
                    "CALIBRATION" : self._smooth.compute_laminage(sim["SIM"]["CALIBRATION"],output_limit).tolist(),
                    "VALIDATION" : self._smooth.compute_laminage(sim["SIM"]["VALIDATION"],output_limit).tolist()
                }
        elif output_limit != 0 and window != 0 :
            lissage_cal = self._smooth.compute_lissage(sim["SIM"]["CALIBRATION"],window)
            lissage_val = self._smooth.compute_lissage(sim["SIM"]["VALIDATION"],window)
            self._smoothness = {
                    "CALIBRATION" : self._smooth.compute_laminage(lissage_cal,output_limit).tolist(),
                    "VALIDATION" : self._smooth.compute_laminage(lissage_val,output_limit).tolist()
                }
        else:
            self._smoothness = {
                    "CALIBRATION" : sim["SIM"]["CALIBRATION"],
                    "VALIDATION" : sim["SIM"]["VALIDATION"]
                }
        evaluator_calib = RegressionMetric(np.array(sim["OBS"]["CALIBRATION"]), np.array(self._smoothness["CALIBRATION"]))
        evaluator_valid = RegressionMetric(np.array(sim["OBS"]["VALIDATION"]), np.array(self._smoothness["VALIDATION"]))

        calibration_metric = evaluator_calib.get_metrics_by_list_names(["NSE", "KGE", "RMSE", "MAE", "MAPE", "R2"])
        validation_metric = evaluator_valid.get_metrics_by_list_names(["NSE", "KGE", "RMSE", "MAE", "MAPE", "R2"])

        self._sim["CRITERIA"]["CALIBRATION"] = {key : np.round(value,3).tolist() for key,value in  calibration_metric.items()}
        self._sim["CRITERIA"]["VALIDATION"] = {key : np.round(value,3).tolist() for key,value in  validation_metric.items()}
        self.simChanged.emit()
        self.smoothnessChanged.emit()


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
