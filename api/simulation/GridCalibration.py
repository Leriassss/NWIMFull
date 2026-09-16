import pandas as pd
import numpy as np

from backend.results.ResultsFileManager import ResultsFileManager
from backend.simulation.Simulation import Simulation
from backend.grid.Grid import Grid, GridModel
from backend.ptq.PTQ import PTQ
from backend.workers.BackendThread import BackendThread
from PySide6.QtCore import QObject, Signal, Slot, Property

class GridCalibration(QObject):
    def __init__(self):
        super().__init__()
        self._parameter_bundle = {}
        self._parameters_methods = {}
        self._ptq = {}
        self._grid_thread = None  # <- stockage du thread

        self._errors = []
        self._sim = None
        self._metrics = Simulation.Metrics
        self._optim_metric = "NSE"
        self._best_metrics = ["", ""]
        self._optim_result = None

    metricsChanged = Signal()
    errorsChanged = Signal()
    optimParamsChanged = Signal()
    bestMetricsChanged = Signal()
    paramsBundleChanged = Signal()
    parameters_type = ["pn", "qb", "sim", "loss"]

    @Property(list, notify=errorsChanged)
    def errors(self):
        return self._errors

    @Property(list, constant=True)
    def metrics(self):
        return self._metrics

    @Property(list, notify=bestMetricsChanged)
    def bestMetrics(self):
        return self._best_metrics

    @Property(dict, notify=optimParamsChanged)
    def optimParams(self):
        return self._optim_result

    @Property(dict, notify=paramsBundleChanged)
    def paramsBundle(self):
        return self._parameter_bundle

    @Slot(str)
    def setMetric(self, metric):
        if metric in self._metrics:
            self._optim_metric = metric
        else:
            raise Exception("Metric not found")

    @Slot(dict, list, str, str, dict)
    def gridCalibration(self, params_dict, optim_list, weightNSE, weightKGE, ptq):
        self._errors = []
        self._optim_result = None

        self._parameter_bundle = {"pn": None, "qb": None, "sim": None, "loss": None}
        self._parameters_methods = {"pn": None, "qb": None, "sim": None, "loss": None}
        self._ptq = ptq

        if not set(self._ptq.keys()) == set(["CALIBRATION", "VALIDATION"]):
            raise Exception("Calibration and validation datas not found")

        if len(self._ptq["CALIBRATION"]) == 0 or len(self._ptq["VALIDATION"]) == 0:
            self._errors.append("Calibration and validation datas not provided")
            return

        if self.check_keys_match(params_dict, self.parameters_type):
            for key in self.parameters_type:
                range_parameter_model_list = params_dict[key]
                if len(range_parameter_model_list) == 0:
                    self._errors.append("Required methods not provided")
                    return

                self._parameter_bundle[key] = []
                self._parameters_methods[key] = []
                for range_parameter_model in range_parameter_model_list:
                    methodKeys = list(range_parameter_model.property('methodKeys').keys())
                    parameters_dict = dict(zip(
                        range_parameter_model.property('parameterNames'),
                        range_parameter_model.property('parameterValues')
                    ))
                    if self.check_keys_match(parameters_dict, methodKeys):
                        self._parameter_bundle[key].append(parameters_dict)
                        self._parameters_methods[key].append(range_parameter_model.property('currentMethod'))
                        self.paramsBundleChanged.emit()
                    else:
                        self._errors.append("Required parameters not provided")
        else:
            self._errors.append("Required methods not provided")

        if any(item is None for values in self._parameter_bundle.values() for item in values):
            self._errors.append("Provided parameters are non-correct")
            return

        grid_bundle = {
            key: {
                self._parameters_methods[key][index]: self._parameter_bundle[key][index]
                for index in range(len(self._parameters_methods[key]))
            }
            for key in self.parameters_type
        }

        calibration_df = pd.DataFrame(self._ptq["CALIBRATION"])
        validation_df = pd.DataFrame(self._ptq["VALIDATION"])

        ptq_calibration = PTQ(
            calibration_df["P"], calibration_df["ETP"],
            calibration_df["Q"], calibration_df["Dates"]
        )

        ptq_validation = PTQ(
            validation_df["P"], validation_df["ETP"],
            validation_df["Q"], validation_df["Dates"]
        )

        m_weightNSE = float(weightNSE) if 0 <= float(weightNSE) <= 1 else 1
        m_weightKGE = 1 - m_weightNSE

        optim = optim_list[0]
        optim_parameters = optim.property('parameters')
        optimizator_name = optim.property('currentMethod')

        gm = GridModel(grid_bundle["pn"], grid_bundle["qb"], grid_bundle["sim"], grid_bundle["loss"])
        grid_search_ga = Grid(gm, ptq_calibration, ptq_validation)

        def _run_grid():
            return grid_search_ga.grid_optimization(
                m_weightNSE,
                m_weightKGE,
                optimizator_name,
                **optim_parameters
            )

        # Stocker le thread dans self pour éviter destruction
        self._grid_thread = BackendThread(_run_grid)

        def on_grid_finished(result):
            grid_results_ga, combn = result

            self._optim_result = {
                key: {
                    method_name: {
                        param: paramValue
                        for param, paramValue in zip(
                            grid_bundle[key][method_name].keys(),
                            grid_results_ga.params[key]
                        )
                    }
                }
                for key, method_name in dict(zip(['pn', 'qb', 'sim', 'loss'], combn)).items()
            }

            self._best_metrics = [
                float(np.round(grid_results_ga.calibration_metric, 3)),
                float(np.round(grid_results_ga.validation_metric, 3))
            ]

            self.optimParamsChanged.emit()
            self.bestMetricsChanged.emit()

        self._grid_thread.finished.connect(on_grid_finished)
        self._grid_thread.finished.connect(self._grid_thread.deleteLater)
        self._grid_thread.error.connect(lambda e: print("Grid error:", e))
        self._grid_thread.start()

    def check_keys_match(self, d, keys_list):
        return set(d.keys()) == set(keys_list)

    @Slot(str)
    def saveSimulationResults(self, path):
        if self._optim_result is not None:
            ResultsFileManager.save_calibration_results(self._optim_result, path)
