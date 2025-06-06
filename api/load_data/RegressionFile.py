# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement

from backend.results.ResultsFileManager import ResultsFileManager

class RegressionFile(QObject):
    def __init__(self):
        super().__init__()

        self._data_parameters = {}
        self._data_parameters_list = []

    dataParametersListChanged = Signal()


    @Slot(str)
    def getParameters(self, path):
        model_data = ResultsFileManager.load_calibration_results(path)
        model_data["id"] = path
        self._data_parameters_list.append(model_data)
        self.dataParametersListChanged.emit()


    @Property(list, notify = dataParametersListChanged)
    def parametersList(self):
        return self._data_parameters_list

