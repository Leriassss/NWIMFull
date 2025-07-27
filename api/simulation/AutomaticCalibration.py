import pandas as pd
import numpy as np
import datetime

from backend.simulation.Simulation import Simulation
from backend.ptq.PTQ import PTQ
from backend.factory.OptimizationFactory import OptimizationFactory
from backend.results.ResultsFileManager import ResultsFileManager
from PySide6.QtCore import QObject, Signal, Slot, Property

class AutomaticCalibration(QObject):
    def __init__(self):
        super().__init__()
        self._parameter_bundle =  {}
        self._parameters_methods = {}
        self._ptq = {}

        self._errors = []
        self._sim = None
        self._metrics = Simulation.Metrics
        self._optim_metric = "NSE"
        self._optim_result = None
        self._best_metrics = ["",""]

    metricsChanged = Signal()
    errorsChanged = Signal()
    paramsBundleChanged = Signal()
    optimParamsChanged = Signal()
    bestMetricsChanged = Signal()
    parameters_type = ["pn","qb","sim","loss"]

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    @Property(list, constant=True)
    def metrics(self):
        return self._metrics

    @Property(list, notify=bestMetricsChanged)
    def bestMetrics(self):
        return self._best_metrics

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

    @Property(dict, notify=optimParamsChanged)
    def optimParams(self):
        return self._optim_result

    @Slot(dict, list, dict)
    def setParameters(self, params_dict, optim_list, ptq):
        self._errors = []
        self._best_metrics = ["",""]

        self._parameter_bundle =  {
        "pn":None,"qb":None,"sim": None,"loss" : None
        }
        self._parameters_methods = {
            "pn":None,"qb":None,"sim": None,"loss" : None
        }

        self._optim_result = None

        self._ptq = ptq

        if not set(self._ptq.keys()) == set(["CALIBRATION","VALIDATION"]) :
            self._errors.append("Calibration and validation datas not found")
            return

        if len(self._ptq["CALIBRATION"]) == 0 or len(self._ptq["VALIDATION"]) == 0:
            self._errors.append("Calibration and validation datas not not provided")
            return

        if self.check_keys_match(params_dict, self.parameters_type):
            for key in self.parameters_type :
                range_parameter_model = params_dict[key]
                    #A CHANGER POUR FAIRE PASSER DU KEY A VALUE
                methodKeys = list(range_parameter_model.property('methodKeys').keys())
                #parameters_dict = range_parameter_model.property('parameters')
                parameters_dict = dict(zip(range_parameter_model.property('parameterNames'), range_parameter_model.property('parameterValues')))
                if self.check_keys_match(parameters_dict, methodKeys) :
                    self._parameter_bundle[key] = parameters_dict
                    self._parameters_methods[key] = range_parameter_model.property('currentMethod')

                    self.paramsBundleChanged.emit()
                else:
                    self._errors.append("Required parameters not provided")
        else:
            self._errors.append("Required methods not provided")

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

        sim_r_hun = optimizator.optim()

        param_names = {section: list(params.keys()) for section, params in self._parameter_bundle.items()}
        original_dict = {}

        for section in self._parameters_methods:
            model = self._parameters_methods[section]
            params_by_section = param_names[section]
            values = sim_r_hun.params[section]

            # Associer les noms de paramètres aux valeurs converties en chaînes
            param_dict = {name: str(value) for name, value in zip(params_by_section, values)}

            # Construire le dictionnaire imbriqué
            original_dict[section] = {model: param_dict}

        self._optim_result = original_dict
        print("sim_r_hun ------------------ : ", sim_r_hun.validation_metric)
        self._best_metrics = [float(np.round(sim_r_hun.calibration_metric,3)),
                                float(np.round(sim_r_hun.validation_metric,3))]

        self.optimParamsChanged.emit()
        self.bestMetricsChanged.emit()

        print("-------- saving ----------")
        print(self._optim_result)
        print(self._best_metrics)



    @Slot(str)
    def saveSimulationResults(self, path):
        if self._optim_result is not None :
            ResultsFileManager.save_calibration_results(self._optim_result, path)


    def check_keys_match(self, d, keys_list):
        dict_keys = set(d.keys())
        list_keys = set(keys_list)
        return dict_keys == list_keys
